from typing import Any, Optional


class Node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size: int = 0

    def size(self) -> int:
        return self._size

    @property
    def head(self) -> Optional[Node]:
        return self._head

    @property
    def tail(self) -> Optional[Node]:
        return self._tail

    def is_empty(self) -> bool:
        if self._head is None:
            return True
        return False

    def insert_at_tail(self, val: Any) -> None:
        new_node = Node(val)

        if self.is_empty():
            self._head = self._tail = new_node
        else:
            assert self._tail is not None
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        self._size += 1

    def delete_head(self) -> Any:
        assert self._head is not None
        data = self._head.data

        if self.is_empty():
            return None
        if self._head == self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
            assert self._head is not None
            self._head.prev = None

        self._size -= 1
        return data

    def delete_node(self, node: Node) -> Any:
        assert self._head is not None

        data = node.data
        if self._head == self._tail:
            self._head = self._tail = None
        else:
            prev_node = node.prev
            assert prev_node is not None
            prev_node.next = node.next
            if node.next:
                node.next.prev = prev_node
                node.next = None
            else:
                self._tail = prev_node
                node.prev = None
        self._size -= 1
        return data

    def display(self) -> None:
        head = self._head
        while head:
            print(head.data, end=" ")
            head = head.next
        print()
