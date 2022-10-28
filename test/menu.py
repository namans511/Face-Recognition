print("starting app....")
import os
print("os done")
import platform
print("platform done")
from dotenv import load_dotenv
print("dotenv done")
import capture_images
print("capture images done")
load_dotenv()
print("loaded configurations....")

def title_bar():
    if platform.system()=='Windows':
        os.system('cls')  # for windows

    # title of the program

    print("\t**********************************************")
    print("\t***** Face Recognition Attendance System *****")
    print("\t**********************************************")


# creating the user main menu function

def mainMenu():
    title_bar()

    while True:
        print(10 * "*", "WELCOME MENU", 10 * "*")
        print("[1] Check Camera")
        print("[2] Capture Faces")
        print("[3] Train Images")
        print("[4] Recognize & Attendance")
        print("[5] Auto Mail")
        print("[6] Quit")
        print()
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                print("checking camera....")
                # checkCamera()
                # break
            elif choice == 2:
                CaptureFaces()
                # break
            elif choice == 3:
                print("training images....")
                # Trainimages()
                # break
            elif choice == 4:
                print("taking attendance...")
                # RecognizeFaces()
                # break
            elif choice == 5:
                print("random stuff")
                # os.system("py automail.py")
                # break
                # mainMenu()
            elif choice == 6:
                print("Thank You")
                break
            else:
                print("Invalid Choice. Enter 1-6")
                mainMenu()
        except ValueError:
            print("Invalid Choice. Enter 1-6\n Try Again")
        print()
    exit


def CaptureFaces():
    name=input("Enter name: ")
    id=input('Enter ' + os.getenv("ID") + ": ")
    # print(name,id)
    capture_images.takeImages(id,name)

if __name__=='__main__':
    mainMenu()
