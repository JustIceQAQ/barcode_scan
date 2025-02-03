from fastapi import APIRouter

from apps.page.api import page_router
from apps.status.api import status_router

apis_router = APIRouter(prefix="/api")
apis_router.include_router(status_router)
