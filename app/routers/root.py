"""
Routes for root API
"""

from fastapi import APIRouter
from .config import URL_PREFIX

router = APIRouter(
    prefix=f"{URL_PREFIX}",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root():
    """
    Index API Route (GET)
    """

    return {"message": "running"}
