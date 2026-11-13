from pydantic import BaseModel,Field
class ProfilePatch(BaseModel):
 label:str=Field(min_length=1,max_length=100)
 editor_note:str=Field(default='',max_length=500)
