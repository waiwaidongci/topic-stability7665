from sqlalchemy import select,func
from fastapi import HTTPException
from src.models import Corpus,TokenDocument
from src.utils.serialize import row
from .audit import record
def list_corpora(db):return [dict(row(c),document_count=db.scalar(select(func.count()).select_from(TokenDocument).where(TokenDocument.corpus_id==c.id))) for c in db.scalars(select(Corpus).order_by(Corpus.id))]
def list_documents(db,corpus_id=None):
 q=select(TokenDocument).order_by(TokenDocument.reference)
 if corpus_id is not None:q=q.where(TokenDocument.corpus_id==corpus_id)
 return [row(x) for x in db.scalars(q)]
def create_corpus(db,data,user):
 if db.scalar(select(Corpus).where(Corpus.name==data.name)):raise HTTPException(409,'语料名称已存在')
 obj=Corpus(**data.model_dump(exclude={'documents'}));db.add(obj);db.flush();db.add_all([TokenDocument(corpus_id=obj.id,**d.model_dump()) for d in data.documents]);db.commit();record(db,user.email,'corpus.import',{'corpus_id':obj.id,'documents':len(data.documents)});return row(obj)
def patch_document(db,id,data,user):
 obj=db.get(TokenDocument,id)
 if not obj:raise HTTPException(404,'文档不存在')
 obj.title=data.title;obj.tokens_text=data.tokens_text;db.commit();record(db,user.email,'document.edit',{'document_id':id});return row(obj)
