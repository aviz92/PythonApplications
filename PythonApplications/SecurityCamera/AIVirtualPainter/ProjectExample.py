import time
import cv2
import HandTrackingModule as htm
import mediapipe as mp


if __name__ == '__main__':
    p_time = 0
    c_time = 0

    cap = cv2.VideoCapture(0)

    detector = htm.HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lm_list = detector.findPosition(img, draw=False)
        if len(lm_list) != 0:
            print(lm_list[4])

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
