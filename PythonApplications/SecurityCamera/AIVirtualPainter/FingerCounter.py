import os
import time
import cv2
import HandTrackingModule as htm


FOLDER_PATH = "FingerImages"
W_CAM, H_CAM = 640, 480

if __name__ == '__main__':
    camera = cv2.VideoCapture(1)

    camera.set(3, W_CAM)
    camera.set(4, H_CAM)

    myList = os.listdir(FOLDER_PATH)
    # print(myList)

    overlay_list = []
    for imPath in myList:
        image = cv2.imread(f'{FOLDER_PATH}/{imPath}')
        # print(f'{FOLDER_PATH}/{imPath}')
        overlay_list.append(image)

    # print(len(overlay_list))
    p_time = 0

    detector = htm.HandDetector(detection_con=0.75)

    tip_ids = [4, 8, 12, 16, 20]

    while True:
        success, img = camera.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)
        # print(lm_list)

        if len(lm_list) != 0:
            fingers = []

            # Thumb
            print(f'{lm_list[tip_ids[0]][1]}  ---  {lm_list[tip_ids[0] - 1][1]}')
            if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id_ in range(1, 5):
                print(f'{lm_list[tip_ids[id_]][2]}  ---  {lm_list[tip_ids[id_] - 2][2]}')
                if lm_list[tip_ids[id_]][2] < lm_list[tip_ids[id_] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)
            total_fingers = fingers.count(1)
            print(total_fingers)

            h, w, c = overlay_list[total_fingers].shape
            if total_fingers:
                img[0:h, 0:w] = overlay_list[total_fingers]
            else:
                img = overlay_list[total_fingers]

            cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(total_fingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
