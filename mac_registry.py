# A-Level 9618 Revision: String Manipulation & Dictionary Searching
# 理由：为了在 A-Level Prelim 前复习字符串切片和字典匹配，我写了这个厂商识别逻辑
# 与此同时，我在家里和同学用的这些设备的品牌有些了解，打算写这一部分的python 和复习CS A level 的即将到来的考试做练习。
# 这一部分是打算复习和练习Paper 4 的 Dictionary { } 和 String Slicing [ : ]
class VendorLookup:
    def __init__(self):
      self.devices = {"14:48:BB": "Apple_iPhone_XR", "BC:D1:1F": "Xiaomi_Router","8C:DE:F9": "Huawei_Tablet","00:00:00":"Unknown Device"}
