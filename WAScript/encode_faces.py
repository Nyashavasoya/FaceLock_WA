import cv2
import face_recognition
import numpy as np
import os
import pickle
import logging

# Set up logging to use the same file as main.py
logging.basicConfig(filename='combined.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add a separator to indicate a new session
logging.info("------------------New logging session for encoding ------------------")

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def encode_faces(image_folder, encodings_file):
    encodings = []
    images = load_images_from_folder(image_folder)
    for img in images:
        logging.info("Encoding image...")
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            # Find all face encodings in the image
            img_encodings = face_recognition.face_encodings(rgb_img)
            encodings.extend(img_encodings)
        except IndexError:
            logging.warning("No face found in the image.")

    # Save encodings to file
    with open(encodings_file, 'wb') as file:
        pickle.dump(encodings, file)
    logging.info(f"Encodings saved to {encodings_file}")

if __name__ == "__main__":
    # Specify the image folder and file to save encodings
    image_folder = "data"  # Folder where images are stored
    encodings_file = "face_encodings.pkl"  # File to save encodings
    encode_faces(image_folder, encodings_file)
