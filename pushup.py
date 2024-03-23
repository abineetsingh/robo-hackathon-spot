import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

def is_pushup(landmarks):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    
    # Check if the person is in a plank position
    if left_shoulder.y > left_elbow.y and right_shoulder.y > right_elbow.y:
        # Check if the elbows are bent
        if left_elbow.y < left_shoulder.y and right_elbow.y < right_shoulder.y:
            # Check if the wrists are below the shoulders
            if left_wrist.y > left_shoulder.y and right_wrist.y > right_shoulder.y:
                return True
    
    return False

def analyze_pushup_pose(landmarks):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    
    feedback = "To improve your push-up pose, try the following:\n"
    
    # Check if the hands are wider than shoulder-width apart
    if left_wrist.x < left_shoulder.x - 0.1 or right_wrist.x > right_shoulder.x + 0.1:
        feedback += "- Place your hands slightly wider than shoulder-width apart for better stability.\n"
    
    # Check if the body is in a straight line
    if abs(left_shoulder.y - left_hip.y) > 0.1 or abs(right_shoulder.y - right_hip.y) > 0.1:
        feedback += "- Keep your body in a straight line from head to heels, engaging your core muscles.\n"
    
    # Check if the elbows are close to the body
    if left_elbow.x < left_shoulder.x - 0.1 or right_elbow.x > right_shoulder.x + 0.1:
        feedback += "- Keep your elbows close to your body as you lower down, tucking them in at about a 45-degree angle.\n"
    
    # Check if the chest is lowered close to the ground
    if left_shoulder.y > left_wrist.y + 0.2 or right_shoulder.y > right_wrist.y + 0.2:
        feedback += "- Lower your chest closer to the ground, aiming to bring it just a few inches off the surface.\n"
    
    # Check if the arms are fully extended at the top
    if left_elbow.y > left_shoulder.y - 0.1 or right_elbow.y > right_shoulder.y - 0.1:
        feedback += "- Fully extend your arms at the top of the push-up, pushing your body back up to the starting position.\n"
    
    return feedback

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    return file_path

def main():
    # Prompt the user to select an image file
    image_path = select_image()
    
    if image_path:
        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe Pose
        results = pose.process(image_rgb)

        # Initialize the feedback variable
        feedback = ""

        # Check if pose landmarks are detected
        if results.pose_landmarks:
            # Get the pose landmarks
            landmarks = results.pose_landmarks.landmark
            
            # Check if the person is doing a push-up
            if is_pushup(landmarks):
                # Analyze the push-up pose and provide feedback
                feedback = analyze_pushup_pose(landmarks)
            else:
                feedback = "It seems like you are not currently in a push-up pose. To perform a proper push-up, follow these steps:\n"
                feedback += "1. Start in a high plank position with your hands slightly wider than shoulder-width apart and your feet together.\n"
                feedback += "2. Keep your body in a straight line from head to heels, engaging your core muscles.\n"
                feedback += "3. Lower your body towards the ground by bending your elbows, keeping them close to your body.\n"
                feedback += "4. Lower your chest until it nearly touches the ground, maintaining a straight body line.\n"
                feedback += "5. Push your body back up to the starting position by extending your arms, keeping your body straight throughout the movement.\n"
                feedback += "6. Repeat for the desired number of repetitions."
        else:
            feedback = "No person detected in the image. Please make sure you are visible in the frame."

        # Display the feedback
        print(feedback)

        # Draw the landmarks and connections on the image
        mp_drawing = mp.solutions.drawing_utils
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the image
        cv2.imshow('Push-up Analysis', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No image selected. Exiting the program.")

if __name__ == "__main__":
    main()
