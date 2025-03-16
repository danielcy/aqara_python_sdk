from typing import List

from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.enums.query import QueryType
from aqara_python_sdk.models.client import Scene


class SceneManager:
    def __init__(self, client: AqaraClient, scenes: List[Scene]):
        self.client = client
        self.scenes = scenes

    def list_scene_names(self) -> List[str]:
        return list(map(lambda x: x.name, self.scenes))

    def get_scene_by_name(self, name, queryType: QueryType = QueryType.ACCURATE) -> Scene | None:
        for scene in self.scenes:
            if queryType == QueryType.ACCURATE:
                if scene.name == name:
                    return scene
            if queryType == QueryType.FUZZY:
                if name in scene.name:
                    return scene
        return None
