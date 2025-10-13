from fastapi import APIRouter

from .categories import router as categories_router
from .users import router as users_router

v1_router = APIRouter(prefix="/v1", tags=["v1"])
v1_router.include_router(users_router)
v1_router.include_router(categories_router)
