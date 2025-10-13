from fastapi import APIRouter

from app.api.v1 import v1_router

api_router = APIRouter(prefix="/api", tags=["api"])
api_router.include_router(v1_router)

# Si en el futuro agregas v2:
# from app.api.v2 import v2_router
# api_router.include_router(v2_router)
