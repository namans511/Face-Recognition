import csv
import time

class Attendance:
    def __init__(self):
        #stores list of students and number of times they blinked
        self.students = {}

    def blink_count(self, names):
        blinked_twice = []
        for name in names:
            try:
                self.students[name]+=1
            except KeyError:
                #if student name not in dict then add it
                self.students[name]=1
            if self.students[name] == 2:
                blinked_twice.append(name)
        return blinked_twice

    def mark(self, names):
        if not names:
            return
        blinked_twice = self.blink_count(names)
        time1 = time.asctime()
        with open("atten.csv","a") as file:
            writer = csv.writer(file)
            for name in blinked_twice:
                print(f"{name} is present")
                writer.writerow([name, time1])