from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,JSON,ForeignKey,UniqueConstraint
from sqlalchemy.dialects.mysql import DOUBLE
from src.config.database import Base
class TopicProfile(Base):
 __tablename__='topic_profiles'
 __table_args__=(UniqueConstraint('run_id','topic_index'),)
 id:Mapped[int]=mapped_column(primary_key=True)
 run_id:Mapped[int]=mapped_column(ForeignKey('topic_runs.id'))
 topic_index:Mapped[int]=mapped_column()
 label:Mapped[str]=mapped_column(String(100))
 editor_note:Mapped[str]=mapped_column(String(500),default='')
 weights:Mapped[list]=mapped_column(JSON)
 mean_similarity:Mapped[float]=mapped_column(DOUBLE(asdecimal=False))
