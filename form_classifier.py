# Placeholder for form classification model (future feature)
# You can collect joint angle data and train a classifier to distinguish good vs. bad reps

def classify_form(knee_angle, hip_angle, back_angle):
    if 80 <= knee_angle <= 100 and back_angle < 15:
        return "Good", 1
    else:
        return "Needs Improvement", 0
