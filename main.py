import cv2
import recogniser as rc
import classifier as clf
import attendance

atten = attendance.Attendance()

def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

video_capture = cv2.VideoCapture(0)

#IMPORTING MODEL AND TRAINING
#----------------------------
face_data = rc.FaceData()
print("training start")
face_data.train()
print("training done")
#----------------------------
blink = rc.Blink(0.3, 3)
blink_count=0
cf = clf.Classify()
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # rgb_small_frame = small_frame[..., :, ::-1]
    # rbg_small_frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # print("here6969")
    locations, landmarks, encodings = rc.get_properties(small_frame)
    # print("here")
    face_names = cf.recognise(face_data, encodings)
    face_locations = [_rect_to_css(face) for face in locations]
    # #processing every other frame
    # if process_this_frame:
    #     face_locations, face_names = face_req.recognise(rgb_small_frame)

    no_blinks = blink.detect_blinks(small_frame, face_names, face_landmarks=landmarks)
    atten.mark(no_blinks)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()