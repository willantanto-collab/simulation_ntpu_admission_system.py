#project : NTPU Overseas Admission Analysis Engine
#Purpose : 为华侨生申请台北大学提供精准的加权计算与录取模拟
import datetime

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
class NTPU_CSIE_Alevel_System(Department): #针对A level,3核心科目体系的质工系录取模拟
  def __init__(self,student_name,grades):
    self.student_name = student_name
    self.weights = {"Math":2.2,"CS":2.0,"Physics":1.8} #设定质工系特定权重
    analyser = Cambridge_Analyser(student_grades)
    final_score = analyser.calculate_weighted_score()
    super().__init__(name="台北大学质工系”，threshold=310,code = "CSIE",score=final_score) #继承
  def display_report(self):
    result = self.analyse_admission() 
    print(f"{datetime.date.today()} 申请人：{self.student_name}")
    print(f"计算得分：{self.score} 门槛：{self.threshold}")
    print(f"分析结果：{result}")

    
  
    
    
    

    
