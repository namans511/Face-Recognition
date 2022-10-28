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

def takeImages(Id,name):

    print(name,Id)
    
    
    # harcascadePath = "haarcascade_frontalface_default.xml"
    # detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    SAMPLE_SIZE = int(os.getenv('SAMPLE_SIZE'))
    std_folder_name = name+"_"+Id
    flag = checkDir(std_folder_name)
    cam = cv2.VideoCapture(0)
    while(flag):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
        faces = face_recognition.face_locations(gray)
        print(faces)
        # for(x,y,w,h) in faces:
        for (top, right, bottom, left) in faces:
            # cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            #incrementing sample number
            sampleNum = sampleNum+1
            #saving the captured face in the dataset folder TrainingImage
            cv2.imwrite(TRAINING_IMAGES_FOLDER + os.sep + std_folder_name+os.sep+str(name) + "_"+str(Id) + '.' + str(sampleNum) + ".jpg", gray[top:bottom, left:right])
            #display the frame
        cv2.imshow('frame', img)
        #wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is more than 100
        elif sampleNum > SAMPLE_SIZE:
            break
    cam.release()
    cv2.destroyAllWindows()
    temp=''.join(list(i for i in name.split()))
    res = "Images Saved for ID : " + str(Id) + " Name : " + str(temp) 
    row = [Id, name]
    # with open("EmployeeDetails"+os.sep+"EmployeeDetails.csv", 'a+') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerow(row)
    # csvFile.close()

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

            

    
