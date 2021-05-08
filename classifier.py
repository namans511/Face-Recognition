import numpy as np
from sklearn import svm

class Classify:
    def __init__(self):
        pass

    def face_distance(self, face_encodings, face_to_compare):
        """
        Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
        """
        if len(face_encodings) == 0:
            return np.empty((0))
        return np.linalg.norm(face_encodings - face_to_compare, axis=1)

    def compare_faces(self, known_face_encodings, new_face_encoding, tolerance=0.6):
        """
        Compare a list of face encodings against a candidate encoding to see if they match.
        """
        return list(face_distance(known_face_encodings, new_face_encoding) <= tolerance)

    def recognise(self, FaceData, face_encodings, tolerance=0.6):
        face_names = []
        # print(len(FaceData.encodings))
        for face_encoding in face_encodings:
            name = "Unknown"
            enco = FaceData.encodings
            face_distances = self.face_distance(enco, face_encoding)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] <= tolerance:
                name = FaceData.names[best_match_index]

            face_names.append(name)

        return face_names


    def create_svm_classfier(self, FaceData):
        self.clf = svm.SVC(gamma='scale')
        self.clf.fit(FaceData.encodings, FaceData.names)

    def svm_predict(self, encoding):
        if not encoding:
            return []
        name = self.clf.predict(encoding)
        return name
