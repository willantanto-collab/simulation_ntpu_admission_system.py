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
