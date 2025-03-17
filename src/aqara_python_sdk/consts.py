from dataclasses import dataclass


@dataclass
class ResourceIdConsts:
    POWER_STATUS: str = "4.1.85"
    POWER_STATUS_CH_1: str = "4.1.85"
    POWER_STATUS_CH_2: str = "4.2.85"
    POWER_STATUS_CH_3: str = "4.3.85"
    LIGHT_LEVEL: str = "1.7.85"
    LIGHT_LEVEL_V2: str = "14.1.85"
    COLOR_TEMPERATURE: str = "1.9.85"
    COLOR_TEMPERATURE_V2: str = "14.2.85"
