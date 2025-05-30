# Smart feedback module

def get_feedback(knee_angle, back_angle):
    feedback = []
    if knee_angle < 80:
        feedback.append("Try to squat lower.")
    elif knee_angle > 110:
        feedback.append("Don't go too deep — protect your knees.")

    if back_angle > 20:
        feedback.append("Keep your back straighter.")

    return " ".join(feedback) if feedback else "Great form!"
