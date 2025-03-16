import logging
from typing import List

from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.manager.device import DeviceManager
from aqara_python_sdk.manager.position import PositionManager
from aqara_python_sdk.enums.device_type import DeviceType
from aqara_python_sdk.enums.query import QueryType
from aqara_python_sdk.models.client import Device, Position
from aqara_python_sdk.sub_control.light import LightControl
from aqara_python_sdk.sub_control.switch import SwitchControl


class FinalQuery:
    def __init__(self,
                 client: AqaraClient,
                 position: PositionManager,
                 device: DeviceManager,
                 devices: List[Device],
                 positions: List[Position] | None = None,
                 device_type: DeviceType = DeviceType.ANY,
                 ):
        self.__client = client
        self.__position: PositionManager = position
        self.__device: DeviceManager = device
        self.__positions: List[Position] | None = positions
        self.__type: DeviceType = device_type
        self.__devices: List[Device] = devices

    def query(self) -> List[Device]:
        return self.__devices

    def light(self) -> List[LightControl]:
        if self.__type in [DeviceType.LIGHT, DeviceType.ANY]:
            devices = self.__devices
            lights = list(map(lambda x: LightControl(self.__client, x), devices))
            return lights
        else:
            logging.warning("Only light devices can be controlled by light manager")
            return []

    def switch(self) -> List[SwitchControl]:
        if self.__type in [DeviceType.SWITCH, DeviceType.ANY]:
            devices = self.__devices
            switches = list(map(lambda x: SwitchControl(self.__client, x), devices))
            return switches
        else:
            logging.warning("Only switch devices can be controlled by switch manager")
            return []


class DeviceQuery:
    def __init__(self,
                 client: AqaraClient,
                 position: PositionManager,
                 device: DeviceManager,
                 positions: List[Position] | None = None,
                 device_type: DeviceType = DeviceType.ANY):
        self.__client = client
        self.__position: PositionManager = position
        self.__device: DeviceManager = device
        self.__positions: List[Position] | None = positions
        self.__type: DeviceType = device_type

    def device_name(self, name, query_type: QueryType = QueryType.ACCURATE) -> FinalQuery:
        devices = self.__filter(self.__device.find_devices_by_name(name, query_type))
        return FinalQuery(self.__client, self.__position, self.__device, devices, self.__positions, self.__type)

    def device_id(self, id: str) -> FinalQuery:
        device = self.__device.find_device_by_did(id)
        devices = self.__filter([device] if device else [])
        return FinalQuery(self.__client, self.__position, self.__device, devices, self.__positions, self.__type)

    def device_any(self) -> FinalQuery:
        devices = self.__filter(self.__device.devices)
        return FinalQuery(self.__client, self.__position, self.__device, devices, self.__positions, self.__type)

    def __filter(self, devices: List[Device]):
        if self.__positions:
            position_ids = list(map(lambda x: x.position_id, self.__positions))
            devices = list(filter(lambda x: x.position_id in position_ids, devices))
        if self.__type != DeviceType.ANY:
            devices = list(filter(lambda x: self.__device.get_device_type(x) == self.__type, devices))
        return devices


class DeviceTypeQuery:
    def __init__(self,
                 client: AqaraClient,
                 position: PositionManager,
                 device: DeviceManager,
                 positions: List[Position] | None = None):
        self.__client = client
        self.__position: PositionManager = position
        self.__device: DeviceManager = device
        self.__positions: List[Position] | None = positions

    def device_type(self, type: DeviceType) -> DeviceQuery:
        return DeviceQuery(self.__client, self.__position, self.__device, self.__positions, type)

    def device_type_any(self) -> DeviceQuery:
        return DeviceQuery(self.__client, self.__position, self.__device, self.__positions)


class ControlQuery:

    def __init__(self,
                 client: AqaraClient,
                 position: PositionManager,
                 device: DeviceManager):
        self.__client = client
        self.__position: PositionManager = position
        self.__device: DeviceManager = device

    def position_name(self, name, query_type: QueryType = QueryType.ACCURATE) -> DeviceTypeQuery:
        positions = self.__position.find_positions_by_name(name, query_type)
        return DeviceTypeQuery(self.__client, self.__position, self.__device, positions)

    def position_id(self, id: str) -> DeviceTypeQuery:
        position = self.__position.find_position_by_id(id)
        return DeviceTypeQuery(self.__client, self.__position, self.__device, [position])

    def position_any(self) -> DeviceTypeQuery:
        return DeviceTypeQuery(self.__client, self.__position, self.__device)