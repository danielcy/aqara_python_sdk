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

    client = AqaraClient(app_id, key_id, app_key, account="13482892612")

    client.send_auth_code(token_validity='1y')
    # 输入手机收到的验证码
    code = input("Please input the code: ")
    token_res = client.get_token(code)
    token = token_res['accessToken']
    refresh_token = token_res['refreshToken']
    print(f"Token: {token}")
