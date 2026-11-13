from pydantic import BaseModel,Field,model_validator
class DocumentInput(BaseModel):
 reference:str=Field(min_length=1,max_length=80)
 title:str=Field(min_length=1,max_length=120)
 tokens_text:str=Field(max_length=10000)
class CorpusInput(BaseModel):
 name:str=Field(min_length=1,max_length=100)
 filename:str=Field(min_length=1,max_length=160)
 description:str=Field(default='',max_length=500)
 documents:list[DocumentInput]=Field(min_length=5,max_length=1000)
 @model_validator(mode='after')
 def unique_docs(self):
  if len({d.reference for d in self.documents})!=len(self.documents):raise ValueError('文档reference不可重复')
  return self
class DocumentPatch(BaseModel):
 title:str=Field(min_length=1,max_length=120)
 tokens_text:str=Field(max_length=10000)
