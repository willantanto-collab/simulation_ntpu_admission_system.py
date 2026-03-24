#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 上面这两行，我在 GitHub 上看那些开源项目（比如 Scapy 官方文档里的工具）时，发现代码厉害的文件开头都有。
# 我查了一下，发现这是为了在 Linux 下能直接运行，并且让中文注释不乱码，所以我专门在平板上手打加了进去。

# 我之前写的 algorithm.py 那个文件只能识别攻击类型，但在 WMN Lab 的研究中，
# 我发现陈教授的论文中提到攻击源的“网络拓扑位置” (Hop count)。
# 我看不懂那么多复杂的数学模型，但我在学习 Scapy 的 IP() 类时产生了一个疑问：
# 为什么它会有 ttl, tos, flags 这些字段？这些缩写名字是谁定义的？
# 于是我顺着 Scapy 的文档去搜了 IPv4 Standard，最终锁定了互联网协议的“宪法”—— RFC 791。
# 因此我引入了 RFC 791 里的 TTL 逻辑进行优化，想看看能不能算出黑客离我有多远。
# 自学参考来自：Wireshark 官方文档、Scapy 文档、RFC 791

#layer 4
from scapy.all import *
import time

# 定义合法访问的白名单（模拟台积电内部受保护网段，或者是 WMN 实验室的受信任机器）
AUTHORIZED_IPS = ["192.168.1.100", "192.168.1.101"]

# 我刚学到真正的 Layer 4 审计必须具备“记忆”。
# 如果只看一个包，我分不清它是正常请求还是黑客在搞 SYN Flood 攻击。
# 所以我建立这个审计状态的这种方式，用来记录每个 IP 在短时间内的 SYN 频率。
connection_history = {} 

def get_topology_dist(packet):
    if packet.haslayer(IP):
        ttl_value = packet[IP].ttl # 利用 RFC 791 的 TTL 逻辑反推距离。用 64 减去。。是因为我查到大多数 Linux 系统的初始 TTL 是 64。
        # 减出来的数字就是这个包一路上“跳”过了多少个路由器。
        # 这个数字能帮我判断黑客离我有多远，是我在看陈教授论文时看见教授很看重的一个点叫“拓扑位置”。
        return 64 - ttl_value
    return "Unknown" # 异常的边界，如系统无法判断或出现错误

def compliance_audit_sniffer(packet):
    # 针对 Layer 4 判定“意图”与“响应”
    if packet.haslayer(TCP):
        flags = packet[TCP].flags
        src_ip = packet[IP].src
        dist = get_topology_dist(packet)
        now = time.time()

        # 核心判定：如果 Flags 是 "S" (SYN)，代表扫描或企图侵入
        if flags == "S":
                    # 【Day 32 记录：啃下 TCP Options 嵌套列表解析】
        # 我在 Wireshark 看到 TCP 后面跟着一串 MSS, WScale... 
        # 但 Scapy 拿出来的 options 是个嵌套列表：[('MSS', 1460), ('WScale', 7)]。
        # 我折腾了一下，用 dict() 强转才好拿数据。这几行是我为了对齐陈教授论文里的“拓扑特征”加的。
        if flags == "S":
            # 我在Wireshark看到 TCP 后面跟着一串 MSS, WScale... 但 Scapy 拿出来的 options 是个嵌套列表。
            # 我发现可以用 dict() 把这个列表转成字典，这样就能用 .get('MSS') 拿到数据了。
            tcp_options = dict(packet[TCP].options)
            mss_val = tcp_options.get('MSS')
            
            # 如果 MSS 偏小（比如 < 1400），可能代表黑客中间套了隧道或 VPN。
            # 我在 Wireshark 调试时发现MSS值的变动，我发现这似乎能从侧面辅助验证陈教授论文中提到的拓扑隐蔽性。
            if mss_val:
                print(f"[证据提取] 探测到 TCP 指纹 MSS: {mss_val} (拓扑距离: {dist})") #MSS 是Maximum Segment Size的意思。
                if mss_val < 1400:
                    print(f"疑似存在加密隧道，源端拓扑环境可能经过二次封装。")

            # 意图审查 (Intent Audit)：违反越权访问规制
            if src_ip not in AUTHORIZED_IPS:
                print(f"[警告] 非法入侵企图：源 IP {src_ip} (拓扑距离: {dist}) 试图发起未经授权的请求。")
            else:
                print(f"[审计] 合法连接请求：源 {src_ip} (拓扑距离: {dist}) 正在履行准入协议。")

            # 可用性保护 (Availability Protection)：对抗 SYN Flood
            # 这里的逻辑是：代码即法律，如果同一源短时间内发送大量 SYN，判定为“架构滥用”
            history = connection_history.get(src_ip, [])
            history = [t for t in history if now - t < 1.0] # 仅保留 1 秒内的记录，这就是“滑动窗口”
            history.append(now)
            connection_history[src_ip] = history

            if len(history) > 10:
                print(f"[致命风险] 检测到 SYN Flood：源 {src_ip} 频率过高，正在消耗系统资源！")

        # 如果 Flags 是 "A" (ACK)，标志三次握手完成
        elif flags == "A":
            # 调研陈教授的论文后，我将这部分重构为“数字鉴识”(Forensics) 检查
            # 因为 ACK 意味着连接已经从“想进来”变成了“已经进来”，法律判定为“实质侵入”阶段
            print(f"[鉴识报告] 连接已建立：源 {src_ip} 已通过握手阶段。")

