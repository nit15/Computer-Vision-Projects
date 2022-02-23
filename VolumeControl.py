import cv2
import mediapipe as mp
import numpy as np
import time
import HnadtrackingMODULE as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# print(volume.GetMasterVolumeLevel())
vol = volume.GetVolumeRange()
min_vol = vol[0]
max_vol = vol[1]

cam = cv2.VideoCapture(0)
cam.set(3,1020)
cam.set(4,1020)
detect= htm.Handdetector()

pt=0
while True:
    success, img= cam.read()
    img = detect.detecthand(img)
    Lmlist= detect.trackhand(img)
    if len(Lmlist)!=0:
        x1,y1 = Lmlist[4][1],Lmlist[4][2]
        x2,y2 = Lmlist[8][1],Lmlist[8][2]
        # print(y2)
        cv2.circle(img,(x1,y1),5, (255,0,255), 3)
        cv2.circle(img, (x2, y2), 5, (255, 0, 255), 3)
        cv2.line(img,(x1,y1),(x2,y2), (0,255,0) , 2)
        length = math.hypot(x2-x1,y2-y1)
        #print(length)

        new_length = np.interp(length, [35,265], [min_vol,max_vol])
        print(new_length)
        volume.SetMasterVolumeLevel(new_length, None)

    ct=time.time()
    fps=1/(ct-pt)
    pt=ct

    cv2.putText(img, f'FPS:{int(fps)}', (20,70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
