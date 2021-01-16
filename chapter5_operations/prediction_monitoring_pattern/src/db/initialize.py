from logging import getLogger

from src.db.database import Base

logger = getLogger(__name__)


def create_tables(engine, checkfirst: bool = True):
    logger.info("Initialize tables if not exist.")
    Base.metadata.create_all(engine, checkfirst=checkfirst)


def initialize_database(engine, checkfirst: bool = True):
    logger.info("Initialize tables")
    create_tables(engine=engine, checkfirst=checkfirst)
