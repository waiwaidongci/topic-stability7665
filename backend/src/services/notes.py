from sqlalchemy import select
from fastapi import HTTPException
from src.models import TopicRun,TopicProfile,EditorialNote
from src.constants.enums import RunStatus,NoteStatus
from src.utils.serialize import row
from .audit import record
def list_notes(db):return [row(x) for x in db.scalars(select(EditorialNote).order_by(EditorialNote.id.desc()))]
def create_note(db,data,user):
 run=db.get(TopicRun,data.run_id)
 if not run or run.status!=RunStatus.SUCCEEDED:raise HTTPException(422,'请选择成功主题运行')
 valid=set(db.scalars(select(TopicProfile.id).where(TopicProfile.run_id==run.id)))
 if len(set(data.profile_ids))!=len(data.profile_ids) or not set(data.profile_ids)<=valid:raise HTTPException(422,'主题须来自本运行且不重复')
 snapshot=[row(p) for p in db.scalars(select(TopicProfile).where(TopicProfile.id.in_(data.profile_ids)).order_by(TopicProfile.topic_index))]
 obj=EditorialNote(**data.model_dump(),profile_snapshot=snapshot,creator_id=user.id);db.add(obj);db.commit();record(db,user.email,'editorial.created',{'note_id':obj.id});return row(obj)
def approve_note(db,id,data,user):
 obj=db.get(EditorialNote,id)
 if not obj:raise HTTPException(404,'编辑说明不存在')
 if obj.status!=NoteStatus.DRAFT:raise HTTPException(409,'仅草案可审阅')
 obj.status=data.status;obj.review_note=data.review_note;db.commit();record(db,user.email,'editorial.reviewed',{'note_id':id,'status':obj.status});return row(obj)
