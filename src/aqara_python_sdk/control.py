import logging
from typing import List

from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.manager.device import DeviceManager
from aqara_python_sdk.manager.position import PositionManager
from aqara_python_sdk.manager.scene import SceneManager
from aqara_python_sdk.models.client import Device, Position, Scene
from aqara_python_sdk.query.control import ControlQuery


class AqaraController:
    def __init__(self, client: AqaraClient):
        self.client = client
        self.__devices: List[Device] = []
        self.__positions: List[Position] = []
        self.__scenes: List[Scene] = []

    def load_data(self) -> None:
        logging.info("AqaraController loading all devices")
        page_size = 100
        paging_res = self.client.query_devices(page_size=page_size)
        if paging_res.total <= page_size:
            self.__devices = paging_res.data
        else:
            devices = paging_res.data
            for i in range(2, paging_res.total // page_size + 1):
                paging_res = self.client.query_devices(page_num=i, page_size=page_size)
                devices += paging_res.data
            self.__devices = devices
        logging.info(f"AqaraController loaded all devices. device count: {len(self.__devices)}")

        logging.info("AqaraController loading all positions")
        # 获取顶层位置
        position_res = self.client.query_positions(page_size=page_size)
        if position_res.total <= page_size:
            positions = position_res.data
        else:
            positions = position_res.data
            for i in range(2, position_res.total // page_size + 1):
                position_res = self.client.query_positions(page_num=i, page_size=page_size)
                positions += position_res.data
            positions = positions
        # 进一步获取每一个顶层位置的下层位置
        sub_positions = []
        for position in positions:
            sub_position_res = self.client.query_positions(parent_position_ids=position.position_id, page_size=page_size)
            if sub_position_res.total <= page_size:
                single_sub_positions = sub_position_res.data
            else:
                single_sub_positions = sub_position_res.data
                for i in range(2, sub_position_res.total // page_size + 1):
                    sub_position_res = self.client.query_positions(parent_position_ids=position.position_id, page_num=i,
                                                                  page_size=page_size)
                    single_sub_positions += sub_position_res.data
            sub_positions += single_sub_positions
        positions += sub_positions
        self.__positions = positions
        logging.info(f"AqaraController loaded all positions. position count: {len(self.__positions)}")

        logging.info("AqaraController loading all scenes")
        scene_res = self.client.query_scenes_by_position(page_size=page_size)
        if scene_res.total <= page_size:
            self.__scenes = scene_res.data
        else:
            scenes = scene_res.data
            for i in range(2, scene_res.total // page_size + 1):
                scene_res = self.client.query_scenes_by_position(page_num=i, page_size=page_size)
                scenes += scene_res.data
            self.__scenes = scenes
        logging.info(f"AqaraController loaded all scenes. scene count: {len(self.__scenes)}")

    def query_device(self):
        return ControlQuery(self.client, self.position(), self.device())

    def device(self) -> DeviceManager:
        return DeviceManager(self.client, self.__devices)

    def position(self) -> PositionManager:
        return PositionManager(self.client, self.__positions)

    def scene(self) -> SceneManager:
        return SceneManager(self.client, self.__scenes)
