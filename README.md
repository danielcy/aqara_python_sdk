## 项目简介
本SDK为Aqara开放平台的API的Python封装版本，除了对API进行封装外，还提供了一层控制层，用于简化对设备的查询和操作。

## 使用说明

### 准备工作
1. 默认你已经准备好了Aqara设备，注册了Aqara Home账号，并将它们接入了Aqara Home App
2. 进入[Aqara开放平台](https://developer.aqara.com/), 使用你的Aqara Home账号登录，并进入控制台
3. 在项目管理页面中，创建一个新项目，获取到AppID, AppKey, KeyID

### 创建Client
这里假定你已经将AppID, AppKey, KeyID保存在环境变量中，可以通过`os.getenv`获取到这些值
1. 没有accessToken的情况下，可以创建Client并获取accessToken
```python
from aqara_python_sdk import AqaraClient
import os

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

# 你可以直接进行后续的逻辑，也可以将token保存下来，下次直接使用
# 当次运行中AqaraClient里会保留这次获取到的Token，但是下次运行时需要重新获取
# Your business logic here
```

2. 已经有accessToken的情况下，可以直接创建Client
```python
from aqara_python_sdk import AqaraClient
import os

app_id = os.getenv("AQARA_APP_ID")
key_id = os.getenv("AQARA_KEY_ID")
app_key = os.getenv("AQARA_APP_KEY")
token = os.getenv("AQARA_ACCESS_TOKEN")
refresh_token = os.getenv("AQARA_REFRESH_TOKEN")

client = AqaraClient(app_id, key_id, app_key, 
                     account="Your Aqara Username", 
                     token=token, 
                     refresh_token=refresh_token)
# Your business logic here
```

### 查询
client只作为一个最底层的API封装类，所以一般不推荐直接调用client中的方法进行操作，而是引入AqaraController进行操作
```python
from aqara_python_sdk import AqaraClient, AqaraController
from aqara_python_sdk.enums.device_type import DeviceType
import os

app_id = os.getenv("AQARA_APP_ID")
key_id = os.getenv("AQARA_KEY_ID")
app_key = os.getenv("AQARA_APP_KEY")
token = os.getenv("AQARA_ACCESS_TOKEN")
refresh_token = os.getenv("AQARA_REFRESH_TOKEN")

client = AqaraClient(app_id, key_id, app_key, 
                     account="Your Aqara Username", 
                     token=token, 
                     refresh_token=refresh_token)

controller = AqaraController(client)
# 加载所有数据，如果数据在其他地方有更新（如在Aqara Home APP中更新了），需要重新调用一次此方法获取最新的数据
controller.load_data()

# 查询指定设备
devices = controller.query_device().position_name("客厅").device_type(DeviceType.LIGHT).device_name("我的射灯").query()

# 查询灯设备
light_controls = controller.query_device().position_name("客厅").device_type(DeviceType.LIGHT).device_name("我的射灯").light()

# 查询场景
all_scene_names = controller.scene().list_scene_names()
my_scene = controller.scene().get_scene_by_name("我的场景")
```

### 操作设备 / 场景
```python
from aqara_python_sdk import AqaraClient, AqaraController
from aqara_python_sdk.enums.device_type import DeviceType
import os

app_id = os.getenv("AQARA_APP_ID")
key_id = os.getenv("AQARA_KEY_ID")
app_key = os.getenv("AQARA_APP_KEY")
token = os.getenv("AQARA_ACCESS_TOKEN")
refresh_token = os.getenv("AQARA_REFRESH_TOKEN")

client = AqaraClient(app_id, key_id, app_key, 
                     account="Your Aqara Username", 
                     token=token, 
                     refresh_token=refresh_token)

controller = AqaraController(client)
# 加载所有数据，如果数据在其他地方有更新（如在Aqara Home APP中更新了），需要重新调用一次此方法获取最新的数据
controller.load_data()

# 获取灯设备
my_light = controller.query_device().position_name("客厅").device_type(DeviceType.LIGHT).device_name("我的射灯").light()[0]
# 执行灯操作
if not my_light.is_on():
    my_light.turn_on()
my_light.set_brightness(50)
my_light.set_color_temperature(4000)

# 执行场景
controller.scene().execute_scene("我的场景")
```

## TODO List:
- [ ] 发布至Pypi
- [ ] 查询功能完善
- [ ] 支持更多开关功能定制
- [ ] 支持窗帘等更多设备
- [ ] 支持场景的创建和编辑