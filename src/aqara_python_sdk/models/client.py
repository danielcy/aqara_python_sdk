class Device:
    def __init__(self, data_dict):
        # 设备id
        self.did: str = data_dict.get("did")
        # 网关id
        self.parent_did: str = data_dict.get("parentDid")
        # 位置id
        self.position_id: str = data_dict.get("positionId")
        # 物模型
        self.model: str = data_dict.get("model")
        # 1：可挂子设备的网关；2：不可挂子设备的网关；3：子设备
        self.model_type: int = data_dict.get("modelType")
        # 在线状态：1-在线 0-离线
        self.state: int = data_dict.get("state")
        # 设备名称
        self.device_name: str = data_dict.get("deviceName")
        # 时区
        self.time_zone: str = data_dict.get("timeZone")
        # 固件版本号
        self.firmware_version: str = data_dict.get("firmwareVersion")
        # 入网时间
        self.create_time: str = data_dict.get("createTime")
        # 更新时间
        self.update_time: str = data_dict.get("updateTime")


class Resource:
    def __init__(self, data_dict):
        # 物模型
        self.subject_model: str = data_dict.get("subjectModel")
        # 资源 ID
        self.resource_id: str = data_dict.get("resourceId")
        # 最小值
        self.min_value: int = data_dict.get("minValue")
        # 最大值
        self.max_value: int = data_dict.get("maxValue")
        # 权限 (0-可读， 1-可写， 2-可读/可写)
        self.access: int = data_dict.get("access")
        # 参数枚举值
        self.enums: str = data_dict.get("enums")
        # 资源名称
        self.name: str = data_dict.get("name")
        # 资源描述
        self.description: str = data_dict.get("description")
        # 值单位
        self.unit: int = data_dict.get("unit")


class Position:
    def __init__(self, data_dict):
        # 父位置id
        self.parent_position_id: str = data_dict.get("parentPositionId")
        # 位置id
        self.position_id: str = data_dict.get("positionId")
        # 位置名称
        self.position_name: str = data_dict.get("positionName")
        # 创建时间
        self.create_time: str = data_dict.get("createTime")
        # 位置描述
        self.description: str = data_dict.get("description")


class Scene:
    def __init__(self, data_dict):
        # 场景id
        self.scene_id = data_dict.get("sceneId")
        # 场景model
        self.model = data_dict.get("model")
        # 场景名称
        self.name = data_dict.get("name")
        # 0:云端 1:本地 3：云端化中 4：本地化中
        self.localize = data_dict.get("localizd")


class ResourceStatus:
    def __init__(self, data_dict):
        self.subject_id = data_dict.get("subjectId")
        self.resource_id = data_dict.get("resourceId")
        self.value = data_dict.get("value")
        self.time_stamp = data_dict.get("timeStamp")
