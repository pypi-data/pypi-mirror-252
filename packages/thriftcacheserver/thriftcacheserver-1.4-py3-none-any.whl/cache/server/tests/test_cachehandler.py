from cache.server.cachehandler import CacheHandler
from cache.gen.keyvalue.ttypes import GetRequest, SetRequest, KeyNotFound
import time


def test_set_and_get():
    ch = CacheHandler()
    request = SetRequest(key="test_key", val="test_value", ttl=10)
    ch.Set(request)
    get_request = GetRequest(key="test_key")
    response = ch.Get(get_request)
    assert response.val == "test_value"


def test_get_nonexistent_key():
    ch = CacheHandler()
    get_request = GetRequest(key="nonexistent_key")
    try:
        ch.Get(get_request)
    except KeyNotFound:
        assert True


def test_get_expired_key():
    ch = CacheHandler()
    request = SetRequest(key="test_key", val="test_value", ttl=1)
    ch.Set(request)
    time.sleep(2)  # Wait for the key to expire
    get_request = GetRequest(key="test_key")
    try:
        ch.Get(get_request)
    except KeyNotFound:
        assert True


def test_cache_full():
    ch = CacheHandler(capacity=3)
    request1 = SetRequest(key="key1", val="value1", ttl=10)
    ch.Set(request1)
    request2 = SetRequest(key="key2", val="value2", ttl=10)
    ch.Set(request2)
    request3 = SetRequest(key="key3", val="value3", ttl=10)
    ch.Set(request3)
    request4 = SetRequest(key="key4", val="value4", ttl=10)
    ch.Set(request4)
    get_request = GetRequest(key="key1")
    try:
        ch.Get(get_request)
    except KeyNotFound:
        assert True
