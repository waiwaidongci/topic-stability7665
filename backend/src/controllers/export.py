from fastapi import HTTPException
from src.models import EditorialNote,TopicProfile,TopicRun
from src.constants.enums import NoteStatus
from src.utils.csv_export import csv_response
def export_note(db,id):
 note=db.get(EditorialNote,id)
 if not note:raise HTTPException(404,'编辑说明不存在')
 if note.status!=NoteStatus.APPROVED:raise HTTPException(403,'仅获批说明可导出')
 run=db.get(TopicRun,note.run_id);rows=[]
 for p in note.profile_snapshot:
  for word in p['weights'][:12]:rows.append([note.name,p['topic_index']+1,p['label'],p['editor_note'],word['term'],word['weight'],p['mean_similarity'],run.config['k'],run.config['repeats'],note.interpretation,note.next_step,note.review_note,'相对激活非后验概率；稳定性非语义真值'])
 return csv_response(f'editorial-{id}.csv',rows,['编辑说明','主题编号','人工主题名','命名备注','词','L1词权','平均对齐余弦','预选K','初始化重复','人工解释','下一步','审阅说明','边界'])
