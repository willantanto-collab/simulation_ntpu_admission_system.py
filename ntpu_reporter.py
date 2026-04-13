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
