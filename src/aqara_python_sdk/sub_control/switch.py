import logging

from aqara_python_sdk.sub_control.base import BaseControl


class SwitchControl(BaseControl):

    def __init__(self, client, device):
        super().__init__(client, device)

    def is_on(self, channel_index: int):
        if channel_index > 2:
            raise Exception("Switch only supports 3 channels")
        resource_id = f"4.{channel_index + 1}.85"
        value = self._get_single_resource_value(resource_id)
        return value == "1"

    def turn_on(self, channel_index: int):
        if channel_index > 2:
            raise Exception("Switch only supports 3 channels")
        resource_id = f"4.{channel_index + 1}.85"
        logging.info(f"Turning on switch {self.device.device_name} channel {channel_index}")
        self._update_single_resource(resource_id, "1")

    def turn_off(self, channel_index: int):
        if channel_index > 2:
            raise Exception("Switch only supports 3 channels")
        resource_id = f"4.{channel_index + 1}.85"
        logging.info(f"Turning off switch {self.device.device_name} channel {channel_index}")
        self._update_single_resource(resource_id, "0")
