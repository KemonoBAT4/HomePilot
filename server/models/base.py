import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Enum
from sqlalchemy.orm import relationship

from database import Base

class BaseModel(Base):
    __abstract__ = True

    id         = Column(String  , unique=True , primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, unique=False, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now(tz=timezone.utc)
    # #enddef __init__
# #endclass BaseModel