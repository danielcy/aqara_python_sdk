import logging
import os

from dotenv import load_dotenv

from aqara_python_sdk import AqaraClient, AqaraController
from aqara_python_sdk.enums.device_type import DeviceType

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)
load_dotenv(verbose=True)

if __name__ == "__main__":
    app_id = os.getenv("AQARA_APP_ID")
    key_id = os.getenv("AQARA_KEY_ID")
    app_key = os.getenv("AQARA_APP_KEY")

    client = AqaraClient(app_id, key_id, app_key, account="Your Aqara Username")
    # 会向你的手机发送一条验证码, 后续获取到Token的有效期可以自行指定，支持1~24h, 1~30d, 1~10y, 默认为30d
    client.send_auth_code(token_validity='30d')
    # 输入手机收到的验证码
    code = input("Please input the code: ")
    token_res = client.get_token(code)
    token = token_res['accessToken']
    refresh_token = token_res['refreshToken']
    print(f"Token: {token}")

    controller = AqaraController(client)
    controller.load_data()

    controller = AqaraController(client)
    # 加载所有数据，如果数据在其他地方有更新（如在Aqara Home APP中更新了），需要重新调用一次此方法获取最新的数据
    controller.load_data()

    # 查询指定设备
    devices = controller.query_device().position_name("客厅").device_type(DeviceType.LIGHT).device_name(
        "我的射灯").query()

    # 查询灯设备
    light_controls = controller.query_device().position_name("客厅").device_type(DeviceType.LIGHT).device_name(
        "我的射灯").light()

    # 查询场景
    all_scene_names = controller.scene().list_scene_names()
    my_scene = controller.scene().get_scene_by_name("我的场景")

    # 获取灯设备
    my_light = controller.query_device().position_name("客厅").device_type(DeviceType.LIGHT).device_name("我的射灯").light()[0]
    # 执行灯操作
    if not my_light.is_on():
        my_light.turn_on()
    my_light.set_brightness(50)
    my_light.set_color_temperature(4000)

    # 执行场景
    controller.scene().execute_scene("我的场景")

