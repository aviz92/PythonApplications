import cv2
import datetime


CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
PATH_TO_SAVE = f'output_{CURRENT_DATE}.avi'

if __name__ == '__main__':
    try:
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(PATH_TO_SAVE, fourcc, 20.0, (640, 480))

        # start the video
        # camera = cv2.VideoCapture('rtsp://user:password@192.168.59.53')  # mTM-9kx-Yyz
        camera = cv2.VideoCapture(0)

        while camera.isOpened():
            ret, frame = camera.read()
            if ret:
                # write the flipped frame
                out.write(frame)

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        camera.release()
        out.release()
        cv2.destroyAllWindows()
    except Exception as err:
        print(err)
