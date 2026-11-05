
import cv2
import numpy as np
from collections import deque


def main():
    cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("파란색 물체를 카메라에 보여주세요.")
    print("q 또는 ESC를 누르면 종료됩니다.")

    # 최근 중심점 30개 저장
    trail = deque(maxlen=30)

    # 보정된 중심점
    smooth_x = None
    smooth_y = None

    while True:
        ret, frame = cap.read()

        if not ret:
            print("카메라 프레임을 읽을 수 없습니다.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([90, 80, 50])
        upper_blue = np.array([135, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

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

                # 중심점 위치를 부드럽게 보정
                if smooth_x is None:
                    smooth_x = center_x
                    smooth_y = center_y
                else:
                    alpha = 0.3
                    smooth_x = int(
                        alpha * center_x + (1 - alpha) * smooth_x
                    )
                    smooth_y = int(
                        alpha * center_y + (1 - alpha) * smooth_y
                    )

                trail.append((smooth_x, smooth_y))

                cv2.rectangle(
                    frame, (x, y), (x + w, y + h),
                    (0, 255, 0), 2
                )

                cv2.circle(
                    frame, (smooth_x, smooth_y),
                    6, (0, 0, 255), -1
                )

                # 이동 경로 그리기
                if len(trail) > 1:
                    cv2.polylines(
                        frame,
                        [np.array(trail, dtype=np.int32)],
                        False,
                        (255, 0, 255),
                        3,
                    )

                status = "Tracking"
            else:
                trail.clear()
                smooth_x = None
                smooth_y = None
                status = "Searching"
        else:
            trail.clear()
            smooth_x = None
            smooth_y = None
            status = "Searching"

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0) if status == "Tracking" else (0, 0, 255),
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
