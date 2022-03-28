import face_recognition
import os
import numpy as np
import db as database

class FaceRecognition:

    def __init__(self):
        self.encodings = []
        self.names = []
        self.names,self.encodings = database.getEncodings()

    def train(self, known_dir="known"):
        for file in os.listdir(known_dir):
            img = face_recognition.load_image_file(known_dir + '/' + file)
            img_encoding = face_recognition.face_encodings(img)[0]
            name = file.split('.')[0]
            self.encodings.append(img_encoding)
            self.names.append(name)
            database.saveEncoding(name, img_encoding)

    def recognise(self, img):
        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.names[best_match_index]

            face_names.append(name)

        return face_locations, face_names

if __name__ == '__main__':
    print("class me bhi chalta hai")
