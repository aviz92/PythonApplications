import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

FOLDER_PATH = "FingerImages"
W_CAM, H_CAM = 640, 480

if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    # camera = cv2.VideoCapture(1)

    cap.set(3, W_CAM)
    cap.set(4, H_CAM)

    p_time = 0
    
    detector = htm.HandDetector(detection_con=0.7)
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    vol_range = volume.GetVolumeRange()
    min_vol = vol_range[0]
    max_vol = vol_range[1]
    vol = 0
    vol_bar = 400
    vol_per = 0
    
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)
        if len(lm_list) != 0:
            # print(lm_list[4], lm_list[8])
    
            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
    
            length = math.hypot(x2 - x1, y2 - y1)
            # print(length)
    
            # Hand range 50 - 300
            # Volume Range -65 - 0
    
            vol = np.interp(length, [50, 100], [min_vol, max_vol])
            vol_bar = np.interp(length, [50, 120], [400, 150])
            vol_per = np.interp(length, [50, 100], [0, 100])
            print(int(length), vol)
            volume.SetMasterVolumeLevel(vol, None)
    
            if length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(vol_per)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    
        cTime = time.time()
        fps = 1 / (cTime - p_time)
        p_time = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    
        cv2.imshow("Img", img)
        cv2.waitKey(1)
