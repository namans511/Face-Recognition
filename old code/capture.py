import cv2
import time
from blink2 import Blink

prev_frame_time = 0
new_frame_time = 0
#----------

blink = Blink(0.3, 3)

vid = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while True:
    new_frame_time=time.time()

    ret, frame = vid.read()
    frame = cv2.resize(frame, (500, 300))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    #----------------calculating fps
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps=str(int(fps))
    cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

    if blink.detect_blink(frame):
        print("blink boss")

    cv2.imshow('frame', frame)

    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()