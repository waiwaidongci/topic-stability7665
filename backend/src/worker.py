import json
from pathlib import Path
from sqlalchemy import select
from celery import Celery
from src.config.database import SessionLocal
from src.config.settings import REDIS_URL,ARTIFACT_DIR
from src.models import TopicRun,Corpus,TopicProfile
from src.services.corpora import list_documents
from src.services.analysis import analyze
from src.services.audit import record
from src.utils.serialize import row
app=Celery('topic_stability',broker=REDIS_URL,backend=REDIS_URL)
app.conf.update(task_track_started=True,worker_prefetch_multiplier=1,task_acks_late=True)
@app.task(name='topic.analyze',soft_time_limit=240,time_limit=270)
def analyze_run(id):
 with SessionLocal() as db:
  run=db.get(TopicRun,id)
  if not run or run.status=='succeeded':return
  run.status='running';db.commit()
  try:
   result=analyze(row(db.get(Corpus,run.corpus_id)),list_documents(db,run.corpus_id),run.config)
   for p in result['profiles']:
    if not db.scalar(select(TopicProfile).where(TopicProfile.run_id==id,TopicProfile.topic_index==p['topic_index'])):db.add(TopicProfile(run_id=id,topic_index=p['topic_index'],label=p['label'],weights=p['weights'],mean_similarity=p['mean_similarity']))
   Path(ARTIFACT_DIR).mkdir(parents=True,exist_ok=True);Path(ARTIFACT_DIR,f'topic-{id}.json').write_text(json.dumps(result,ensure_ascii=False,allow_nan=False));run.result=result;run.status='succeeded';run.error=None;db.commit();record(db,'worker','topic.succeeded',{'run_id':id,'repeats':run.config['repeats']})
  except Exception as e:
   db.rollback();run=db.get(TopicRun,id);run.status='failed';run.error=str(e)[:1000];db.commit();record(db,'worker','topic.failed',{'run_id':id,'error':run.error})
