from datetime import datetime, timezone, time

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    func,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Float,
    JSON,
    ColumnElement,
    Numeric,
    Index,
)
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

    @property
    def is_due(self) -> bool | ColumnElement[bool]:
        """Check if the event should run again based on frequency."""
        if self.last_run_at is None:
            return True  # If it never ran before, it's due
        return (datetime.now(timezone.utc) - self.last_run_at).total_seconds() >= self.frequency


class EventAverages(Base):
    __tablename__ = "event_stats_daily"
    __table_args__ = (UniqueConstraint("eid", "date"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    eid = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(
        DateTime,
        default=datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc),
        index=True,
    )
    avg_response_time = Column(Numeric, default=0)
    uptime = Column(Float, default=100)
    count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted = Column(Boolean, default=False)


class EventLogs(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    eid = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    success = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    run_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted = Column(Boolean, default=False)
    time_took = Column(Numeric, default=0)
    error = Column(Text, default=None, nullable=True)


class LastEventRuns(Base):
    __tablename__ = "latest_events"
    __table_args__ = (Index("idx_last_10_event_runs_eid_run_at", "eid", "run_at"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    eid = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    time_took = Column(Numeric, nullable=False)
    run_at = Column(DateTime(timezone=True), server_default=func.now())
