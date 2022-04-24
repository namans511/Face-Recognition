import cv2
from FaceRecognition import FaceRecognition
from blink2 import Blink
import db

video_capture = cv2.VideoCapture(0)

#IMPORTING MODEL AND TRAINING
#----------------------------
face_req = FaceRecognition()
print("training start")
face_req.train()
print("training done")
#----------------------------

# blink = Blink(0.3, 3)
# blink_count=0

process_this_frame = True

frame_count = {}
FRAME_COUNT_THRESH = 15
database = db.Student()

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.20, fy=0.20)
    rgb_small_frame = small_frame[:, :, ::-1]

    #processing every other frame
    if process_this_frame:
        face_locations, face_names = face_req.recognise(rgb_small_frame)
        
    process_this_frame = not process_this_frame
    # did_blink = blink.detect_blink(frame)
    # if did_blink:
    #     blink_count+=1
    #     print("human detected", blink_count)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 5
        right *= 5
        bottom *= 5
        left *= 5

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        if not name in frame_count:
            frame_count[name]=0
        else:
            frame_count[name]+=1
            if frame_count[name]==FRAME_COUNT_THRESH:
                database.markAttendance(name)
                print(f"{FRAME_COUNT_THRESH} frames for {name}")
                frame_count[name]=0



    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()