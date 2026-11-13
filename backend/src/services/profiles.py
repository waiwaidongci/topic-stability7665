from sqlalchemy import select
from fastapi import HTTPException
from src.models import TopicProfile
from src.utils.serialize import row
from .audit import record
def list_profiles(db):return [row(x) for x in db.scalars(select(TopicProfile).order_by(TopicProfile.run_id,TopicProfile.topic_index))]
def patch_profile(db,id,data,user):
 obj=db.get(TopicProfile,id)
 if not obj:raise HTTPException(404,'主题不存在')
 obj.label=data.label;obj.editor_note=data.editor_note;db.commit();record(db,user.email,'topic.named',{'profile_id':id,'label':obj.label});return row(obj)
