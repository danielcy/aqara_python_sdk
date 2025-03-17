from typing import List

from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.enums.query import QueryType
from aqara_python_sdk.models.client import Scene
from aqara_python_sdk.models.contract import BaseResponse


class SceneManager:
    def __init__(self, client: AqaraClient, scenes: List[Scene]):
        self.client = client
        self.scenes = scenes

    def list_scene_names(self) -> List[str]:
        return list(map(lambda x: x.name, self.scenes))

    def execute_scene(self, name: str) -> BaseResponse:
        scene = self.get_scene_by_name(name)
        if scene is None:
            return BaseResponse(False, "场景不存在")
        response = self.client.execute_scene(scene.scene_id)
        return response

    def get_scene_by_name(self, name, query_type: QueryType = QueryType.ACCURATE) -> Scene | None:
        for scene in self.scenes:
            if query_type == QueryType.ACCURATE:
                if scene.name == name:
                    return scene
            if query_type == QueryType.FUZZY:
                if name in scene.name:
                    return scene
        return None
