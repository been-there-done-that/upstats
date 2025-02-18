from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Text, DateTime, func, Boolean, ForeignKeyConstraint, UniqueConstraint
from cuid2 import cuid_wrapper


cuid = cuid_wrapper()


class Base(DeclarativeBase):
    pass


class Events(Base):
    __tablename__ = "events"
    __table_args__ = (UniqueConstraint("url", "method", "frequency", "rid"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    rid = Column(Text, nullable=False, default=cuid, unique=True)
    name = Column(Text, nullable=False, default="")
    url = Column(Text, nullable=False)
    frequency = Column(Integer, nullable=False)
    method = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted = Column(Boolean, default=False)
    last_run_at = Column(DateTime(timezone=True), nullable=True)
