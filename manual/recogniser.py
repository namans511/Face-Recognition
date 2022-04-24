from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import dlib
import PIL.Image
import numpy as np
import face_recognition_models
import os
# import cv2

#importing dlib models
face_detector = dlib.get_frontal_face_detector()
predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor = dlib.shape_predictor(predictor_68_point_model)
face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

def get_face_locations(img):
    """
    Returns an array of bounding boxes of human faces in a image
    """
    return face_detector(img, 0)

def get_face_landmarks(img, face_locations=None):
    """
    Returns facial landmarks for all faces in the image
    """
    if face_locations is None:    
        face_locations = get_face_locations(img)

    return [pose_predictor(img, face_location) for face_location in face_locations]

def get_face_encodings(img, face_locations=None, face_landmarks=None):
    """
    Returns the 128-dimension face encoding for each face in the image.
    """
    if face_landmarks is None:
        face_landmarks = get_face_landmarks(img, face_locations)
    return [np.array(face_encoder.compute_face_descriptor(img, raw_landmark_set, 1)) for raw_landmark_set in face_landmarks]

def get_properties(img):
    """
    Returns face locations, landmarks and encodings
    """
    # print("lessgo")
    locations = get_face_locations(img)
    # print("location yes")
    landmarks = get_face_landmarks(img, locations)
    # print("landmark yes")
    encodings = get_face_encodings(img, face_locations=locations ,face_landmarks=landmarks)
    # print("we got em")
    return locations, landmarks, encodings

class FaceData:
    def __init__(self):
        self.encodings = []
        self.names = []

    def train(self, known_dir="known"):
        for file in os.listdir(known_dir):
            img = np.array(PIL.Image.open(known_dir + '/' + file))
            img_enc = get_face_encodings(img)
            if len(img_enc)>0:
                self.encodings.append(img_enc[0])
                self.names.append(file.split('.')[0])
    
    def add(self, encoding, name):
        self.encodings.append(encoding)
        self.names.append(name)

class Blink:
    def __init__(self, EYE_AR_THRESH, EYE_AR_CONSEC_FRAMES):
        self.EYE_AR_THRESH = EYE_AR_THRESH
        self.EYE_AR_CONSEC_FRAMES = EYE_AR_CONSEC_FRAMES
        self.blinks = {}

    def eye_aspect_ratio(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear

    def detect_blinks(self, frame, names, face_landmarks=None):
        lStart, lEnd = 42, 48
        rStart, rEnd = 36, 42
        blinked = [] #list of people who blinked

        if face_landmarks is None:
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_landmarks = get_face_landmarks(gray)
            
        # loop over the face landmarks
        for i in range(len(face_landmarks)):
            shape = face_utils.shape_to_np(face_landmarks[i])
            
            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < self.EYE_AR_THRESH:
                if names[i] not in self.blinks:
                    self.blinks[names[i]] = 1
                else:
                    self.blinks[names[i]]+= 1
            else:
                if names[i] in self.blinks and self.blinks[names[i]] >= self.EYE_AR_CONSEC_FRAMES:
                    blinked.append(names[i])
                self.blinks[names[i]] = 0
        #return list of people who blinked
        return blinked


    





