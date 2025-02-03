from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect
from starlette.responses import FileResponse
from user_agents import parse
from configs.settings import get_settings

from apps.page.schemas import Device
from apps.page.websocket_manager import ConnectionResultPageManager

page_router = APIRouter(prefix="", tags=["Page"])
templates = Jinja2Templates(directory="templates")
runtime_settings = get_settings()


@page_router.get("/")
async def index_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"is_debug": runtime_settings.IS_DEBUG},
    )


@page_router.get("/apple-touch-icon-precomposed.png")
async def apple_touch_icon_precomposed(
    request: Request,
):
    return FileResponse("static/apple-touch-icon-precomposed.png")


@page_router.get("/apple-touch-icon.png")
async def apple_touch_icon():
    return FileResponse("static/apple-touch-icon.png")


@page_router.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


@page_router.get("/result")
async def result_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"is_debug": runtime_settings.IS_DEBUG},
    )


result_page_manager = ConnectionResultPageManager()


@page_router.websocket("/ws/result")
async def websocket_result_endpoint(websocket: WebSocket):
    await result_page_manager.connect(websocket)
    await result_page_manager.send_personal_message(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        result_page_manager.disconnect(websocket)


@page_router.websocket("/ws/scan/{connect_id}")
async def websocket_scan_endpoint(websocket: WebSocket, connect_id: str):
    await websocket.accept()

    device = Device(
        name=str(parse(websocket.headers.get("user-agent"))), connect_id=connect_id
    )
    await result_page_manager.create_connected_device(device)
    try:
        while True:
            code = await websocket.receive_text()
            await result_page_manager.broadcast(code)
    except WebSocketDisconnect:
        await result_page_manager.destroy_connected_device(device)
