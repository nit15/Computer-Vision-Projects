import cv2
import mediapipe as mp
import time


# wcam = 720
# hcam = 720
# data.set(3, wcam)
# data.set(4, hcam)

# Previous time

class Handdetector():
    def __init__(self, mode=False, max_hands=2, complex=1, det_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.complex = complex
        self.det_con = det_con
        self.track_con = track_con

        self.mphand = mp.solutions.hands
        self.hands = self.mphand.Hands(self.mode, self.max_hands, self.complex, self.det_con, self.track_con)
        self.mpDraw = mp.solutions.drawing_utils

    def detecthand(self, img, draw=True):
        IMG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(IMG)
        if self.result.multi_hand_landmarks:
            for handlm in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlm, self.mphand.HAND_CONNECTIONS)
        return img

    def trackhand(self, img, hand=0, draw=False):
        self.lmlist = []
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[hand]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return self.lmlist

    def fingerup(self, img):
        fingers = []
        fingertip = [4,8,12,16,20]
        if self.lmlist[fingertip[0]][1] < self.lmlist[fingertip[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if self.lmlist[fingertip[id]][2] < self.lmlist[fingertip[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


def main():
    pt = 0
    data = cv2.VideoCapture(0)
    detector = Handdetector()
    while True:
        success, img = data.read()
        img = detector.detecthand(img)
        list = detector.trackhand(img, 0, True)
        if len(list) != 0:
            print(list[4])
        ct = time.time()
        fps = 1 / (ct - pt)
        pt = ct

        cv2.putText(img, f'FPS:{int(fps)}', (20, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()