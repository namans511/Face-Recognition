import datetime
import os
import sys
import pickle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

from face.models import *


#FIXME take this from config later
PICKLE_FILE_NAME = "facedata"

def savePerson(name, roll, enc):
    stu = Person(name=name,roll_number=roll,encoding=enc)
    stu.save()


def saveEncoding(names, encodings):
    #HACK decide to save in pickle
    savePickle(names, encodings)
    # students = [Person(name=name,roll_number=number,encoding=enc.tolist()) for name,number,enc in zip(names,roll_nos,encodings)]
    # students = []
    # for name,number,enc in zip(names,roll_nos,encodings):
    #     student = Person(name=name,roll_number=number,encoding=enc.tolist())
    #     students.append(student)
    return
    Person.objects.bulk_create(students)
    print(names, " encoding saved")
    pass

def savePickle(names, encodings):
    data = {}
    for name,enc in zip(names, encodings):
        data[name]=enc
    print(data)
    with open(PICKLE_FILE_NAME,"wb") as f:
        pickle.dump(data,f)

def getPickle():
    names = []
    encodings = []
    try:
        with open(PICKLE_FILE_NAME,"rb") as file:
            data = pickle.load(file)
            for name in data.keys():
                names.append(name)
                encodings.append(data[name])
    except FileNotFoundError:
        pass  
    return names,encodings





def getEncodings():
    #HACK decide if you wanna return shit from db or pickle
    return getPickle()
    # data = Person.objects.all()
    # names = []
    # encodings = []
    # roll_nos = []
    # for i in data:
    #     names.append(i.name)
    #     encodings.append(i.encoding)
    #     roll_nos.append(i.roll_number)
    # return (names,encodings)

#INFO mark entry in db
def mark(name):
    print(f"{name} is marked present")
    Timings.objects.create(name=name,time=datetime.datetime.now())
    #Attendece.objects.create(student=pk,date=datetime.now,time=jh)
    pass

#get configurations from db
def getConfig():
    pass



class Student:
    def __init__(self) -> None:
        self.present = {}
        #FIXME get this info from config
        self.timeDelta = 15

    def markAttendance(self, name):
        #dont mark present if name is Unknown
        if name=='Unknown':
            return
            
        if name not in self.present:
            mark(name)
            self.present[name] = datetime.datetime.now()
        else:
            delta = datetime.datetime.now() - self.present[name]
            # print(delta.seconds, self.timeDelta*60)    
            if delta.seconds>=self.timeDelta*60:
                mark(name)
                self.present[name] = datetime.datetime.now()
        

    
   
    
    

