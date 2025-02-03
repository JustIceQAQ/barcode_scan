import datetime

from pydantic import BaseModel, Field
from typing import Literal

from helpers.utils.datetime.helper import datetime_now


class Device(BaseModel):
    name: str
    connect_id: str


class Barcode(BaseModel):
    code: str
    create_datetime: datetime.datetime = Field(default_factory=datetime_now)


class DeviceList(BaseModel):
    devices: list[Device]

class BarcodeDict(BaseModel):
    barcode: Barcode

class ResultType(BaseModel):
    type: Literal["device", "data"]
    data: Device
