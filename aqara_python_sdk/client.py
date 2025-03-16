import random
import time
from typing import List, Dict

import requests

from aqara_python_sdk.models.base import PagingResponse
from aqara_python_sdk.models.client import Device, Resource, ResourceStatus, Position, Scene
from aqara_python_sdk.models.contract import QueryDeviceResourceRequest, ControlDeviceRequest, BaseResponse
from aqara_python_sdk.utils.sign import sign


class AqaraClient:
    def __init__(self, app_id, key_id, app_key, token=None, refresh_token=None, account=None, account_type=0):
        self.__app_id = app_id
        self.__key_id = key_id
        self.__app_key = app_key
        self.__token = token
        self._account = account
        self._account_type = account_type
        self.__refresh_token = refresh_token

    def query_devices(self, dids=None, position_id=None, page_num=1, page_size=50) -> PagingResponse[Device]:
        intent = "query.device.info"
        data = {
            "dids": dids,
            "positionId": position_id,
            "pageNum": page_num,
            "pageSize": page_size
        }
        response = self._post(intent, data)
        data_list = response["result"]["data"]
        total = response["result"]["totalCount"]
        result = []
        for data in data_list:
            result.append(Device(data))
        return PagingResponse(result, total)

    def query_positions(self, parent_position_ids: str | None = None, page_num=1, page_size=50) -> PagingResponse[Position]:
        intent = "query.position.info"
        data = {
            "parentPositionId": parent_position_ids,
            "pageNum": page_num,
            "pageSize": page_size
        }
        response = self._post(intent, data)
        data_list = response["result"]["data"]
        total = response["result"]["totalCount"]
        result = []
        for data in data_list:
            result.append(Position(data))
        return PagingResponse(result, total)

    def query_scenes_by_position(self, position_id: str | None = None, page_num=1, page_size=50) -> PagingResponse[Scene]:
        intent = "query.scene.listByPositionId"
        data = {
            "positionId": position_id,
            "pageNum": page_num,
            "pageSize": page_size
        }
        response = self._post(intent, data)
        data_list = response["result"]["data"]
        total = response["result"]["totalCount"]
        result = []
        for data in data_list:
            result.append(Scene(data))
        return PagingResponse(result, total)

    def query_model_resource(self, model, resource_id=None) -> List[Resource]:
        intent = "query.resource.info"
        data = {
            "model": model,
            "resourceId": resource_id
        }
        response = self._post(intent, data)
        data_list = response["result"]
        result = []
        for data in data_list:
            result.append(Resource(data))
        return result

    def query_device_resource_latest_status(self, request: List[QueryDeviceResourceRequest]) \
            -> Dict[str, List[ResourceStatus]]:
        intent = "query.resource.value"
        data = {
            "resources": list(map(lambda x: {"subjectId": x.device_id, "resourceIds": x.resource_ids}, request))
        }
        response = self._post(intent, data)
        data_list = response["result"]
        result = {}
        for data in data_list:
            if data["subjectId"] not in result:
                result[data["subjectId"]] = []
            result[data["subjectId"]].append(ResourceStatus(data))

        return result

    def control_devices(self, request: List[ControlDeviceRequest]) -> BaseResponse:
        intent = "write.resource.device"
        data = list(map(lambda x: {"subjectId": x.device_id,
                                             "resources": list(map(lambda y: {
                                                 "resourceId": y.resource_id,
                                                 "value": y.value}, x.resources))},
                    request))
        response = self._post(intent, data)
        if response["message"] != "Success":
            return BaseResponse(False, response["message"])
        return BaseResponse(True, response["message"])

    def execute_scene(self, scene_id: str) -> BaseResponse:
        intent = "config.scene.run"
        data = {
            "sceneId": scene_id
        }
        response = self._post(intent, data)
        if response["message"] != "Success":
            return BaseResponse(False, response["message"])
        return BaseResponse(True, response["message"])

    def update_device_name(self, did: str, name: str) -> BaseResponse:
        intent = "config.device.updateName"
        data = {
            "did": did,
            "name": name
        }
        response = self._post(intent, data)
        if response["message"] != "Success":
            return BaseResponse(False, response["message"])
        return BaseResponse(True, response["message"])

    def send_auth_code(self,
                       account=None,
                       account_type=None,
                       token_validity='30d'):

        intent = "config.auth.getAuthCode"
        data = {
            "account": account if account is not None else self._account,
            "accountType": account_type if account_type is not None else self._account_type,
            "accessTokenValidity": token_validity
        }
        response = self._post(intent, data, False)
        return response["result"]["authCode"]

    def get_token(self, auth_code, account=None, account_type=None):
        intent = "config.auth.getToken"
        data = {
            "account": account if account is not None else self._account,
            "authCode": auth_code,
            "accountType": account_type if account_type is not None else self._account_type
        }
        response = self._post(intent, data, False)
        self.__token = response["result"]["accessToken"]
        self.__refresh_token = response["result"]["refreshToken"]
        return response["result"]

    def refresh_token(self, refresh_token: str = None):
        if refresh_token is None:
            refresh_token = self.__refresh_token
        if refresh_token is None:
            raise Exception("Refresh token is required.")
        intent = "config.auth.refreshToken"
        data = {
            "refreshToken": refresh_token
        }
        response = self._post(intent, data, False)
        self.__token = response["result"]["accessToken"]
        return response["result"]

    def _post(self, intent, data, with_token=True):
        headers = self.__make_headers(with_token)
        request = {
            "intent": intent,
            "data": data
        }
        response = requests.post(f"https://open-cn.aqara.com/v3.0/open/api", headers=headers, json=request)
        result = response.json()
        if result["message"] != "Success":
            raise Exception(result["message"])
        return result

    def __make_headers(self, with_token=True):
        if with_token and not hasattr(self, "_AqaraClient__token"):
            raise Exception("Token is required, please fetch token first.")
        timestamp = str(int(time.time()) * 1000)
        nonce = str(random.randint(100000, 999999))
        return {
            "Accesstoken": self.__token if with_token else None,
            "Appid": self.__app_id,
            "Keyid": self.__key_id,
            "Nonce": nonce,
            "Time": timestamp,
            "Sign": sign(self.__token, self.__app_id, self.__key_id, self.__app_key, timestamp, nonce) if with_token else
            sign(None, self.__app_id, self.__key_id, self.__app_key, timestamp, nonce),
            "Lang": "zh"
        }