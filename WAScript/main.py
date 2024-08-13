import cv2
import face_recognition
import numpy as np
import os
import time

print("Face recognition script started...")


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


def encode_faces(image_folder):
    encodings = []
    images = load_images_from_folder(image_folder)
    for img in images:
        print("Encoding image...")
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            # Find all face encodings in the image
            img_encodings = face_recognition.face_encodings(rgb_img)
            encodings.extend(img_encodings)
        except IndexError:
            print("No face found in the image.")
    return encodings


# Load your face encodings
print("Loading face encodings...")
encodings = encode_faces("data")

# Initialize the webcam
print("Initializing webcam...")
video_capture = cv2.VideoCapture(0)


def detect_face():
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture image from webcam.")
        return False

    # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    print("Found face locations:", face_locations)

    # Find all face encodings in the current frame of video
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    print("Found face encodings:", face_encodings)

    for face_encoding in face_encodings:
        # Check if the face matches any of your saved encodings
        matches = face_recognition.compare_faces(encodings, face_encoding)
        if True in matches:
            return True
    return False


# Wait a few seconds to allow WhatsApp to open
time.sleep(5)
print("Checking for face...")
if detect_face():
    print("Face recognized! WhatsApp stays open.")
else:
    print("Face not recognized! Closing WhatsApp.")
    os.system("taskkill /f /im WhatsApp.exe")

# Release the webcam
print("Releasing webcam...")
video_capture.release()
cv2.destroyAllWindows()