# 启动针对 WMN Lab 环境的协议合规性实时审计
# 我原本在查 TCP 的原始标准 RFC 793，结果在翻看维基百科和 IETF 官网时，
# 看到一个醒目的提示说 RFC 793 已经在 2022 年被 RFC 9293 取代（Obsoleted）了。
# 既然要学就学最新的，虽然里面很多拥塞控制的算法我看不懂，
# 但它对 Flags 的基本定义没变，所以我决定在审计逻辑里标注这个最新的标准。
print("正在执行 Layer 4 协议合规性实时审计 (基于 RFC 791 & RFC 9293)...")
# 过滤 tcp 流量，store=0 是因为我想像专业工具那样只实时处理而不把包全存进内存，省点资源。
sniff(filter="tcp", prn=compliance_audit_sniffer, store=0)


#layer 3
import time
from scapy.all import * # 导入所有工具，省去查文档的时间

TARGET_IP = "192.168.1.100"  # 模拟的IoT网关地址
SECRET_DATA = "PROMPT_ID_791:ACTION_BYPASS_LEGAL_FILTER" # 模拟一段经过“质询工程”处理后的法律存证

def send_covert_packet(target, message):
    # 模拟 6G/IoT 实验中的实时反馈
    print(f"正在向 {target} 注入 Layer 3 流量...")

    # 构造 IP 层 (Layer 3)
    # [学习笔记] id=791: 我手动指定了 ID 字段，这样在 Wireshark 过滤器里输入 'ip.id == 791' 就能瞬间定位
    # 这样设定，因为这比默认的随机 ID 更像一个“实验室预设”的特征码
    ip_layer = IP(dst=target, id=791) 

    # 协议封装逻辑 (Protocol Stack Construction)
    # 利用 / 符号快速叠加协议，比写复杂的类定义快得多
    # 将 message 直接作为载荷，实现极简信令传输
    icmp_packet = ip_layer / ICMP() / message 

    # 逻辑：通过 raw() 函数把包转成十六进制打印出来
    # 目的：学习 L3 载荷在网线里到底长什么样。看到 '4500' 开头就知道这是 IPv4
    raw_bytes = raw(icmp_packet)
    print(f"原始字节流(Hex): {raw_bytes.hex()[:50]}...") 

    # 执行 Layer 3 原始套接字注入
    # verbose=False: 解决逻辑：防止控制台被 Scapy 自带的 "Sent 1 packets" 刷屏，保持实验界面整洁
    send(icmp_packet, verbose=False)
    
    # 通过 Python 内置 len() 监控 L3 载荷大小，评估 6G 信令的传输效率
    print(f"数据包已发出，载荷长度: {len(message)} bytes") 

if __name__ == "__main__":
    # 模拟 NTPU WMN Lab 实验环境
    print("NTPU WMN Lab 模拟环境 (RPG-791)")
    print("提示：已开启 id=791 特征标记，请在 Wireshark 中同步观察")
    
    try:
        while True:
            send_covert_packet(TARGET_IP, SECRET_DATA)
            # 设置 5 秒实验间隔。源于平板运行环境的性能限制，确保我有足够时间切换到抓包软件看一眼
            time.sleep(5) 
    except KeyboardInterrupt: 
        # 针对 Pydroid 3 这种平板环境，捕获停止按钮产生的信号，避免屏幕变红
        print("\n 实验停止，数据已手动保存。")

