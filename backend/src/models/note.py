from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,JSON,ForeignKey,DateTime
from datetime import datetime,timezone
from src.config.database import Base
class EditorialNote(Base):
 __tablename__='editorial_notes'
 id:Mapped[int]=mapped_column(primary_key=True)
 run_id:Mapped[int]=mapped_column(ForeignKey('topic_runs.id'))
 name:Mapped[str]=mapped_column(String(100))
 profile_ids:Mapped[list]=mapped_column(JSON)
 profile_snapshot:Mapped[list]=mapped_column(JSON)
 interpretation:Mapped[str]=mapped_column(String(700))
 next_step:Mapped[str]=mapped_column(String(500))
 status:Mapped[str]=mapped_column(String(20),default='draft')
 review_note:Mapped[str]=mapped_column(String(500),default='')
 creator_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
 created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
