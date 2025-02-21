from datetime import datetime, timezone, time

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Text, DateTime, func, Boolean, ForeignKey, UniqueConstraint, Float, JSON
from sqlalchemy.dialects.postgresql import JSONB
from cuid2 import cuid_wrapper


cuid = cuid_wrapper()


class Base(DeclarativeBase):
    pass


class Events(Base):
    __tablename__ = "events"
    __table_args__ = (UniqueConstraint("url", "method", "frequency", "eid"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    eid = Column(Text, nullable=False, default=cuid, unique=True)
    name = Column(Text, nullable=False, default="")
    url = Column(Text, nullable=False)
    frequency = Column(Integer, nullable=False)
    method = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted = Column(Boolean, default=False)
    last_run_at = Column(DateTime(timezone=True), nullable=True)


class EventAverages(Base):
    __tablename__ = "event_stats_daily"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(Text, nullable=False, default=cuid, unique=True)
    eid = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(DateTime, default=datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc))
    avg_response_time = Column(Integer, default=0)
    uptime = Column(Float, default=100)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted = Column(Boolean, default=False)


class EventLogs(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    eid = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    response = Column(JSONB, default={})
    status_code = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted = Column(Boolean, default=False)
