from fastapi import APIRouter

from .users import router as users_router

v1_router = APIRouter(prefix="/v1", tags=["v1"])
v1_router.include_router(users_router)
