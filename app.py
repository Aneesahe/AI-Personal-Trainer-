# AI-Powered Personal Trainer using Streamlit and Mediapipe (Smart Version)

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# Setup Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate angle between joints
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Function to score squat form
def score_squat(angle):
    if 80 <= angle <= 100:
        return 100, "Perfect form!"
    elif 70 <= angle < 80 or 100 < angle <= 110:
        return 75, "Almost there — adjust your depth."
    else:
        return 50, "Too shallow or too deep. Try a better angle."

# Streamlit App
st.title("🤖 AI-Powered Personal Trainer (Smart)")
st.markdown("This app counts your squats in real-time, scores your form, and gives live feedback using your webcam.")

run = st.checkbox('Start Camera')

counter = 0
stage = None
score_display = 0
feedback = ""

if run:
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                # Calculate angle
                angle = calculate_angle(hip, knee, ankle)
                score_display, feedback = score_squat(angle)

                # Rep counting logic
                if angle > 160:
                    stage = "up"
                if angle < 90 and stage == 'up':
                    stage = "down"
                    counter += 1

                # Display angle
                cv2.putText(image, f"Angle: {round(angle, 1)}", (400, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass

            # Render squat counter and score
            cv2.rectangle(image, (0,0), (300,90), (245,117,16), -1)
            cv2.putText(image, 'REPS', (15,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10,70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, 'FORM SCORE', (100,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(score_display), (120,70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)

            # Draw pose landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Streamlit image feed
            st.image(image, channels="BGR")
            st.success(feedback)

            if st.button("Stop Camera"):
                break

        cap.release()
        cv2.destroyAllWindows()

else:
    st.info("Click the checkbox above to start your smart AI workout!")