#layer 2
#layer 2
from scapy.all import *

# 实测发现RSSI跳变剧烈，建立一个历史列表存最近5个包。
rssi_history = [] 

def cross_layer_analysis(pkt): # pkt = packet
    global rssi_history # 必须加 global 才能在函数里更新这个列表
    
    # 抓取 RadioTap 头部，获取 Layer 2的物理层链路强度 (RSSI)
    if pkt.haslayer(RadioTap):
        # rssi_value 提取自 RadioTap 层，是设备的信号强度 (单位为 dBm)
        rssi_value = pkt.dBm_AntSignal 
        
        # 异常捕获：部分管理帧或干扰帧可能无法提取 RSSI (返回 None)
        # 为防止 sum() 运算因类型不匹配崩溃，需过滤掉无效的物理层采样
        if rssi_value is None:
            return 
        
        # 提取 TCP 拥塞控制的表征——窗口大小
        if pkt.haslayer(TCP):
            rssi_history.append(rssi_value)
            if len(rssi_history) > 5:
                rssi_history.pop(0) # 无线信号是实时变化的，所以要替换掉旧的数据（FIFO）
            avg_rssi = sum(rssi_history) / len(rssi_history) # 算平均值以平滑信号抖动

            tcp_window = pkt[TCP].window
            src_ip = pkt[IP].src       
            
            # 观测 RSSI 下降与 TCP 窗口的协同变化
            print(f"[Link-Awareness Test] Source: {src_ip}")
            print(f"  Layer 2 (RSSI): {rssi_value} dBm | Avg: {avg_rssi:.1f}") # 这里多显个平均值对比
            print(f"  Layer 4 (TCP Win): {tcp_window}")            
            
            # 改用 avg_rssi 判定，防止信号抖动导致误判。
            if avg_rssi < -70: 
                print(f"链路质量劣化：平均信号跌至 {avg_rssi:.1f} dBm。")
                
                # 实测点：当窗口跌破 1000，验证 TCP 是否因物理层丢包而错误进入拥塞控制
                if tcp_window < 1000: 
                    print("验证成功：捕获到 TCP 窗口大幅收缩，说明协议误判了拥塞。\n")


#layer 1:
from scapy.all import *
# 物理层模拟 (Layer 1 Metadata)
# 使用RadioTap层模拟特定的物理层参数，如发射功率、信道
# 在Lessig理论中的一种前置的“空间法律”
radio_layer = RadioTap(present='Rate+Channel+dBm_AntSignal',Rate=2.0，ChannelFrequency=2412, dBm_Power_Signal=-30)
# 链路层构建 (Layer 2 - Code is Law)
# 构造一个 802.11 Beacon 帧。Addr2 是发送方，Addr3 是 BSSID。
# 这里的代码逻辑决定了周围设备是否能识别并受其约束。
# 因为真正的 Layer 1 需要昂贵的 SDR（软件定义无线电） 硬件才能直接操作电磁波
# 在没有特定设备的情况下，我选择用Scapy这种方式，通过代码在 Layer 2 伪造物理参数来达到“模拟质询”的效果。
# 我最初只是好奇为什么手机能搜到 WiFi 名字。通过查资料，我发现所有路由器都在不停广播一个叫 Beacon 的东西。
# 顺着这个线索，我找到了 Scapy 这个工具，并在它的文档里看到了 802.11 协议的结构图
# 在 802.11 协议的代码架构中，type=0 代表它是管理类数据包，而 subtype=8 则是它的法律身份编号
dot11 = Dot11(type=0, subtype=8, 
              addr1="ff:ff:ff:ff:ff:ff", 
              addr2="aa:bb:cc:dd:ee:ff", 
              addr3="aa:bb:cc:dd:ee:ff")
# 质询载荷 (Inquiry Engineering)
# 将 Lessig 的核心思想作为 Payload。在质询工程中，载荷用于测试系统对非标准数据的响应。
# Beacon 更像无线世界的“强制公告”，它定义了该信号覆盖范围内的所有连接规则。
beacon = Dot11Beacon(cap="ESS+privacy") #将安全约束直接写入物理帧，利用Code is Law强制周围设备必须匹配特定加密逻辑才能建立连接。
essid = Dot11Elt(ID="SSID", info="Code is Law", len=len("Code is Law")) #这是无线网络的“身份公告”，不仅通过SSID广播网络名称，还利用 len 参数严格对齐字节长度，确保物理层扫描器能合法解析出这个由“代码”定义的空间边界。
rates = Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96") #宣告物理层支持的传输速率（1,2,5.5,11Mbps），为协议握手的后续改变做准备
dsset = Dot11Elt(ID="DSset", info=b"\x06") #确保逻辑层与RadioTap物理频率实现硬性对齐

