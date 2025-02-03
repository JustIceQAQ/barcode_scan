from fastapi import APIRouter
from fastapi.requests import Request

from configs.settings import get_settings
from .sechemas import GetStatusResponse
from user_agents import parse

status_router = APIRouter(prefix="/status", tags=["Status"])

runtime_settings = get_settings()


@status_router.get("/", response_model=GetStatusResponse)
async def get_status(request: Request):
    parse_result = parse(request.headers.get("user-agent"))
    return GetStatusResponse(
        runserver_datetime=runtime_settings.RUNSERVER_DATETIME, device=str(parse_result)
    )
