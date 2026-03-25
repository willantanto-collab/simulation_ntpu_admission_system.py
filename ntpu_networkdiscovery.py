# 自学笔记：从 RFC 官方文件到 Scapy 的二层实现
# 我在研究 Wireshark 抓包时发现，即使在线节点屏蔽了 Ping (ICMP)，它也必须服从 ARP 协议的“局域网法律”才可以流量交互。
# 为了验证 Lessig "Code is Law" 的理念，我翻阅了 Scapy 官方文档中极简的 'Stacking Layers' 章节。
# 我通过 ls(ARP) 命令摸清了字段，并查阅 RFC 官方文件实测证实了广播地址必须设为 ff:ff:ff:ff:ff:ff。

from scapy.all import ARP, Ether, srp

def arp_scan(ip_range):
    # 准专业工具：局域网活动主机扫描
    # 原理：构造二层以太网帧，封装ARP请求，获取MAC地址
    # 构造以太网广播包
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # 构造ARP请求包
    arp = ARP(pdst=ip_range)
    # 组合包
    packet = ether/arp

    # 发送并接收响应 (timeout为等待时间，verbose=False隐藏冗余输出)
    result = srp(packet, timeout=3, verbose=False)[0]

    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return clients
