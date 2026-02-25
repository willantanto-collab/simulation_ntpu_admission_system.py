class SearchManager:
    def __init__(self, data_list):
        self.__data = data_list  
        self.comparisons = 0     
        self._cache = {}  # 缓存，避免重复的行为计算
    def linear_search(self, target):
        if target in self._cache:  # 增加缓存检查，如果找过就直接给结果
            return self._cache[target]
        for index, value in enumerate(self.__data): # 使用 enumerate 替代 range(len())，更简洁高效，他是用来循环时自动一边点名，一边报数，不用自己动手写代码去数现在是第几个的一种流程。
            self.comparisons += 1
            if value == target:
                self._cache[target] = index #存入缓存
                return index  
        self._cache[target] = -1
        return -1
    def find_all(self, target):
        results = []
        for index, value in enumerate(self.__data):
            if value == target:
                results.append(index)
        return results
    def get_efficiency_report(self, target):  # 只负责生成好看的报告，更简洁
        result = self.linear_search(target)
        if result != -1:
            status = f"该申请人的相关数据: {result}"
        else:
            status = "查无此人，请核对编号"
        return f"查询报告 ｜ 目标: {target} ｜ 结果: {status} ｜ 累计比较: {self.comparisons}次"
import hashlib #Standard python library for cyptographic hashing
#Hash function like SHA-256 are one-way function: easy to compute,hard to reverse.
#Used here to create unique fingerprints of document for integrity vertification.
#Hash : a fixed-length unique fingerprint representing some data
class SecureDocument:
    def __init__(self,name,content = Name,student = None):
        self.name = name
        self.content = content or "" #Write or "" ensures the node always has a string,preventing error in hash computation if content is missing.
        self.student = student or [] #Similar logic as the self.content = content or ""
        self.hash = self.generate_hash() #Computes a fingerprint of this node and its subtree for furture integrity checks
    def generate_hash(self): #calculates a SHA-256 fingerprint using this node's conetnt plus all students
        combined = self.content
        for stud in self.student:
            combined += stud.hash
        return hash.lib.sha256(combined.encode()).hexdigest()) #converts content to bytes and creates a unique fingerprint for integrity vertification
        #line 42 turn the string from human language into machine code
#Knowledge about this class Securedocument known by self-study.
