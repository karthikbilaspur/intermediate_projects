import cv2
import numpy as np
import threading

class ObjectDetector:
    def __init__(self, model_name, dataset_path):
        self.model_name = model_name
        self.dataset_path = dataset_path
        self.net = cv2.dnn.readNetFromDarknet(model_name + ".cfg", model_name + ".weights")
        self.classes = self.load_classes(dataset_path + "/classes.txt")
        self.trackers = []
        self.detections = []

    def load_classes(self, classes_path):
        with open(classes_path, "r") as f:
            return [line.strip() for line in f.readlines()]

    def detect_objects(self, frame):
        self.net.setInput(cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False))
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())
        self.detections = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:
                    x, y, w, h = detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                    self.detections.append((x, y, w, h))

    def track_objects(self, frame):
        for (x, y, w, h) in self.detections:
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (x, y, w, h))
            self.trackers.append(tracker)

    def evaluate_model(self, detections, ground_truths):
        precision, recall, AP = 0, 0, 0
        for detection, ground_truth in zip(detections, ground_truths):
            iou = self.calculate_iou(detection, ground_truth)
            if iou > 0.5:
                precision += 1
                recall += 1
        precision /= len(detections)
        recall /= len(ground_truths)
        AP = precision * recall / (precision + recall)
        return precision, recall, AP

    def calculate_iou(self, box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        intersection = max(0, min(x1+w1, x2+w2) - max(x1, x2)) * max(0, min(y1+h1, y2+h2) - max(y1, y2))
        union = w1*h1 + w2*h2 - intersection
        return intersection / union

    def visualize_detections(self, frame, detections):
        for (x, y, w, h) in detections:
            cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)
            cv2.putText(frame, f"Object", (int(x), int(y-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return frame

    def start_detection(self, frame):
        self.detection_thread = threading.Thread(target=self.detect_objects, args=(frame,))
        self.detection_thread.start()

    def start_tracking(self, frame):
        self.tracking_thread = threading.Thread(target=self.track_objects, args=(frame,))
        self.tracking_thread.start()