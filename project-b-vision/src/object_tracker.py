
import cv2
import numpy as np


def main():
    # 1. 카메라 연결
    cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    # 2. 파란색 HSV 범위
    lower_blue = np.array([90, 80, 50])
    upper_blue = np.array([135, 255, 255])

    # 3. 노이즈 제거 및 영역 연결용 커널
    open_kernel = np.ones((5, 5), np.uint8)
    close_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (17, 17)
    )

    # 최소 검출 영역
    min_area = 500

    try:
        while True:
            # 4. 카메라 프레임 읽기
            ret, frame = cap.read()

            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            # 5. BGR -> HSV 변환
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # 6. 파란색 영역 추출
            mask = cv2.inRange(
                hsv,
                lower_blue,
                upper_blue
            )

            # 7. 끊어진 영역 연결
            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_CLOSE,
                close_kernel
            )

            # 8. 작은 노이즈 제거
            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_OPEN,
                open_kernel
            )

            # 9. 윤곽선 검출
            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            detected_count = 0

            # 10. 모든 윤곽선 확인
            for contour in contours:
                area = cv2.contourArea(contour)

                # 너무 작은 영역 제외
                if area < min_area:
                    continue

                x, y, w, h = cv2.boundingRect(contour)

                center_x = x + w // 2
                center_y = y + h // 2

                detected_count += 1

                # 경계 상자
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                # 중심점
                cv2.circle(
                    frame,
                    (center_x, center_y),
                    5,
                    (0, 0, 255),
                    -1
                )

                # 영역 크기
                cv2.putText(
                    frame,
                    f"Area: {int(area)}",
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            # 11. 검출 개수 표시
            cv2.putText(
                frame,
                f"Detected: {detected_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # 12. 결과 출력
            cv2.imshow("Object Detection", frame)
            cv2.imshow("Color Detection", mask)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
