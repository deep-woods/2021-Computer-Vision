import cv2
import mediapipe as mp
import time
import numpy as np

class HandTracker():

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    # On creation, you can specify camera (webcam) or put a path instead to use a specific video footage. 
    def __init__(self, camera=0):
        self.cap = cv2.VideoCapture(camera)

    def track_hand(self):
        while True:
            success, img = self.cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)
            # print(results.multi_hand_landmarks)

            if results.multi_hand_landmarks:                            # if multiple hands are detected,
                for hand_landmarks in results.multi_hand_landmarks:     # hand_landmarks = a [list] of landmark data for a hand
                    for id, lm in enumerate(hand_landmarks.landmark):   # id = the enumerate index. lm = x, y, z coordinates of each hand landmark point.
                        print(id, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)           # pixellise the landmark values (x, y, z)
                        print(id, cx, cy)

                        # At this point: so... how do we make use of the landmark data in fact?
                        # Now that we have labelled each landmark with id, and the pixellised coordinate values,
                        # we can do fun things with each individual landmark.
                        if id == 4:
                            cv2.circle(img, (cx, cy), 30, (100, 9, 255), cv2.FILLED)

                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)    # draw the landmarks

            self.cTime = time.time()
            fps = 1/(self.cTime-self.pTime)   # frames per second
            self.pTime = self.cTime

            cv2.putText(img, str(f"FPS {np.floor(fps)}"), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            cv2.imshow("Perform tasks on specific landmarks - example 2", img)
            cv2.waitKey(1)

# Initialise an object of HandTracker class, then track a hand.
ht = HandTracker()
ht.track_hand()
