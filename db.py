import datetime
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

from face.models import *

def savePerson(name, roll, enc):
    stu = Person(name=name,roll_number=roll,encoding=enc)
    stu.save()


def saveEncoding(names, roll_nos, encodings):
    students = [Person(name=name,roll_number=number,encoding=enc.tolist()) for name,number,enc in zip(names,roll_nos,encodings)]
    # students = []
    # for name,number,enc in zip(names,roll_nos,encodings):
    #     student = Person(name=name,roll_number=number,encoding=enc.tolist())
    #     students.append(student)
    Person.objects.bulk_create(students)
    print(names, " encoding saved")
    pass

def getEncodings():
    data = Person.objects.all()
    names = []
    encodings = []
    roll_nos = []
    for i in data:
        names.append(i.name)
        encodings.append(i.encoding)
        roll_nos.append(i.roll_number)
    return (names,encodings)

#mark entry in db
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
        

    
   
    
    

