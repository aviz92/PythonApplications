import cv2


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
