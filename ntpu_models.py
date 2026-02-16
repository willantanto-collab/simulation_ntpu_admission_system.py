#project : NTPU Overseas Admission Analysis Engine
#Purpose : 为华侨生申请台北大学提供精准的加权计算与录取模拟
class Department:
  def __init__(self,name,threshold,code,score):
    self.name = name
    self.threshold = threshold
    self.code = code
    self.score = score
  def analyse_admission(self):
    margin = (self.score - self.threshold)/self.threshold #门槛，判断学生的成绩是否能进
    if margin >= 0.1: #超过10%
        return "稳定录取”
    elif margin >= 0: 
        return "录取概率高"
    else:
        return "存在风选，建议作为冲刺志向”


    
