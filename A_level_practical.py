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

def insertion_sort(alist):
    # The first element is considered sorted, so we start from index 1
    for index in range(1, len(alist)):
        current_value = alist[index]
        position = index

        # Shift elements of the sorted part that are greater than current_value
        while position > 0 and alist[position - 1] > current_value:
            alist[position] = alist[position - 1]
            position = position - 1

        # Insert the value into its correct location
        alist[position] = current_value

    return alist

# Example usage
data = [9, 5, 4, 15, 3]
sorted_data = insertion_sort(data)
print(sorted_data)

#Recursion Binary tree
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def buildTree(preorder, inorder):
    # Mapping inorder values to indices for O(1) lookup
    idx_map = {val: i for i, val in enumerate(inorder)}
    
    def helper(pre_start, pre_end, in_start, in_end):
        # Base case: no elements to construct the tree
        if pre_start > pre_end:
            return None

        # Root is the first element in current preorder segment
        root_val = preorder[pre_start]
        root = TreeNode(root_val)

        # Locate root in inorder to split left/right subtrees
        root_idx = idx_map[root_val]
        left_size = root_idx - in_start

        # Recursively build subtrees using index boundaries
        root.left = helper(pre_start + 1, pre_start + left_size, in_start, root_idx - 1)
        root.right = helper(pre_start + left_size + 1, pre_end, root_idx + 1, in_end)

        return root

    return helper(0, len(preorder) - 1, 0, len(inorder) - 1)

# Example Execution
# Preorder: [3, 9, 20, 15, 7]
# Inorder:  [9, 3, 15, 20, 7]
root = buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])

#Linked list
class Node:
    def __init__(self, data):
        self.data = data      # The actual value stored
        self.next = None      # Pointer to the next node

class LinkedList:
    def __init__(self):
        self.head = None      # Start of the list

    def insert_at_end(self, data):
        new_node = Node(data)
        
        # If the list is empty, make new node the head
        if self.head is None:
            self.head = new_node
            return
        
        # Otherwise, traverse to the last node
        current = self.head
        while current.next:
            current = current.next
        
        # Point the last node to the new node
        current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

# --- Practical Test ---
my_list = LinkedList()
my_list.insert_at_end("A")
my_list.insert_at_end("B")
my_list.insert_at_end("C")

my_list.display() 
# Output: A -> B -> C -> None