legal_payload = Raw(load="[Inquiry] Protocol is the Regulatory Architecture.") #将质询逻辑作为原始负载注入，测试系统是否能在遵守协议“法律”的同时，正确过滤这些非标准的架构指令
#封装发送

packet = radio_layer / dot11 / beacon / essid / rates / dsset / legal_payload
print("Packet Structure")
packet.show() 

# 注意：以下操作需要支持 Monitor 模式的网卡
# sendp(packet, iface="wlan0mon", count=10, inter=0.1)

from scapy.all import *

# 定义半导体常见的 Modbus TCP 探测逻辑 (模拟 SECS/GEM 的质询过程)
def compliance_inquiry(target_ip):
    # 构造一个非标准/畸形的质询封包 (Inquiry Packet)
    # 目的：测试设备是否会拒绝不符合合规契约的非法指令
    # 通过 Wireshark 官方提供的 ModbusTCP 样本封包（pcap文件），观察其十六进制流（Hex Stream），发现其报文头（MBAP Header）前 7 个字节有固定规律，从而学会了如何在 Scapy 中构造对应的 Raw(load=...)。
    # 在研究半导体 OT 资安时，我查阅了工业协议标准。了解到Modbus TCP 作为工业自动化中最基础的协议之一，其官方标准端口（Well-known Port）就是 502。虽然它很简单，但它能为我后续理解更复杂的半导体专用协议（如基于 TCP 的 HSMS/SECS-II）做基础。
    packet = IP(dst=target_ip)/TCP(dport=502)/Raw(load="\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00") #实际操作中需先完成三向握手或利用 Scapy 的StreamSocket模拟长连接，以符合半导体 HSMS 协议的连线状态要求。
    
    # 发送并等待响应
    response = sr1(packet, timeout=2, verbose=0)
    
    if response:
        # 逻辑：如果设备竟然执行了非法指令，说明其“合规防火墙”有漏洞
        print(f"警报：设备 {target_ip} 违反安全法规，执行了未授权质询！")
    else:
        # 逻辑：符合合规逻辑，设备拒绝了非授权访问
        print(f"通过：设备 {target_ip} 具备合规自卫能力。")

# Layer 5

# Layer 5 核心：会话属性与对话权控
# 既然 L4 搞定了同步与重传，L5 就要负责“会话权重”与“对话权限”管理
SESSION_ID = "NTPU-6G-TEST" 
SESSION_TOKEN = "AUTH-PRO-791"  # 扩充：L5 令牌。L4 链路通了不代表有权对话，确立会话级准入
session_counter = 0
MAX_PAYLOAD_SIZE = 100 
SESSION_PRIORITY = "HIGH"       # 扩充：会话优先级。用于 WMN 节点在拥塞时决定丢弃顺序

def send_layer5_packet(target, message):
    global session_counter
    
    # 逻辑增强：利用列表推导式物理切分指令
    chunks = [message[i:i + MAX_PAYLOAD_SIZE] for i in range(0, len(message), MAX_PAYLOAD_SIZE)]
    total_chunks = len(chunks)

    for index, chunk in enumerate(chunks):
        session_counter += 1
        
        # Layer 5 头部重构：[SID][TOKEN][PRIO][SEQ][FRAG]
        # 增加 PRIO：告知 WMN 节点此会话优先级，实现 QoS（服务质量）的会话级控制
        # 移除 L4 已有的 SYNC 逻辑，保持层级纯粹性，避免功能重叠
        l5_header = f"[{SESSION_ID}][{SESSION_TOKEN}][P:{SESSION_PRIORITY}][SEQ:{session_counter}][FRAG:{index+1}/{total_chunks}]"
        
        # 逻辑衔接：封装 L5 属性头部与原始切片
        combined_message = l5_header + chunk
        
        # 调用 Layer 3/4 函数，利用 L4 的重传机制保证送达
        send_covert_packet(target, combined_message)

    # 扩充：会话结束信号 (Dialog Unit End)
    # 作用：释放对话令牌 (Token)，允许对端发起反向请求，实现高效的半双工切换
    fin_signal = f"[{SESSION_ID}][{SESSION_TOKEN}][DIALOG:RELEASE]"
    send_covert_packet(target, fin_signal)

