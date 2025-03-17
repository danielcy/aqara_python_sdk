from typing import List

from aqara_python_sdk.client import AqaraClient
from aqara_python_sdk.enums.query import QueryType
from aqara_python_sdk.models.client import Position


class PositionManager:
    def __init__(self, client: AqaraClient, positions: List[Position]):
        self.client = client
        self.positions = positions

    def find_position_by_id(self, position_id: str) -> Position | None:
        for position in self.positions:
            if position.position_id == position_id:
                return position
        return None

    def find_positions_by_name(self, name: str, query_type: QueryType = QueryType.ACCURATE) -> List[Position]:
        if query_type == QueryType.ACCURATE:
            return [position for position in self.positions if position.position_name == name]
        elif query_type == QueryType.FUZZY:
            return [position for position in self.positions if name in position.position_name]
