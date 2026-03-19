#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 以上两行，我在 GitHub 上看一些开源的网络安全项目（比如 Scapy 的官方文档或相关的网络工具）时，发现其他代码写的厉害的文件开头都有这两行。
# 我查了一下，发现这是为了在 Linux 环境下能直接运行，并且让中文注释不乱码，所以我专门在平板上手打加了进去。
# 我之前写的scapy 在algorithm.py 那个文件实现仅能识别攻击类型，但在 WNM Lab 的研究中，
# 我发现陈教授的论文中提到攻击源的“网络拓扑位置” (Hop count) 
# 我看不懂那么多，但是我在学习 Scapy 的 IP() 类时，产生了一个疑问：为什么它会有 ttl, tos, flags 这些字段？还有这些名字是谁定义的？
# 于是我顺着 Scapy 的官方文档去搜了 IPv4 Standard，最终锁定了互联网协议的—— RFC 791
# 因此引入 RFC 791 的 TTL 逻辑进行优化。
# 自学来自网站 WireShark Scapy
def trace_packet(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP): # 检查包有没有 IP 层和 TCP 层
        src_ip = packet[IP].src  # 拿到发件人的 IP 地址 (src 就是 Source)
        ttl_value = packet[IP].ttl  # 拿到这个包的寿命 TTL。我查了 RFC 791，这是 IP 协议里专门管“生存时间”的
        if packet[TCP].flags == "S": # 如果 TCP 标志位是 "S" (SYN)，说明对方想跟我建立连接，这常被黑客用来扫描
            # 【我的发现】：为什么用 64 减？那是因为我查到大多数 Linux 初始 TTL 是 64。
            # 减出来的数字就是这个包一路上“跳”过了多少台路由器。
            # 这个数字能帮我判断黑客离我有多远，是陈教授 WNM 实验室很看重的“拓扑位置”
            print(f"Source: {src_ip}, Distance between router is {64 - ttl_value} jumps") 
def forensic_check_layer4(packet)： # 调研陈教授Life Lab后，将逻辑重构为“数字鉴识”(Forensics) 检查
    #针对Layer 4 判定“意图”与“响应”
    #S = 侵入企图 (SYN)；SA = 目标响应 (SYN-ACK)
  if packet.haslayer(scapy.TCP): # 过滤 Layer 4 传输层：确保后续操作聚焦于 TCP 协议逻辑
    flags = packet[scapy.TCP].flags # 提取封包控制标志位：获取 SYN/ACK 等意图判定的核心元数据（metadata)
    # 核心判定：如果只有 SYN，代表扫描或企图侵入
    if flags == "S":
      return "检测到SYN扫描:法律判定为“侵入企图”"
    elif flags == "SA":
      return "检测到SYN-ACK:目标响应，连接正在建立"
    elif flags == "A": # ACK：标志三次握手完成，连接进入“实质侵害”阶段
      return "检测到 ACK:连接已建立，法律判定为”实质侵入”"
    return "非 TCP 关键封包" #默认返回：过滤非握手阶段的背景流量，确保鉴识逻辑的精准度from scapy.all import *
from scapy.all import *
import time

# 定义合法访问的白名单（模拟台积电内部受保护网段）
AUTHORIZED_IPS = ["192.168.1.100", "192.168.1.101"]

# 【状态审计池】用于记录每个 IP 的 SYN 请求频率，识别意图
# 真正的 Layer 4 审计必须具备“记忆”，才能分辨请求还是攻击
connection_history = {} 

def compliance_audit_sniffer(packet):
    if packet.haslayer(TCP) and packet[TCP].flags == 'S':
        ip_src = packet[IP].src
        now = time.time()
        
        # 意图审查 (Intent Audit)
        # Compliance Check，违反越权访问规制
        if ip_src not in AUTHORIZED_IPS:
            print(f"[警告] 非法入侵企图：源 IP {ip_src} 试图发起未经授权的入场请求。")
        else:
            print(f"[审计] 合法连接请求：源 {ip_src} 正在履行准入协议。")

        # 可用性保护 (Availability Protection)
        # 核心逻辑：如果同一源短时间内发送大量 SYN，判定为“架构滥用”
        history = connection_history.get(ip_src, [])
        history = [t for t in history if now - t < 1.0] # 仅保留 1 秒内的记录
        history.append(now)
        connection_history[ip_src] = history

        if len(history) > 10:
            # 这里的逻辑：代码即法律，当请求频率超出架构承载力，即判定为拒绝服务攻击风险
            print(f"[致命风险] 检测到 SYN Flood：源 {ip_src} 频率过高，正在消耗系统资源！")

# 启动针对 WMN Lab 环境的合规监控
print("正在执行 Layer 4 协议合规性实时审计...")
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


