from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import numpy as np
import time
import dlib
import cv2
import face_recognition_models

class Blink:
    def __init__(self, EYE_AR_THRESH, EYE_AR_CONSEC_FRAMES):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
        self.EYE_AR_THRESH = EYE_AR_THRESH
        self.EYE_AR_CONSEC_FRAMES = EYE_AR_CONSEC_FRAMES
        self.counter = 0

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

    def detect_blink(self, frame):
        lStart, lEnd = 42, 48
        rStart, rEnd = 36, 42

        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects = self.detector(gray, 0)

            
        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            
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
                self.counter += 1
            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if self.counter >= self.EYE_AR_CONSEC_FRAMES:
                    self.counter = 0
                    return True
                self.counter=0
        return False

    def detect(self, show_fps=False):
        # initialize the frame counters and the total number of blinks
        COUNTER = 0
        TOTAL = 0

        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        # start the video stream thread
        print("[INFO] starting video stream thread...")
        vs = VideoStream(src=0).start()
        time.sleep(1.0)


        #---------
        prev_frame_time = 0
        new_frame_time = 0
        #----------

        # loop over frames from the video stream
        while True:
            new_frame_time = time.time()
            

            # grab the frame from the threaded video file stream, resize
            # it, and convert it to grayscale
            # channels)
            frame = vs.read()
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # detect faces in the grayscale frame
            rects = self.detector(gray, 0)

            
            # loop over the face detections
            for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = self.eye_aspect_ratio(leftEye)
                rightEAR = self.eye_aspect_ratio(rightEye)
                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0


                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                if ear < self.EYE_AR_THRESH:
                    COUNTER += 1
                # otherwise, the eye aspect ratio is not below the blink
                # threshold
                else:
                    # if the eyes were closed for a sufficient number of
                    # then increment the total number of blinks
                    if COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                        TOTAL += 1
                    # reset the eye frame counter
                    COUNTER = 0

                # draw the total number of blinks on the frame along with
                # the computed eye aspect ratio for the frame
                cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


            #----------------calculating fps
            if show_fps:
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                fps="FPS="+str(int(fps))
                cv2.putText(frame, fps, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)


        
            # show the frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
        
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

if __name__ == "__main__" :
    blink = Blink(0.3, 3)
    blink.detect()