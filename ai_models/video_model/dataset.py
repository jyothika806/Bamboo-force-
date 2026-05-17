import cv2
import numpy as np

def load_video_fast(path, max_frames=10):
    cap = cv2.VideoCapture(path)
    frames = []

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(total // max_frames, 1)

    i = 0
    while len(frames) < max_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (112, 112))
        frame = frame / 255.0

        frames.append(frame)
        i += step

    cap.release()

    # pad frames
    while len(frames) < max_frames:
        frames.append(frames[-1])

    return np.array(frames)