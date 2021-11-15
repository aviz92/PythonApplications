import time
import cv2
import threading
from pygame import mixer
import datetime


CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
PATH_TO_SAVE = f'output_{CURRENT_DATE}.avi'


def activate_alarm():
    # start record
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(PATH_TO_SAVE, fourcc, 20.0, (640, 480))
    out.write(frame)


    mixer.init()
    mixer.music.load('WarningBuzzerSpace.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.01)
    # stop record
    cv2.imshow('frame', frame)
    out.release()


if __name__ == '__main__':
    thread_alarm = object()

    try:
        camera = cv2.VideoCapture(0)
        # camera = cv2.VideoCapture('rtsp://user:password@192.168.1.88')

        while camera.isOpened():
            ret, frame = camera.read()
            ret, new_frame = camera.read()
            diff = cv2.absdiff(frame, new_frame)

            gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

            dilated = cv2.dilate(threshold, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

            for c in contours:
                if cv2.contourArea(c) < 5000:
                    continue
                else:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    time.sleep(0.01)
                    if (not hasattr(thread_alarm, 'is_alive')) or \
                            (hasattr(thread_alarm, 'is_alive') and not thread_alarm.is_alive()):
                        print(f"1: {not hasattr(thread_alarm, 'is_alive')}")
                        print(f"2: {(hasattr(thread_alarm, 'is_alive') and not thread_alarm.is_alive())}")

                        thread_alarm = threading.Thread(target=activate_alarm)
                        thread_alarm.daemon = True
                        thread_alarm.start()

            if cv2.waitKey(10) == ord('q'):
                break

            cv2.imshow('Security Camera', frame)  # show the image on the screen
        # Release everything if job is finished
        camera.release()
        cv2.destroyAllWindows()
    except Exception as err:
        print(err)
