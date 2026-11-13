from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.controllers.dependencies import current_user,writers
from src.schemas.run import RunInput
from src.schemas.profile import ProfilePatch
from src.services import runs,profiles
from src.utils.serialize import row
router=APIRouter()
@router.get('/runs')
def index(db:Session=Depends(get_db),user=Depends(current_user)):return runs.list_runs(db)
@router.get('/runs/{id}')
def detail(id:int,db:Session=Depends(get_db),user=Depends(current_user)):return row(runs.get_run(db,id))
@router.post('/runs',status_code=201)
def create(data:RunInput,db:Session=Depends(get_db),user=Depends(writers)):return runs.create_run(db,data,user)
@router.get('/topics')
def topics(db:Session=Depends(get_db),user=Depends(current_user)):return profiles.list_profiles(db)
@router.patch('/topics/{id}')
def edit(id:int,data:ProfilePatch,db:Session=Depends(get_db),user=Depends(writers)):return profiles.patch_profile(db,id,data,user)
