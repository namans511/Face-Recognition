import datetime

def saveEncoding(names, encodings):
    print(names, " encoding saved")
    pass

def getEncodings():
    return ([],[])

#mark entry in db
def mark(name):
    print(f"{name} is marked present")
    pass

#get configurations from db
def getConfig():
    pass



class student:
    def __init__(self) -> None:
        self.present = {}
        #FIXME get this info from config
        self.timeDelta = 15

    def markAttendance(self, name):
        if name=='Unknown':
            return

        if name not in self.present:
            mark(name)
        else:
            delta = datetime.datetime.now() - self.present[name]
            
            if delta.seconds<=self.timeDelta*60:
                mark(name)
        
        self.present[name] = datetime.datetime.now()

        #TODO dont mark present if name is Unknown
        pass
    
   
    
    

