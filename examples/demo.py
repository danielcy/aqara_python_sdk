import json
import logging
import os

from dotenv import load_dotenv

from aqara_python_sdk.control import AqaraController
from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.enums.device_type import DeviceType
from aqara_python_sdk.utils.json_encoder import DefaultEncoder

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)
load_dotenv(verbose=True)

if __name__ == "__main__":
    app_id = os.getenv("AQARA_APP_ID")
    key_id = os.getenv("AQARA_KEY_ID")
    app_key = os.getenv("AQARA_APP_KEY")

    client = AqaraClient(app_id, key_id, app_key, account="13482892612", token="SOME TOKEN")

    # client.send_auth_code()
    # token_res = client.get_token("805859")
    # print(token_res)

    controller = AqaraController(client)
    controller.load_data()
    # print(json.dumps(controller.find_devices_by_name("开关", query_type=QueryType.FUZZY),
    #                  cls=DefaultEncoder, indent=4, ensure_ascii=False))
    light_control = controller.query_device().position_name("客厅").device_type(DeviceType.LIGHT).device_name("走道射灯1").light()[0]
    print(light_control.is_on())

    print(controller.scene().list_scene_names())

