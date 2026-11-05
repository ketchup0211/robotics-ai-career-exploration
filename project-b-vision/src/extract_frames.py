from pathlib import Path
import cv2

# project-b-vision 폴더 기준 경로
BASE_DIR = Path(__file__).resolve().parents[1]

VIDEO_PATH = BASE_DIR / "datasets/pikmin/raw_videos/pikmin_video.mp4"
OUTPUT_DIR = BASE_DIR / "datasets/pikmin/raw"

# 1초마다 한 장 추출
INTERVAL_SECONDS = 1


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(VIDEO_PATH))

    if not cap.isOpened():
        print(f"영상을 열 수 없습니다: {VIDEO_PATH}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, round(fps * INTERVAL_SECONDS))

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            output_path = OUTPUT_DIR / f"pikmin_{saved_count:04d}.jpg"
            cv2.imwrite(str(output_path), frame)
            saved_count += 1

        frame_count += 1

    cap.release()

    print(f"영상 프레임 수: {frame_count}")
    print(f"저장된 사진 수: {saved_count}")
    print(f"저장 위치: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()