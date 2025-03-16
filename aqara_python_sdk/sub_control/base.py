from typing import List

from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.models.client import Device
from aqara_python_sdk.models.contract import ControlDeviceRequest, ControlDeviceResourceRequest, \
    QueryDeviceResourceRequest


class BaseControl:
    def __init__(self, client: AqaraClient, device: Device):
        self.client = client
        self.device = device

    def name(self):
        return self.device.device_name

    def device_id(self):
        return self.device.did

    def _check_resource_support(self, resource_id: str):
        resources = self.client.query_model_resource(self.device.model, resource_id)
        return len(resources) > 0 and resources[0].access != 0

    # 该方法的作用是检查资源是否支持，如果支持则返回资源id，否则抛出异常
    def _check_resources_either_support(self, resource_ids: List[str]) -> str | None:
        resources = self.client.query_model_resource(self.device.model)
        for resource in resources:
            if resource.resource_id in resource_ids and resource.access != 0:
                return resource.resource_id
        return None

    def _update_single_resource(self, resource_id: str, value: str):
        if self._check_resource_support(resource_id):
            self.client.control_devices([
                ControlDeviceRequest(
                    device_id=self.device.did,
                    resources=[
                        ControlDeviceResourceRequest(resource_id=resource_id, value=value)
                    ]
                )
            ])
        else:
            raise Exception(f"Device {self.device.device_name} does not support {resource_id}")

    def _update_either_resource(self, resource_ids: List[str], value: str):
        support = self._check_resources_either_support(resource_ids)
        if support:
            self.client.control_devices([
                ControlDeviceRequest(
                    device_id=self.device.did,
                    resources=[
                        ControlDeviceResourceRequest(resource_id=support, value=value)
                    ]
                )
            ])
        else:
            raise Exception(f"Device {self.device.device_name} does not support any of {resource_ids}")

    def _get_single_resource_value(self, resource_id: str):
        if self._check_resource_support(resource_id):
            status = self.client.query_device_resource_latest_status([
                QueryDeviceResourceRequest(
                    device_id=self.device.did,
                    resource_ids=[resource_id]
                )
            ])
            # 判断字典不为空
            if status and status[self.device.did] and len(status[self.device.did]) > 0:
                return status[self.device.did][0].value

        raise Exception(f"Device {self.device.device_name} does not support {resource_id}")

    def _get_either_resource_value(self, resource_ids: List[str]):
        support = self._check_resources_either_support(resource_ids)
        if support:
            status = self.client.query_device_resource_latest_status([
                QueryDeviceResourceRequest(
                    device_id=self.device.did,
                    resource_ids=[support]
                )
            ])
            # 判断字典不为空
            if status and status[self.device.did] and len(status[self.device.did]) > 0:
                return status[self.device.did][0].value

        raise Exception(f"Device {self.device.device_name} does not support any of {resource_ids}")

