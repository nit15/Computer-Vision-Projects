import numpy as np
import pyttsx3
import speech_recognition as sr
import cv2
import time
import HnadtrackingMODULE as htm


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
pt=0
color = (255,255,255)
xp,yp = 0,0
Brushsize = 10
img1 = np.zeros((720,1280,3),np.uint8)
det = htm.Handdetector()
engine= pyttsx3.init('sapi5')

voices= engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voices',voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def input():
    i= sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        i.pause_threshold = 0.8
        i.energy_threshold = 1000
        audio = i.listen(source)

    try:
        print("Recognizing.....")
        query = i.recognize_google(audio,language='en-in')
        print("user said:"+query)

    except Exception as e:
        print("Sorry, Please Say that again and clear...")
        return "None"

    return query.lower()

speak("hello! I am smart assistant, How may I help you?")

while True:
    success, img= cap.read()
    img = cv2.flip(img,1)
    img = det.detecthand(img)

    #
    lmlist = det.trackhand(img,draw= True)
    if len(lmlist)!= 0 :
        x1,y1 = lmlist[8][1:]
        # print(x1,y1)
        f = det.fingerup(img)
        if f[1] and f[2] and f[0]==0 and f[3]==0 and f[4]==0:
            flag = True
            xp,yp = 0,0
        elif f[1] and f[2]==0 and f[0]==0 and f[3]==0 and f[4]==0:
            # speak("Drawing Mode")
            if xp == 0 and yp == 0:
                xp,yp = x1,y1
            if color == (0,0,0):
                Brushsize = 50
            else:
                Brushsize = 10
            cv2.line(img, (xp,yp), (x1,y1), color, Brushsize)
            cv2.line(img1, (xp,yp), (x1,y1), color, Brushsize)
            xp,yp = x1,y1
            flag = False
        else:
            flag = False
            xp,yp = 0,0

        while flag:
            speak("Selecting Mode. colour or erraser?")
            query = str(input().lower())
            if query == "colour":
                speak("Which colour? Pink, blue, green")
                query = str(input().lower())
                if query == "pink":
                    color = (255,0,255)
                    break
                elif query == "green":
                    color = (0,255,0)
                    break
                elif query == "blue":
                    color = (255,0,0)
                    break
                else:
                    speak("Wrong color input")
                    speak("Which colour? Pink, blue, green")


            elif query == "eraser":
                color = (0,0,0)
                break

    ct = time.time()
    fps = 1/(ct-pt)
    pt=ct

    imgg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    _, imginv = cv2.threshold(imgg,50,255,cv2.THRESH_BINARY_INV)
    imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imginv)
    img = cv2.bitwise_or(img, img1)


    # cv2.putText(img, f'hello', (100, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, color, 5)

    cv2.putText(img, f'FPS: {int(fps)}',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255,0,0), 5)
    cv2.imshow("image",img)
    cv2.imshow("canvas", img1)
    cv2.waitKey(1)
