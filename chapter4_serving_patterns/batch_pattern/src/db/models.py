from logging import getLogger

from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import JSON

logger = getLogger(__name__)

from src.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    values = Column(
        JSON,
        nullable=False,
    )
    prediction = Column(
        JSON,
        nullable=True,
    )
    created_datetime = Column(
        TIMESTAMP,
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_datetime = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )


def create_tables(engine, checkfirst: bool = True):
    logger.info("Initialize table")
    Base.metadata.create_all(engine, checkfirst=checkfirst)
