from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import JSON
from src.db.database import Base


class PredictionLog(Base):
    __tablename__ = "prediction_log"

    log_id = Column(
        String(255),
        primary_key=True,
    )
    log = Column(
        JSON,
        nullable=False,
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class OutlierLog(Base):
    __tablename__ = "outlier_log"

    log_id = Column(
        String(255),
        primary_key=True,
    )
    log = Column(
        JSON,
        nullable=False,
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
