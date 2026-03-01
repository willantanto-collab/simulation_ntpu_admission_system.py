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
        #return hash.lib.sha256(combined.encode()).hexdigest()) turn the string from human language into machine code
#Knowledge about this class Securedocument known by self-study.
class SecurityVertifier:
    def vertify(self,document):
        return self.vertify_recursive(document) #starts recursive check from root node
    def vertify_recursive(self,node):
        recalculated = node.content
        for stud in node.student: #veritify all child node
            if not self.vertify_recursive(stud): #if any student fail vertify,stop immediately
                return False
            recalculated += stud.hash #after child vertification,include its hash in parent's recompute
        recalculated  = hashlib.sha256(recalculated.encode()).hexdigest() #recalculate hash for this node
        if recalculated_hash != node.hash:
            print(f"Change of data detected in {node.name}")
            return False #any child tamper triggers in root invalidation
        return True 

#初次尝试写法律逻辑代码化
class CyberLaw:
    def __init__(self, statute_name, severity_level):
        self.statute_name = statute_name  # 法律名称
        self.severity_level = severity_level # 严重等级
class UnauthorizedAccessLaw(CyberLaw):
    def __init__(self, threshold_attempts=3): #threshold_attempts = 3 意思是同一个 IP 尝试非法登录3 次，第一次和第2 次可能因为不小心之类的，第3 次设定为非法登陆
        super().__init__("电脑罪行条例，非法入侵", "High") #定义等级为高严重等级
        self.threshold = threshold_attempts
    def judge(self, logs): #解释情况：根据抓取的痕迹，判断是否违法
        for ip, count in logs.items(): # 统计同一个 IP 的异常行为
            if count > self.threshold: #
                return f"逻辑判定: {ip} 违反了 {self.statute_name}，证据已确凿。"
        return "继续侦查中，关注异常行为”

#Scapy,初次尝试防守黑客攻击者的代码
#自学来的，自学链接用的这个 https://www.youtube.com/watch?v=f4Pr2X98UfE 和其他搜索来源
#https://www.youtube.com/watch?v=f4Pr2X98UfE 这个链接主要讲的是黑客用scapy 的基础攻击手段。
#所以我尝试去理解攻击者的攻击，并试着用代码来反过来从他们攻击的方式防守。我先去理解他们的攻击逻辑。
#还有就是，我写中文注释时担心兼容性，所以专门去查了 Python 编码规范，添加了下面这一行，这个coding and utf8
# -*- coding: utf-8 -*-
from scapy.all import sniff,IP,TCP

def trace_packet(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP): #只关注具有潜在攻击特征的TCP 数据包
      src_ip = packet[IP].src #[IP]：打开packet的外壳，查看网络层（IP层）。.src：Source 是发件人的 IP 地址。.dst：Destination（目的地）是收件人的 IP 地址。
      dst_ip = packet[IP].dst
      if packet[TCP].flags == "S": #模拟黑客追踪，如果发现某个IP 在短时间尝试了大量的SYN 同步包.flags：查看这个包的标志说法，S 代表 SYN，SYN 同步的意思
        print(f"追踪痕迹，查找潜在扫描行为：{src_ip} -> {dst_ip}")#实时反馈：显示攻击源 IP 到目标 IP 的流向
        save_evidence_to_github_style_log(src_ip,"端口扫描尝试")#调用日志函数：将攻击源和行为特征存入本地文件，进行安全取证

def save_evidence_to_github_style_log(ip,behaviour): #Log 是程序在运行过程中，自动记录下来的事件信息。
  with open("forensics_report.log","a", encoding="utf-8") as f: # 使用 with 确保文件操作安全关闭，"a" 模式是为了把新发现的攻击证据追加到日志末尾而不覆盖旧记录。
    f.write(f"IP: {ip} ,行为：{behaviour},状态：已取证\n") # \n 是换行符，确保每条攻击证据独立成行，方便后续自动化审计和搜索。

print("正在尝试监控网络痕迹...需要管理员权限")
sniff(filter = "ip",prn = trace_packet,count = 10) #count = 10 意思是抓取10 个包演示，prn 是回调函数
class AdvancedLegalAnchor: #用来做身份核实，确实是申请人本人所为，而非他人冒用 IP 进行的恶意栽赃
    def __init__(self):
        self.identity_map = {}  #存储 申请人ID -> {设备指纹,临时出入证，常用IP}
    def identify_subject(self, student_id, capture_data):
        # 从 Scapy 抓到的包里提取出所有身份特征
        captured_ip = capture_data.get("ip")
        captured_fingerprint = capture_data.get("fingerprint") #浏览器指纹
        captured_token = capture_data.get("token")           #只有本人才有的登录 Token
        user_anchor = self.identity_map.get(student_id)
        if not user_anchor:
            return 0.1 # 关联度极低，不足以启动行政处分

        #逻辑加权：IP 匹配只占 20%，Token 匹配占 80%
        match_score = 0
        if captured_ip == user_anchor["ip"]:
            match_score += 0.2
        if captured_token == user_anchor["token"]:
            match_score += 0.8 # 只有私钥或 Token 匹配，才能证明是本人操作
        return match_score



    

    
