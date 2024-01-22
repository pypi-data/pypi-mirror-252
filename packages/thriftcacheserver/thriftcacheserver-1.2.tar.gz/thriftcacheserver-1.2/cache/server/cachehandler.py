import time
from typing import Any, Dict
from cache.core.doublylinkedlist import DoublyLinkedList
from cache.gen.keyvalue.ttypes import (
    GetRequest,
    GetResponse,
    SetRequest,
    KeyNotFound
)


class KeyValue:
    def __init__(self, key: str, value: str, ttl: int) -> None:
        self.key = key
        self.value = value
        self.ttl = ttl
        self.insert_time: float = time.time()


class CacheHandler:
    def __init__(self, capacity: int = 100000) -> None:
        self._cache: Dict[str, Any] = {}
        self.capacity = capacity
        self._values_list = DoublyLinkedList()

    def Set(self, request: SetRequest) -> None:
        key = request.key
        value = request.val
        ttl = request.ttl

        if key in self._cache:
            self._values_list.delete_node(self._cache[key])
        elif self._values_list.size() == self.capacity:
            del_data = self._values_list.delete_head()
            del self._cache[del_data.key]

        self._values_list.insert_at_tail(KeyValue(key, value, ttl))
        self._cache[key] = self._values_list.tail

    def Get(self, request: GetRequest) -> GetResponse:
        key = request.key
        if key in self._cache:
            data = self._cache[key].data
            is_expired = self._check_key_expired(data.insert_time, data.ttl)
            if is_expired:
                del self._cache[key]
            else:
                return GetResponse(val=data.value)
        raise KeyNotFound()

    def _check_key_expired(self, insert_time: int, ttl: int) -> int:
        current_time = time.time()
        if ttl == 0:
            return 0
        if (current_time - insert_time) >= ttl:
            return 1
        return 0


if __name__ == "__main__":
    ch = CacheHandler()
    ch.Set(SetRequest(key="shivam", val="mitra", ttl=0))
    result: GetResponse = ch.Get(GetRequest(key="shivam"))
    print(result.val)
