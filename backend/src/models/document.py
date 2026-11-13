from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Text,ForeignKey,UniqueConstraint
from src.config.database import Base
class TokenDocument(Base):
 __tablename__='token_documents'
 __table_args__=(UniqueConstraint('corpus_id','reference'),)
 id:Mapped[int]=mapped_column(primary_key=True)
 corpus_id:Mapped[int]=mapped_column(ForeignKey('corpora.id'))
 reference:Mapped[str]=mapped_column(String(80))
 title:Mapped[str]=mapped_column(String(120))
 tokens_text:Mapped[str]=mapped_column(Text)
