# import csv
import cv2
import os
import face_recognition
import shutil


# counting the numbers

TRAINING_IMAGES_FOLDER=os.getenv("IMAGES_FOLDER_NAME") or "TrainingImages"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



# Take image function

def takeImages(Id=None,name=None):

    if name is None:
        name = input("enter name:")
    if Id is None:
        Id = input("enter Id: ")
    print(name,Id)

    
    # harcascadePath = "haarcascade_frontalface_default.xml"
    # detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    SAMPLE_SIZE = int(os.getenv('SAMPLE_SIZE')) or 1
    std_folder_name = name+"_"+Id
    flag = checkDir(std_folder_name)
    cam = cv2.VideoCapture(0)
    imgs = []
    while(flag):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(gray)
        print(faces)

        for (top, right, bottom, left) in faces:
            #drawing rectangles around faces
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                        
            #saving the captured face in the dataset folder TrainingImage
            imgs.append(img[top:bottom, left:right])
            # cv2.imwrite(TRAINING_IMAGES_FOLDER + os.sep + std_folder_name+os.sep+str(name) + "_"+str(Id) + '.' + str(sampleNum) + ".jpg", gray[top:bottom, left:right])

            #incrementing sample number
            sampleNum = sampleNum+1

        
        #display the frame
        cv2.imshow('frame', img)
        #wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is more than sample size
        elif sampleNum > SAMPLE_SIZE:
            break
    cam.release()
    cv2.destroyAllWindows()
    for i,img in enumerate(imgs):
        cv2.imwrite(TRAINING_IMAGES_FOLDER + os.sep + std_folder_name+os.sep+str(name) + "_"+str(Id) + '.' + str(i+1) + ".jpg", img)
    print("Images Saved for ID : " + str(Id) + " Name : " + str(name))

def checkDir(std_folder_name):
    if TRAINING_IMAGES_FOLDER not in os.listdir():
        os.mkdir(TRAINING_IMAGES_FOLDER)

    if std_folder_name in os.listdir(TRAINING_IMAGES_FOLDER):
        print("Data for " + std_folder_name + " already exists.")
        choice=input("Do you wish to overwrite that?(y/n) ")
        if choice=='n':
            return False
        shutil.rmtree(os.path.join(TRAINING_IMAGES_FOLDER,std_folder_name))
        # os.rmdir(os.path.join(TRAINING_IMAGES_FOLDER,std_folder_name))

    os.mkdir(os.path.join(TRAINING_IMAGES_FOLDER,std_folder_name))
    return True

            

    
