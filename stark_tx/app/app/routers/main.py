from fastapi import APIRouter

from . import static

router = APIRouter()
router.include_router(static.router)
