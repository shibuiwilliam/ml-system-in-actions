from fastapi import APIRouter
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()


@router.get("")
def health():
    return {"health": "ok"}