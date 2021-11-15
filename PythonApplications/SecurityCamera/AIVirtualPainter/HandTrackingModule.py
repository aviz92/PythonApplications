import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.detection_con, self.track_con)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):

        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id_, lm in enumerate(my_hand.landmark):
                # print(id_, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id_, cx, cy)
                lm_list.append([id_, cx, cy])
                if draw:
                    if id_ == 4:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
                    if id_ == 8:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

                    if id_ == 12:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

                    if id_ == 16:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

                    if id_ == 20:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        return lm_list


def main():
    p_time = 0
    c_time = 0

    cap = cv2.VideoCapture(0)

    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img, draw=True)
        lm_list = detector.find_position(img, draw=True)
        # img = detector.find_hands(img, draw=False)
        # lm_list = detector.find_position(img, draw=False)
        if len(lm_list) != 0:
            print(lm_list[4])
            print(lm_list[8])
            print(lm_list[12])
            print(lm_list[16])
            print(lm_list[20])
            print()

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
