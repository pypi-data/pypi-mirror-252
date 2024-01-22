import pytest
from cache.core.doublylinkedlist import DoublyLinkedList


@pytest.fixture
def empty_dll():
    return DoublyLinkedList()


@pytest.fixture
def dll_with_values():
    dll = DoublyLinkedList()
    dll.insert_at_tail(1)
    dll.insert_at_tail(2)
    dll.insert_at_tail(3)
    return dll


def test_size(empty_dll, dll_with_values):
    assert empty_dll.size() == 0
    assert dll_with_values.size() == 3


def test_is_empty(empty_dll, dll_with_values):
    assert empty_dll.is_empty() is True
    assert dll_with_values.is_empty() is False


def test_insert_at_tail(empty_dll):
    empty_dll.insert_at_tail(1)
    assert empty_dll.size() == 1
    assert empty_dll.head.data == 1
    assert empty_dll.tail.data == 1


def test_delete_head(dll_with_values):
    deleted_value = dll_with_values.delete_head()
    assert deleted_value == 1
    assert dll_with_values.size() == 2
    assert dll_with_values.head.data == 2


def test_delete_node(dll_with_values):
    node_to_delete = dll_with_values.head.next
    deleted_value = dll_with_values.delete_node(node_to_delete)
    assert deleted_value == 2
    assert dll_with_values.size() == 2
    assert dll_with_values.tail.data == 3


def test_delete_tail(dll_with_values):
    deleted_value = dll_with_values.delete_node(dll_with_values.tail)
    assert deleted_value == 3
    assert dll_with_values.size() == 2
    assert dll_with_values.tail.data == 2


def test_delete_only_node(empty_dll):
    empty_dll.insert_at_tail(1)
    deleted_value = empty_dll.delete_node(empty_dll.head)
    assert deleted_value == 1
    assert empty_dll.size() == 0
    assert empty_dll.head is None
    assert empty_dll.tail is None
