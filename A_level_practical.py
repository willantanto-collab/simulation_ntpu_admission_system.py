
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
