from sqlalchemy import select
from fastapi import HTTPException
from src.models import Corpus,TopicRun
from src.constants.enums import RunStatus
from src.utils.serialize import row
from .audit import record
def list_runs(db):return [row(x) for x in db.scalars(select(TopicRun).order_by(TopicRun.id.desc()))]
def get_run(db,id):
 obj=db.get(TopicRun,id)
 if not obj:raise HTTPException(404,'主题运行不存在')
 return obj
def create_run(db,data,user):
 if not db.get(Corpus,data.corpus_id):raise HTTPException(404,'语料不存在')
 obj=TopicRun(corpus_id=data.corpus_id,name=data.name,config=data.model_dump(exclude={'name','corpus_id'}),creator_id=user.id);db.add(obj);db.commit()
 from src.worker import analyze_run
 try:analyze_run.delay(obj.id)
 except Exception:obj.status=RunStatus.FAILED;obj.error='队列不可用';db.commit();raise HTTPException(503,obj.error)
 record(db,user.email,'topic.queued',{'run_id':obj.id});return row(obj)
