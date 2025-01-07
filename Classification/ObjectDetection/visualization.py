import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, detector):
        self.detector = detector

    def visualize_detections(self, frame, detections):
        for (x, y, w, h) in detections:
            cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)
            cv2.putText(frame, f"Object", (int(x), int(y-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return frame

    def visualize_ground_truths(self, frame, ground_truths):
        for (x, y, w, h) in ground_truths:
            cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 0, 255), 2)
            cv2.putText(frame, f"Ground Truth", (int(x), int(y-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return frame