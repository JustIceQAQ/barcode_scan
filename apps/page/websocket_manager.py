import asyncio

from starlette.websockets import WebSocket

from apps.page.schemas import Device, DeviceList, BarcodeDict, Barcode, ResultType


class ConnectionResultPageManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.connect_device: dict[str, Device] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, websocket: WebSocket):
        await websocket.send_json(
            DeviceList(devices=list(self.connect_device.values())).model_dump_json()
        )

    async def broadcast(self, code: str):
        await asyncio.gather(
            *[
                connection.send_json(
                    BarcodeDict(barcode=Barcode(code=code)).model_dump_json()
                )
                for connection in self.active_connections
            ]
        )

    async def get_all_connected_device(self):
        serialized_data = DeviceList(devices=list(self.connect_device.values()))
        await asyncio.gather(
            *[
                connection.send_json(serialized_data.model_dump_json())
                for connection in self.active_connections
            ]
        )

    async def create_connected_device(self, device: Device):
        new_device = ResultType(type="device", data=device)
        self.connect_device[new_device.data.connect_id] = new_device.data
        await self.get_all_connected_device()

    async def destroy_connected_device(self, device: Device):
        del self.connect_device[device.connect_id]
        await self.get_all_connected_device()
