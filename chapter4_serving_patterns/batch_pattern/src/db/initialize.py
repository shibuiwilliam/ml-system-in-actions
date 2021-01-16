from logging import getLogger

from src.configurations import PlatformConfigurations
from src.db import cruds, models, schemas
from src.db.database import get_context_db

logger = getLogger(__name__)


def initialize_database(engine, checkfirst: bool = True):
    models.create_tables(engine=engine, checkfirst=checkfirst)
    with get_context_db() as db:
        sample_data = PlatformConfigurations.sample_data
        items = [schemas.ItemBase(values=values) for values in sample_data]
        cruds.register_items(db=db, items=items, commit=True)
