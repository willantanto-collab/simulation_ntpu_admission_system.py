class SearchManager:
    def __init__(self, data_list):
        self.__data = data_list  
        self.comparisons = 0     # 记录比较次数，考试常考复杂度分析
    def linear_search(self, target): #找到在哪个位置
        for index in range(len(self.__data)):
            self.comparisons += 1
            if self.__data[index] == target:
                return index
        return -1
    def find_all(self, target): #列出所有能找到的位置
        indices = []
        for index in range(len(self.__data)):
            if self.__data[index] == target:
                indices.append(index)
        return indices
    def get_efficiency_report(self, target): #查找东西的速度
        result = self.linear_search(target)
        status = f"Found at index {result}" 
        if result != -1:
            status = f"已定位该申请人，存储索引为: {result}"
        else:
            status = "查无此人，未提交申请或编号错误"

