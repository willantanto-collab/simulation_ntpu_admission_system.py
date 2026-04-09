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

# Example usage for even 1 hour study
my_app = AdmissionCalculator(gpa=3.5)
chance = my_app.get_admission_probability(study_hours=1)

print("NTPU Admission Simulation Results")
print(f"Study Input: 1 hour")
print(f"Admission Probability: {chance}%")

if chance < 70:
    print("Action: Increase study intensity.")
else:
    print("Status: On track.")
