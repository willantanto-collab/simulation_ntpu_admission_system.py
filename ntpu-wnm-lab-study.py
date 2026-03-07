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
import time
TARGET_IP = "192.168.1.100"  # 模拟的IoT网关地址
SECRET_DATA = "PROMPT_ID_791:ACTION_BYPASS_LEGAL_FILTER" # 模拟一段经过“质询工程”处理后的法律存证
def send_covert_packet(target, message):
    print(f"正在通过 Layer 3 协议向 {target} 发送隐蔽数据...")
    # 构造 IP 层 (Layer 3)
    # 初始化 IPv4 报头 (符合 RFC 791 标准)
    # 在 6G/IoT 仿真中，该字段用于标识边缘计算节点或受控终端
    ip_layer = IP(dst=target)  # dst (Destination Address): 目标 IP 字段，决定了 Layer 3 路由的终点

    #协议封装逻辑 (Protocol Stack Construction)
    # 利用 Scapy 的层叠操作符 (/) 构造非标准协议栈
    # Layer 3 (IP）： 处理寻址与路由
    # Layer 3.5 (ICMP)： 绕过 Layer 4 (TCP) 的三次握手损耗
    # Payload (Raw Data)： 将 6G 存证指令 (RPG-791) 注入 ICMP 载荷区，实现极简信令传输
    icmp_packet = ip_layer / ICMP() / message 

    # 执行 Layer 3 原始套接字注入 (Raw Socket Injection)
    # 绕过系统标准传输层规制，直接将封装好的 ICMP 帧投递至链路层
    # verbose=False: 减少 I/O 开销，适用于 6G 边缘节点的高频信令仿真
    # 发送数据包
    #"Sent 1 packets"，查阅Scapy官方help(send)确认verbose参数控制输出
    # 运行这个使用的工具：Python IDE
    # 发现过程：while循环模拟6G心跳时，控制台被"Sent 1 packets"刷屏，导致无法观察L3载荷。
    # 解决逻辑：在终端输入 help(send) 查阅函数定义，发现 verbose 参数默认为开启，平板设为 False 以保持控制台整洁
    send(icmp_packet, verbose=False)
    print(f"数据包已发出，载荷长度: {len(message)} bytes") # 通过Wireshark观察到Data字段动态变化，故用Python内置len()实时监控L3载荷大小以评估通信效率
if __name__ == "__main__":
    # 模拟 RPG 791 项目中的自动化质询指令发送
    print("NTPU WMN Lab 模拟环境(RPG-791)")
    try:
        while True:
            send_covert_packet(TARGET_IP, SECRET_DATA)
            # 设置 5 秒实验间隔。源于平板运行环境的性能限制，且为了手动对齐 Wireshark 抓包序列与代码输出，确保能逐帧分析 L3 字段
            time.sleep(5)  #实现非连续性信令传输 (Asynchronous Signaling)，模拟 6G/IoT 低功耗模式下的“心跳频率”
    except KeyboardInterrupt: # 针对平板(Pydroid 3等)运行环境，捕获点击停止按钮产生的信号，避免控制台弹出一整屏红色的报错代码
        print("\n 实验停止")

