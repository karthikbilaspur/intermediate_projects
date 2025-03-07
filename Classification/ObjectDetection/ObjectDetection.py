import os
import cv2
import numpy as np
from object_detection import ObjectDetector
from evaluation import Evaluator
from visualization import Visualizer

class Dataset:
    def __init__(self, dataset_path):
        """
        Initializes the Dataset class.

        Args:
            dataset_path (str): The path to the dataset.
        """
        self.dataset_path = dataset_path
        self.classes = self.load_classes()

    def load_classes(self):
        """
        Loads the classes from the dataset.

        Returns:
            list: A list of classes.
        """
        classes_path = os.path.join(self.dataset_path, "classes.txt")
        with open(classes_path, "r") as f:
            return [line.strip() for line in f.readlines()]

    def load_images(self):
        """
        Loads the images from the dataset.

        Returns:
            list: A list of image paths.
        """
        images_path = os.path.join(self.dataset_path, "images")
        return [os.path.join(images_path, f) for f in os.listdir(images_path)]

    def load_annotations(self):
        """
        Loads the annotations from the dataset.

        Returns:
            list: A list of annotation paths.
        """
        annotations_path = os.path.join(self.dataset_path, "annotations")
        return [os.path.join(annotations_path, f) for f in os.listdir(annotations_path)]


class ObjectDetector:
    def __init__(self, model_name, dataset_path):
        """
        Initializes the ObjectDetector class.

        Args:
            model_name (str): The name of the object detection model.
            dataset_path (str): The path to the dataset.
        """
        self.model_name = model_name
        self.dataset_path = dataset_path
        self.net = cv2.dnn.readNetFromDarknet(model_name + ".cfg", model_name + ".weights")
        self.classes = self.load_classes(dataset_path + "/classes.txt")
        self.trackers = []
        self.detections = []

    def load_classes(self, classes_path):
        """
        Loads the classes from the dataset.

        Args:
            classes_path (str): The path to the classes file.

        Returns:
            list: A list of classes.
        """
        with open(classes_path, "r") as f:
            return [line.strip() for line in f.readlines()]

    def detect_objects(self, frame):
        """
        Detects objects in the given frame.

        Args:
            frame (numpy array): The frame to detect objects in.

        Returns:
            list: A list of detected objects.
        """
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
        """
        Tracks objects across frames.

        Args:
            frame (numpy array): The frame to track objects in.
        """
        for (x, y, w, h) in self.detections:
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (x, y, w, h))
            self.trackers.append(tracker)


class Evaluator:
    def __init__(self, detector):
        """
        Initializes the Evaluator class.

        Args:
            detector (ObjectDetector): The object detector to evaluate.
        """
        self.detector = detector

    def evaluate_precision(self, detections, ground_truths):
        """
        Evaluates the precision of the object detector.

        Args:
            detections (list): A list of detected objects.
            ground_truths (list): A list of ground truth objects.

        Returns:
            float: The precision of the object detector.
        """
        true_positives = 0
        for detection, ground_truth in zip(detections, ground_truths):
            iou = self.detector.calculate_iou(detection, ground_truth)
            if iou > 0.5:
                true_positives += 1
        return true_positives / len(ground_truths)

    def evaluate_AP(self, detections, ground_truths):
        """
        Evaluates the average precision of the object detector.

        Args:
            detections (list): A list of detected objects.
            ground_truths (list): A list of ground truth objects.

        Returns:
            float: The average precision of the object detector.
        """
        precision = self.evaluate_precision(detections, ground_truths)
        recall = self.evaluate_recall(detections, ground_truths)
        return precision * recall / (precision + recall)


class Visualizer:
    def __init__(self, detector):
        """
        Initializes the Visualizer class.

        Args:
            detector (ObjectDetector): The object detector to visualize.
        """
        self.detector = detector

    def visualize_detections(self, frame, detections):
        """
        Visualizes the detected objects in the given frame.

        Args:
            frame (numpy array): The frame to visualize.
            detections (list): A list of detected objects.

        Returns:
            numpy array: The visualized frame.
        """
        for (x, y, w, h) in detections:
            cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)
            cv2.putText(frame, f"Object", (int(x), int(y-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return frame

    def visualize_ground_truths(self, frame, ground_truths):
        """
        Visualizes the ground truth objects in the given frame.

        Args:
            frame (numpy array): The frame to visualize.
            ground_truths (list): A list of ground truth objects.

        Returns:
            numpy array: The visualized frame.
        """
        for (x, y, w, h) in ground_truths:
            cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 0, 255), 2)
            cv2.putText(frame, f"Ground Truth", (int(x), int(y-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return frame


def main():
    model_name = "yolov3"
    dataset_path = "dataset"
    detector = ObjectDetector(model_name, dataset_path)
    evaluator = Evaluator(detector)
    visualizer = Visualizer(detector)

    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        if not ret:
            break

        detector.detect_objects(frame)
        detector.track_objects(frame)
        detections = detector.detections
        ground_truths = []  # Replace with actual ground truth data

        precision = evaluator.evaluate_precision(detections, ground_truths)
        recall = evaluator.evaluate_recall(detections, ground_truths)
        ap = evaluator.evaluate_AP(detections, ground_truths)

        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"AP: {ap:.2f}")

        visualized_frame = visualizer.visualize_detections(frame, detections)
        visualized_frame = visualizer.visualize_ground_truths(visualized_frame, ground_truths)

        cv2.imshow("Object Detection", visualized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
