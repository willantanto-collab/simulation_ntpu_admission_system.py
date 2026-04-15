# -*- coding: utf-8 -*-
from datetime import datetime

class TimelineManager:
    # 负责监控申请进度与关键节点的时间差。
    # 展示了开发者对项目管理逻辑和 Python 时间库的应用能力
    def __init__(self):
        # 预设申请过程中的关键时间点 (ISO 格式)
        self.deadlines = {
            "Early_Action": "2026-11-01",
            "Regular_Decision": "2027-01-05",
            "Scholarship_Application": "2026-12-01"
        }
    def get_days_remaining(self, stage_name):
        # 计算距离指定截止日期还有多少天。
        if stage_name not in self.deadlines:
            return None
        
        target_date = datetime.strptime(self.deadlines[stage_name], "%Y-%m-%d")  #strptime,复习python 官方文件的时候，有写。
        today = datetime.now()
        
        # 计算差值并返回天数
        delta = target_date - today
        return delta.days   

    def check_urgency(self, stage_name):
        # 根据剩余天数判断紧急程度。
        days = self.get_days_remaining(stage_name)
        if days is None: 
          return "Unknown"
        if days < 7: 
          return "CRITICAL"
        if days < 30: 
          return "URGENT"
        return "NORMAL"
    def is_missed(self, stage_name):
        # 增加"过期判定"逻辑
        days = self.get_days_remaining(stage_name)
        if days is not None and days < 0:
            return True
        return False
if __name__ == "__main__": #我在看其他人github 写的代码的时候，看到了这一行。搜索后知道，这一行是专业代码的‘标配’
   # 效果是它能防止代码在 import 时产生其他风险。我觉得这种逻辑隔离非常严谨，就把它应用到了我的项目中。
    tm = TimelineManager()
    days_left = tm.get_days_remaining("Regular_Decision")
    status = tm.check_urgency("Regular_Decision")
    print(f"Deadline Status: {days_left} days left [{status}]")
    if tm.is_missed("Regular_Decision"):
        print("This deadline has already passed.")



