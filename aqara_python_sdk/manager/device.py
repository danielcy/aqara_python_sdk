from typing import List

from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.enums.device_type import DeviceType
from aqara_python_sdk.enums.query import QueryType
from aqara_python_sdk.models.client import Device


class DeviceManager:
    def __init__(self, client: AqaraClient, devices: List[Device]):
        self.client = client
        self.devices = devices

    def find_device_by_did(self, did: str) -> Device | None:
        for device in self.devices:
            if device.did == did:
                return device
        return None

    def find_devices_by_name(self, name: str, query_type: QueryType = QueryType.ACCURATE) -> List[Device]:
        if query_type == QueryType.ACCURATE:
            return [device for device in self.devices if device.device_name == name]
        elif query_type == QueryType.FUZZY:
            return [device for device in self.devices if name in device.device_name]

    def find_devices_by_type(self, device_type: DeviceType) -> List[Device]:
        return [device for device in self.devices if self.get_device_type(device) == device_type]

    @staticmethod
    def get_device_type(device: Device) -> DeviceType:
        model_mark = device.model.split(".")[1]
        if model_mark == "light":
            return DeviceType.LIGHT
        elif model_mark == "switch":
            return DeviceType.SWITCH
        elif model_mark == "curtain":
            return DeviceType.CURTAIN
        return DeviceType.UNSUPPORTED