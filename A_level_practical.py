# Stack
class Stack:
    def __init__(self, size):
        self.stack = []
        self.max_size = size
        self.top = -1  # initialise top as -1

    def is_full(self):
        return len(self.stack) == self.max_size

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        if self.is_full():
            print("Stack Overflow")
        else:
            self.stack.append(item)
            self.top += 1

    def pop(self):
        if self.is_empty():
            print("Stack Underflow")
            return None
        else:
            self.top -= 1
            return self.stack.pop()

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None
# Queue
class CircularQueue:
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.queue = [None for i in range(maxSize)]
        self.front = 0
        self.rear = -1
        self.numberOfItems = 0

    def isFull(self):
        return self.numberOfItems == self.maxSize

    def isEmpty(self):
        return self.numberOfItems == 0

    def enqueue(self, item):
        if self.isFull():
            print("Queue Overflow!")
        else:
            self.rear = (self.rear + 1) % self.maxSize #Use the modulo operator (%) to make the pointer wrap around to the start
            self.queue[self.rear] = item
            self.numberOfItems += 1
            print(f"Enqueued: {item}")

    def dequeue(self):
        if self.isEmpty():
            print("Queue Underflow!")
            return None
        else:
            item = self.queue[self.front]
            self.queue[self.front] = None # 可选：清除数据
            # 核心逻辑：Front 指针同样需要循环
            self.front = (self.front + 1) % self.maxSize
            self.numberOfItems -= 1
            return item
q = CircularQueue(3)
q.enqueue("Data1")
q.enqueue("Data2")
q.enqueue("Data3")
print(q.dequeue())    # 输出 Data1
q.enqueue("Data4")    

