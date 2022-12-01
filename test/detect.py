# import face_recognition
import cv2
# import numpy as np
import knn
import os

import sys
sys.path.append("./../")
import db

TRAINING_IMAGES_FOLDER=os.getenv("IMAGES_FOLDER_NAME") or "TrainingImages"

def train():
    print("Training KNN classifier...")
    classifier = knn.train(TRAINING_IMAGES_FOLDER, model_save_path="trained_knn_model.clf")
    print("Training complete!")


def detect_faces():
    if "trained_knn_model.clf" not in os.listdir():
        train()
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    frame_count = {}
    FRAME_COUNT_THRESH = int(os.getenv('FRAME_COUNT_THRESH')) or 15
    database = db.Student()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            pred = knn.predfly(rgb_small_frame, model_path="trained_knn_model.clf")
        process_this_frame = not process_this_frame


        # Display the results
        for name,(top, right, bottom, left) in pred:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if not name in frame_count:
                frame_count[name]=0
            else:
                frame_count[name]+=1
                if frame_count[name]==FRAME_COUNT_THRESH:
                    database.markAttendance(name)
                    # print(f"{FRAME_COUNT_THRESH} frames for {name}")
                    frame_count[name]=0
                    prev = name.split("-")[0] + " has been recorded"

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    detect_faces()