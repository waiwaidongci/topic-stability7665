from pydantic import BaseModel,Field
class RunInput(BaseModel):
 corpus_id:int=Field(gt=0)
 name:str=Field(min_length=1,max_length=100)
 k:int=Field(ge=2,le=6,strict=True)
 repeats:int=Field(ge=5,le=10,strict=True)
 seed:int=Field(ge=0,le=1000000000,strict=True)
 min_df:int=Field(ge=1,le=10,strict=True)
 max_iter:int=Field(ge=10,le=3000,strict=True)
 tolerance:float=Field(ge=1e-8,le=.01,allow_inf_nan=False)
