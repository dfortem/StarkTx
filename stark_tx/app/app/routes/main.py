from fastapi import APIRouter

from . import index, transaction

router = APIRouter()
router.include_router(index.router)
router.include_router(transaction.router)
