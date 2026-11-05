import cv2
import torch
from ultralytics import YOLO


def main():
    # COCO 데이터셋으로 사전 학습된 경량 YOLO 모델.
    # 첫 실행 시 모델 가중치(yolo11n.pt)를 자동으로 다운로드한다.
    model = YOLO("yolo11n.pt")

    # MPS 사용 가능 여부에 따라 추론 장치를 선택한다.
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"추론 장치: {device}")

    # 기존 실험에서 정상 동작을 확인한 카메라 인덱스와 백엔드를 사용한다.
    cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("카메라 프레임을 읽지 못했습니다.")
                break

            # 현재 프레임에서 객체 탐지 수행
            results = model.predict(
                source=frame,
                device=device,
                conf=0.35,
                verbose=False,
            )

            # 탐지 결과(박스, 클래스 이름, confidence)를 원본 프레임에 표시
            annotated_frame = results[0].plot()

            cv2.imshow("YOLO Object Detection", annotated_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
