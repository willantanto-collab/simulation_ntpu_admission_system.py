class AdmissionCalculator:
    def __init__(self, gpa):
        self.gpa = gpa
        self.base_chance = (gpa / 4.0) * 50

    def get_admission_probability(self, study_hours):
        # Every hour adds 2%
        total = self.base_chance + (study_hours * 2)
        
        if total > 99:
            return 99.0
        return total
    def check_scholarship(self, chance):
        # 基于 GPA 和录取概率综合判断奖学金
        if self.gpa >= 3.8 and chance > 80:
            return "Eligible for Full Scholarship"
        elif self.gpa >= 3.5:
            return "Eligible for Partial Scholarship"
        return "No scholarship available at this level."
    def get_interview_boost(self, interview_score):
        #面试表现加分 (0-10分)
        return interview_score * 0.5
    def simulate_decision(self, chance): 
        return random.uniform(chance - 5, chance + 5) >= 75  # 模拟含随机波动的最终录取决策
    def get_safety_status(self, chance)
        if chance >= 90: return "Safety"       # 保底
        if chance >= 70: return "Target"       # 核心目标
        if chance >= 50: return "Reach"        # 冲刺
        return "Unlikely"                      # 极难

# Example usage for even 1 hour study
my_app = AdmissionCalculator(gpa=3.5)
chance = my_app.get_admission_probability(study_hours=1)

# 获取奖学金状态
scholarship_status = my_app.check_scholarship(chance)
print("NTPU Admission Simulation Results")
print(f"Study Input: 1 hour")
print(f"Admission Probability: {chance}%")

if chance < 70:
    print("Action: Increase study intensity.")
else:
    print("Status: On track.")

# 面试分数例子
interview_score = 8.5 
boost = my_app.get_interview_boost(interview_score)

# 计算最终总概率 (原有概率 + 面试加分）
final_chance = min(99.0, chance + boost)

print(f"Interview Score: {interview_score}/10")
print(f"Interview Boost: +{boost}%")
print(f"Scholarship Eligibility: {scholarship_status}")

