from typing import TypeVar, Generic, List

T = TypeVar('T')


class PagingResponse(Generic[T]):
    def __init__(self, data: List[T], total):
        self.data = data
        self.total = total
