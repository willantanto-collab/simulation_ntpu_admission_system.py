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

# Combination of file handling and 2D array 
student_data = [[None for _ in range(4)] for _ in range(10)]

def load_and_process(filename):
    try:
        with open(filename, 'r') as file:
            row_index = 0
            for line in file:
                # prevent out of range ,set a value as 10 
                if row_index >= 10: 
                    break 
                
                # Clean up the data by using strip and split.
                parts = line.strip().split(',')
                
                # Moving data into our 2D array.
                for col_index in range(len(parts)):
                    val = parts[col_index]
                    if col_index > 0:
                        student_data[row_index][col_index] = int(val)
                    else:
                        student_data[row_index][col_index] = val
                
                row_index += 1
        return row_index 
    except FileNotFoundError:
        print("Wait, the file isn't there! Check the filename again.")
        return 0

def calculate_averages(data, num_rows):
    for r in range(num_rows):
        total = 0
        count = 0
        # start 'c' at 1 because column 0 is the Student ID, not a score.
        for c in range(1, 4):
            if data[r][c] is not None:
                total += data[r][c]
                count += 1  
        # Avoid dividing by zero if a student has no scores or like not coming to exam.
        if count > 0:
            avg = total / count
            print(f"Student {data[r][0]}: Average = {avg:.2f}")
actual_rows = load_and_process("data.txt")
calculate_averages(student_data, actual_rows)