# 发送高优先级会话指令，测试 WMN 节点在压力下的优先级调度
send_layer5_packet(TARGET_IP, "RPG-791-HIGH-PRIORITY-TASK-SEQUENCE")
import base64
import zlib
from scapy.all import IP, UDP, send # 引入 Scapy 处理网络层和传输层封装

# Layer 6（表示层：加密与压缩）
def layer6_presentation(raw_data):
    # 压缩 (Compression)：针对 WMN 无线带宽优化，减少冗余
    compressed = zlib.compress(raw_data.encode())
    
    # 加密 (Encryption)：使用 XOR 模拟对称加密，确立安全边界
    key = 0x5A 
    # 逐字节异或处理，将压缩后的二进制流打乱
    encrypted = bytes([b ^ key for b in compressed])
    
    # 编码 (Encoding)：使用 Base64 将加密后的二进制转换为标准可见字符
    # 解决 Layer 5 在传输不可见字符时可能出现的乱码或丢包问题
    encoded_data = base64.b64encode(encrypted).decode()
    
    print(f"L6 Transform: {len(raw_data)}B -> {len(encoded_data)}B (Base64)")
    return encoded_data

# Layer 5的扩充部分，用于连接layer 5 和layer 6，这是layer 5 管理会话标签与数据分发的部分
def send_layer5_packet(target_ip, session_id, payload):
    # 在负载前缀加入 Session ID，用于对端识别会话流
    full_payload = f"SID:{session_id}|{payload}"
    
    # 使用 Scapy 构造 IP/UDP 协议栈，模拟真实网络环境下的数据封装
    # IP(dst) 定位目标主机，UDP(dport) 指定服务端口
    pkt = IP(dst=target_ip) / UDP(dport=5000) / full_payload
    
    # 发送构造好的原始数据包
    send(pkt, verbose=False)
    print(f"[L5] Session {session_id} packet sent to {target_ip}")

# 逻辑整合：将 L6 处理后的数据交给 L5 发送
def send_layer6_to_5_packet(target, original_msg):
    # 先进行 L6 的压缩、加密与编码处理
    secure_payload = layer6_presentation(original_msg)
    
    # 调用 L5 进行会话封装并发送
    # 设置固定的 Session ID 模拟当前通信会话
    send_layer5_packet(target, "1024", secure_payload)

# 调用测试
TARGET_IP = "192.168.1.100" 
send_layer6_to_5_packet(TARGET_IP, "CRITICAL_COMMAND_RFC791")


# Layer 7: 远程控制与遥测协议 (Remote Control Protocol)
from scapy.all import IP, UDP, Raw, send
import json
import time

# 我自学的 L7 应用层逻辑
def layer7_application_handler(action, params=None):
    # 查阅资料后，我决定用 JSON 格式，因为它在不同设备间通用性最强
    payload = {
        "timestamp": int(time.time()), # 学习 NTP 协议时发现时间戳能防重放攻击
        "action": action,
        "params": params or {},
        "version": "v1.0-test"
    }
    
    L7_data = json.dumps(payload)
    print(f" [L7] 构造指令: {action}")
    return L7_data

# L6 处理层：负责把文字转成机器能读的字节
def layer6_presentation(L7_data):
    # 这里是最关键的一步转换，Scapy 只能发送 bytes 类型
    L6_data = L7_data.encode('utf-8')
    return L6_data

# L5 & Scapy 发送逻辑
def send_packet_via_scapy(target, L6_data):
    # 这里参考了 Scapy 文档，把数据塞进 UDP 包
    # 我选择 UDP 是因为无人机通信需要低延迟
    packet = IP(dst=target) / UDP(dport=54321) / Raw(load=L6_data)
    
    print(f"[L5] 准备注入数据包至: {target}")
    send(packet, verbose=False) # verbose=False 优化了日志（log)输出，确保控制台只保留核心的协议交互记录。

# 模拟实验场景
TARGET_IP = "120.126.x.x" 
# 动作：获取无人机位置
L7 = layer7_application_handler("FETCH_POS", {"id": 791})
L6 = layer6_presentation(L7)
send_packet_via_scapy(TARGET_IP, L6)
