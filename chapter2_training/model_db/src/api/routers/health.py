from logging import getLogger

from fastapi import APIRouter

logger = getLogger(__name__)
router = APIRouter()


@router.get("")
def health():
    return {"health": "ok"}
