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
class AdmissionAnalyser:  #通用录取分析，确保逻辑链可扩展
  def __init__(self,grades):
    self.grades = grades
    self.num_subjects = totalsubjects
  def calculate_weighted_score(self): #通用台北大学可判断的统一成绩，含金量之类的
    #实现具体的加权计算
    pass
class Cambridge_Analyser(AdmissionAnalyser):  #具体cambridge 的
  def calculate_weighted_score(self):
    if len(self.grades) != self.num_subjects: #确认考生成绩个数和科目数量是否对的上
      return "错误：填入成绩数与声明科目数不符”
    actual_total = sum(self.grades)
    average_score = actual_total /self.num_subjects
    diffciulty_weight = 1.05 #每年可更改，不同的含金量系数
    unified_score = average_score * difficulty_weight #通用台北大学判断的统一成绩
    return unified_score
    
    

    
