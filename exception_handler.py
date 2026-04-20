# -*- coding: utf-8 -*-
def is_integer(value):
    #检查是否为整数，防止 InsertNode 时因类型错误导致比较失败
    try:
        int(value)
        return True
    except:
        return False

def is_tree_full(current_free, max_size):
    # 防止数组越界（IndexError），在分配 FreeNode 前调用
    if current_free >= max_size:
        print("错误：树空间已满，无法继续插入")
        return True
    return False

def is_valid_pointer(pointer, max_size):
    # 检查指针是否合法，防止读取不存在的内存空间
    if pointer < -1 or pointer >= max_size:
        print(f" 错误：无效索引 {pointer}")
        return False
    return True
