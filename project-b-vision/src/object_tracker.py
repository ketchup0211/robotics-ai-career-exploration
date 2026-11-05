
import cv2
import numpy as np


def nothing(value):
    pass


def main():
    # 1. 카메라 연결
    cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    # 2. 조절 창 생성
    cv2.namedWindow("Controls")

    # HSV 설정
    cv2.createTrackbar("S min", "Controls", 100, 255, nothing)
    cv2.createTrackbar("V min", "Controls", 99, 255, nothing)
    cv2.createTrackbar("V max", "Controls", 255, 255, nothing)

    # 물체 필터 설정
    cv2.createTrackbar("Min Area", "Controls", 3000, 10000, nothing)

    # Aspect Ratio는 0.1 단위로 조절
    cv2.createTrackbar("Min Ratio x10", "Controls", 1, 100, nothing)
    cv2.createTrackbar("Max Ratio x10", "Controls", 100, 100, nothing)

    # 3. 형태학적 연산 커널
    open_kernel = np.ones((5, 5), np.uint8)

    close_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (17, 17)
    )

    try:
        while True:
            # 4. 프레임 읽기
            ret, frame = cap.read()

            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            # 5. BGR -> HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # 6. 슬라이더 값 가져오기
            s_min = cv2.getTrackbarPos("S min", "Controls")
            v_min = cv2.getTrackbarPos("V min", "Controls")
            v_max = cv2.getTrackbarPos("V max", "Controls")

            min_area = cv2.getTrackbarPos("Min Area", "Controls")

            min_ratio = (
                cv2.getTrackbarPos("Min Ratio x10", "Controls") / 10
            )

            max_ratio = (
                cv2.getTrackbarPos("Max Ratio x10", "Controls") / 10
            )

            v_max = max(v_min, v_max)

            # 7. 파란색 영역 추출
            lower_blue = np.array([90, s_min, v_min])
            upper_blue = np.array([135, 255, v_max])

            mask = cv2.inRange(
                hsv,
                lower_blue,
                upper_blue
            )

            # 8. 끊어진 영역 연결
            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_CLOSE,
                close_kernel
            )

            # 9. 작은 노이즈 제거
            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_OPEN,
                open_kernel
            )

            # 10. 윤곽선 검출
            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            detected_count = 0

            for contour in contours:
                area = cv2.contourArea(contour)

                # 최소 면적 필터
                if area < min_area:
                    continue

                x, y, w, h = cv2.boundingRect(contour)

                # 가로세로 비율 계산
                aspect_ratio = w / h if h > 0 else 0

                # 가로세로 비율 필터
                if not (min_ratio <= aspect_ratio <= max_ratio):
                    continue

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

                # 면적 및 비율 표시
                label = f"A:{int(area)} R:{aspect_ratio:.2f}"

                cv2.putText(
                    frame,
                    label,
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            # 11. 현재 설정 표시
            cv2.putText(
                frame,
                f"Detected: {detected_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Area >= {min_area}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Ratio: {min_ratio:.1f} - {max_ratio:.1f}",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            # 12. 화면 출력
            cv2.imshow("Object Detection", frame)
            cv2.imshow("Color Detection", mask)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
