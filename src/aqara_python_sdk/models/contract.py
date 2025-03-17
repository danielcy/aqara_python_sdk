from dataclasses import dataclass
from typing import List


@dataclass
class QueryDeviceResourceRequest:
    device_id: str
    resource_ids: List[str]


@dataclass
class ControlDeviceResourceRequest:
    resource_id: str
    value: str


@dataclass
class ControlDeviceRequest:
    device_id: str
    resources: List[ControlDeviceResourceRequest]


@dataclass
class BaseResponse:
    success: bool
    message: str