from scapy.all import *
def cross_layer_analysis(pkt): # pkt = packet
    #抓取 RadioTap 头部，获取 Layer 2的物理层链路强度 (RSSI)
    if pkt.haslayer(RadioTap):
        #rssi_value 提取自 RadioTap 层，是设备的信号强度 (单位为 dBm)
        rssi_value = pkt.dBm_AntSignal 
        
        # 提取 TCP 拥塞控制的表征——窗口大小
        if pkt.haslayer(TCP) and rssi_value is not None:
            tcp_window = pkt[TCP].window
            src_ip = pkt[IP].src       
            
            # 控制台实时验证：观测RSSI下降与TCP窗口的协同变化
            print(f"[Link-Awareness Test] Source: {src_ip}")
            print(f"  Layer 2 (RSSI): {rssi_value} dBm")
            print(f"  Layer 4 (TCP Win): {tcp_window}")            
            
            #实验观测记录逻辑：dBm 为负值，-75 比 -40 更弱
            if rssi_value < -70: 
                print("链路质量劣化：RSSI 跌至阈值以下。")
                if tcp_window < 1000: # 假设观测到窗口剧烈收缩
                    print("验证成功：TCP 表现过于‘保守’，误将链路损耗判定为网络拥塞。\n")
# 启动监听，需网卡支持 Monitor Mode
# store=0 确保长时间实验不会占用过多平板/电脑内存
sniff(iface="wlan0mon", prn=cross_layer_analysis, store=0) #prn 是一个回调函数

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

# 定义会话状态，L5 的核心就是知道现在是谁在对话，对话到第几次了
SESSION_ID = "NTPU-6G-TEST" 
session_counter = 0
MAX_PAYLOAD_SIZE = 100  # 设定载荷上限，既然单包容易丢，那就手动给它做分片

def send_layer5_packet(target, message):
    global session_counter
    
    # 逻辑增强：利用列表推导式把一串长指令物理切分
    # 这种“切片”思路类似于物理时学到的拆分位移是一样的，化整为零才好控制
    chunks = [message[i:i + MAX_PAYLOAD_SIZE] for i in range(0, len(message), MAX_PAYLOAD_SIZE)]
    total_chunks = len(chunks)

    for index, chunk in enumerate(chunks):
        session_counter += 1
        
        # Layer 5 头部增强：增加 [FRAG:当前片/总片数]
        # 作用：接收方拿到后可以根据这个标识进行数据重组，确保长指令的完整性
        l5_header = f"[{SESSION_ID}][SEQ:{session_counter}][FRAG:{index+1}/{total_chunks}]"
        
        # 逻辑衔接：将增强后的 L5 头部与切片数据拼接
        combined_message = l5_header + chunk
        
        # 调用之前我写好的 Layer 3/4 函数，层级封装逻辑依然稳固
        send_covert_packet(target, combined_message)

# 发送带分片标识的指令，测试这种“分段轰炸”的稳定性
send_layer5_packet(TARGET_IP, "RPG-791-SYNC-SEQUENCE-VERIFICATION")


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
import time
import json #在处理 L7 业务指令时，我意识到零散的字符串难以扩展，于是通过搜索‘结构化数据传输标准’发现了 JSON。
# 它能像容器一样把复杂的指令参数（如坐标、指令名、时间戳）打包成一个标准化的对象，完美衔接了 L7 语义逻辑与 L6 的二进制压缩。

# 功能：定义具体的业务语义（如：获取坐标、控制电机、心跳检测）
# 特点：将结构化数据（JSON）转为字符串，对接 L6 转换

def layer7_application_handler(action, params=None): #params,parameter 的意思
    # 模拟一个无人机/物联网节点的应用层指令
    
    # 构造应用层报文格式（协议头 + 载荷）
    payload = {
        "timestamp": int(time.time()), #实现时钟同步、防止重放攻击。在学习NTP（网络时间协议）或TCP握手时，我频繁看到Timestamp的身影
        "action": action,
        "params": params or {}， #变成{} 也就是none,原因是为了减少在抓取不到目标是产生错误（error)
        "app_version": "WMN-1.0-DEV"
    }
    
    #将目标对象转为 JSON 字符串，准备交给 L6 压缩和 L5 会话
    app_data = json.dumps(payload) #在 L7 采用了 JSON 序列化方案，这确保了协议的跨平台兼容性（Cross-platform Interoperability），为未来在不同架构的嵌入式硬件之间进行异构通信打下了基础
    # Dump 是将内存中的复杂数据瞬间“倒”出来变成一种可持久化或可传输的格式。
    print(f"[L7] Generating Command: {action}")
    return app_data

def send_full_stack_packet(target, action, params=None):
    
    # L7 产生原始指令数据
    L7_data = layer7_application_handler(action, params)
    
    # L6 进行压缩、XOR加密、Base64编码，调用我之前写的代码)
    L6_data = layer6_presentation(L7_data)
    
    # L5 注入会话ID和序列号，调用我之前写的代码)
    # 最终通过Scapy发送 ICMP/UDP隐蔽隧道包
    send_layer5_packet(target, l6_data)

# 场景：向实验室网关发送一个获取“无人机群实时位置”的请求
TARGET_IP = "120.126.x.x" # 台北大学网段
send_full_stack_packet(TARGET_IP, "FETCH_DRONE_POS", {"drone_id": 791, "range": 500})

#场景：模拟传感器阈值报警
send_full_stack_packet(TARGET_IP, "ALERT_OVERHEAT", {"temp": 85.5, "unit": "Celsius"})

