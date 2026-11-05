
import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("파란색 물체를 카메라에 보여주세요.")
    print("종료하려면 q를 누르세요.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("카메라 프레임을 읽을 수 없습니다.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 파란색 범위
        lower_blue = np.array([90, 80, 50])
        upper_blue = np.array([135, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # 작은 노이즈 제거
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(
            mask, cv2.MORPH_OPEN, kernel
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        if contours:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area > 500:
                x, y, w, h = cv2.boundingRect(largest)

                center_x = x + w // 2
                center_y = y + h // 2

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2,
                )

                cv2.circle(
                    frame,
                    (center_x, center_y),
                    5,
                    (0, 0, 255),
                    -1,
                )

                cv2.putText(
                    frame,
                    "Tracking",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

        cv2.imshow("Object Tracking", frame)
        cv2.imshow("Color Detection", mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
