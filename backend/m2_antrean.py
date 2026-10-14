class Stack:
    def __init__(self):
        self.data = []

    def push(self, val):
        self.data.append(val)

    def pop(self):
        if self.is_empty():
            return None
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

def tokenize(ekspresi):
    """Memecah string ekspresi menjadi token angka multi-digit, operator, dan kurung."""
    tokens = []
    i = 0
    n = len(ekspresi)
    while i < n:
        char = ekspresi[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit():
            num_str = ""
            while i < n and ekspresi[i].isdigit():
                num_str += ekspresi[i]
                i += 1
            tokens.append(int(num_str))
        else:
            tokens.append(char)
            i += 1
    return tokens


def ke_postfix(ekspresi):
    """Mengubah ekspresi infix menjadi postfix menggunakan Stack."""
    tokens = tokenize(ekspresi)
    output = []
    stack = Stack()
    
    prioritas = {'+': 1, '-': 1, '*': 2, '/': 2}

    for token in tokens:
        if isinstance(token, int):
            output.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            stack.pop()  # Buang tanda '('
        elif token in prioritas:
            while (not stack.is_empty() and 
                   stack.peek() in prioritas and 
                   prioritas[stack.peek()] >= prioritas[token]):
                output.append(stack.pop())
            stack.push(token)

    while not stack.is_empty():
        output.append(stack.pop())

    return output


def hitung_postfix(postfix_tokens):
    """Menevaluasi token postfix menggunakan Stack nilai."""
    stack = Stack()

    for token in postfix_tokens:
        if isinstance(token, int):
            stack.push(token)
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '/':
                stack.push(a // b)

    return stack.pop()

class QueueNaif:
    def __init__(self):
        self.data = []
        self.total_geseran = 0

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self, k=1):
        """Mengambil k elemen dari depan dengan menggeser seluruh sisa elemen - O(n)."""
        hasil = []
        for _ in range(k):
            if len(self.data) == 0:
                break
            item = self.data.pop(0)  
            self.total_geseran += len(self.data)
            hasil.append(item)
        return hasil

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)


class QueueCircular:
    def __init__(self, capacity=32768):
        self.capacity = capacity
        self.data = [None] * self.capacity
        self.front = 0
        self.rear = 0
        self.count = 0

    def _resize(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.count):
            new_data[i] = self.data[(self.front + i) % self.capacity]
        self.data = new_data
        self.front = 0
        self.rear = self.count
        self.capacity = new_capacity

    def enqueue(self, item):
        if self.count == self.capacity:
            self._resize()
        self.data[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1

    def dequeue(self, k=1):
        """Mengambil k elemen dari depan hanya dengan memajukan penunjuk front - O(1)."""
        hasil = []
        for _ in range(k):
            if self.count == 0:
                break
            item = self.data[self.front]
            self.data[self.front] = None
            self.front = (self.front + 1) % self.capacity
            self.count -= 1
            hasil.append(item)
        return hasil

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count


class UndoRedoManager:
    def __init__(self, queue_naif, queue_circular):
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.q_naif = queue_naif
        self.q_circ = queue_circular

    def catat_aksi(self, jenis_aksi, data):
        self.undo_stack.push((jenis_aksi, data))
        self.redo_stack = Stack()  

    def undo_last(self):
        if self.undo_stack.is_empty():
            return None, "Tidak ada aksi yang bisa dibatalkan."

        aksi, data = self.undo_stack.pop()

        if aksi == 'ENQUEUE':
            if not self.q_naif.is_empty():
                self.q_naif.data.pop()
            if not self.q_circ.is_empty():
                self.q_circ.rear = (self.q_circ.rear - 1 + self.q_circ.capacity) % self.q_circ.capacity
                self.q_circ.data[self.q_circ.rear] = None
                self.q_circ.count -= 1
            pesan = f"Pembatalan enqueue: pesanan {data} dikeluarkan dari belakang."

        elif aksi == 'DEQUEUE':
            self.q_naif.data = data + self.q_naif.data
            for item in reversed(data):
                if self.q_circ.count == self.q_circ.capacity:
                    self.q_circ._resize()
                self.q_circ.front = (self.q_circ.front - 1 + self.q_circ.capacity) % self.q_circ.capacity
                self.q_circ.data[self.q_circ.front] = item
                self.q_circ.count += 1
            pesan = f"Pembatalan dequeue: {len(data)} pesanan dikembalikan ke DEPAN antrean."

        self.redo_stack.push((aksi, data))
        return aksi, pesan

    def redo_last(self):
        if self.redo_stack.is_empty():
            return None, "Tidak ada aksi yang bisa diulang."

        aksi, data = self.redo_stack.pop()

        if aksi == 'ENQUEUE':
            self.q_naif.enqueue(data)
            self.q_circ.enqueue(data)
            pesan = f"Enqueue dikerjakan lagi: pesanan {data} masuk kembali ke belakang."

        elif aksi == 'DEQUEUE':
            k = len(data)
            self.q_naif.dequeue(k)
            self.q_circ.dequeue(k)
            pesan = f"Dequeue dikerjakan lagi: {k} pesanan dikeluarkan kembali."

        self.undo_stack.push((aksi, data))
        return aksi, pesan