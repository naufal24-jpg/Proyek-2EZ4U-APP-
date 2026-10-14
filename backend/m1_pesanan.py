class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CustomArray:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.size = 0
        self.data = [None] * self.capacity

    def _resize(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def get(self, index):
        if index < 0 or index >= self.size:
            return None
        return self.data[index]

    def tambah_reguler(self, item):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = item
        self.size += 1

    def tambah_vip(self, item):
        if self.size == self.capacity:
            self._resize()
        for i in range(self.size, 0, -1):
            self.data[i] = self.data[i - 1]
        self.data[0] = item
        self.size += 1

    def tambah_prioritas(self, item):
        if self.size == self.capacity:
            self._resize()
        mid = self.size // 2
        for i in range(self.size, mid, -1):
            self.data[i] = self.data[i - 1]
        self.data[mid] = item
        self.size += 1

    def hapus(self, index):
        if index < 0 or index >= self.size:
            return None
        removed_item = self.data[index]
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return removed_item


class CustomLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def get(self, index):
        if index < 0 or index >= self.size:
            return None
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.data

    def tambah_reguler(self, item):
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def tambah_vip(self, item):
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.size += 1

    def tambah_prioritas(self, item):
        if self.head is None or self.size == 0:
            self.tambah_vip(item)
            return

        mid = self.size // 2
        new_node = Node(item)
        curr = self.head
        for _ in range(mid - 1):
            curr = curr.next

        new_node.next = curr.next
        curr.next = new_node
        if new_node.next is None:
            self.tail = new_node
        self.size += 1

    def hapus(self, index):
        if index < 0 or index >= self.size or self.head is None:
            return None

        if index == 0:
            removed_data = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return removed_data

        curr = self.head
        for _ in range(index - 1):
            curr = curr.next

        removed_data = curr.next.data
        curr.next = curr.next.next
        if curr.next is None:
            self.tail = curr
        self.size -= 1
        return removed_data