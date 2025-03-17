import logging

from aqara_python_sdk.consts import ResourceIdConsts
from aqara_python_sdk.sub_control.base import BaseControl


class LightControl(BaseControl):
    def __init__(self, client, device):
        super().__init__(client, device)

    def is_on(self):
        value = self._get_single_resource_value(ResourceIdConsts.POWER_STATUS)
        return value == "1"

    def turn_on(self):
        logging.info(f"Turning on light {self.device.device_name}")
        self._update_single_resource(ResourceIdConsts.POWER_STATUS, "1")

    def turn_off(self):
        logging.info(f"Turning off light {self.device.device_name}")
        self._update_single_resource(ResourceIdConsts.POWER_STATUS, "0")

    def get_brightness(self):
        value = self._get_either_resource_value([ResourceIdConsts.LIGHT_LEVEL, ResourceIdConsts.LIGHT_LEVEL_V2])

        return int(value)

    def set_brightness(self, value: int):
        # 亮度值,取值范围0~100
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        logging.info(f"Setting brightness of light {self.device.device_name} to {value}")
        self._update_either_resource(
            [ResourceIdConsts.LIGHT_LEVEL, ResourceIdConsts.LIGHT_LEVEL_V2],
            str(value)
        )

    def get_color_temperature(self):
        value = self._get_either_resource_value([ResourceIdConsts.COLOR_TEMPERATURE, ResourceIdConsts.COLOR_TEMPERATURE_V2])
        return 1000000 // int(value)

    def set_color_temperature(self, value: int):
        # 色温值,取值为微倒度，即1000000/色温度。比如5000K，则色温值为1000000/5000=200.色温度范围2700K~6500K
        logging.info(f"Setting color temperature of light {self.device.device_name} to {value}K")
        real_value = 1000000 // value
        self._update_either_resource(
            [ResourceIdConsts.COLOR_TEMPERATURE, ResourceIdConsts.COLOR_TEMPERATURE_V2],
            str(real_value)
        )
