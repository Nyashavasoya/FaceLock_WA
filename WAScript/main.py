import cv2
import face_recognition
import numpy as np
import os
import time
import pickle
import logging

# Set up logging to use the same file as encode_faces.py
logging.basicConfig(filename='detection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add a separator to indicate a new session
logging.info("------------------New logging session for face recognition ------------------")

logging.info("Face recognition script started...")

def load_encodings(encodings_file):
    """Load face encodings from a file."""
    with open(encodings_file, 'rb') as file:
        encodings = pickle.load(file)
    return encodings

# Load your face encodings
logging.info("Loading face encodings...")
encodings = load_encodings("face_encodings.pkl")

# Initialize the webcam
logging.info("Initializing webcam...")
video_capture = cv2.VideoCapture(0)

def detect_face():
    ret, frame = video_capture.read()
    if not ret:
        logging.error("Failed to capture image from webcam.")
        return False

    # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    logging.info(f"Found face locations: {face_locations}")

    # Find all face encodings in the current frame of video
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    logging.info(f"Found face encodings: {face_encodings}")

    for face_encoding in face_encodings:
        # Check if the face matches any of your saved encodings
        matches = face_recognition.compare_faces(encodings, face_encoding)
        if True in matches:
            return True
    return False

# Wait a few seconds to allow WhatsApp to open
time.sleep(5)
logging.info("Checking for face...")
if detect_face():
    logging.info("Face recognized! WhatsApp stays open.")
else:
    logging.info("Face not recognized! Closing WhatsApp.")
    os.system("taskkill /f /im WhatsApp.exe")

# Release the webcam
logging.info("Releasing webcam...")
video_capture.release()
cv2.destroyAllWindows()
