import numpy as np

class Evaluator:
    def __init__(self, detector):
        self.detector = detector

    def evaluate_precision(self, detections, ground_truths):
        true_positives = 0
        for detection, ground_truth in zip(detections, ground_truths):
            iou = self.detector.calculate_iou(detection, ground_truth)
            if iou > 0.5:
                true_positives += 1
        return true_positives / len(detections)

    def evaluate_recall(self, detections, ground_truths):
        true_positives = 0
        for detection, ground_truth in zip(detections, ground_truths):
            iou = self.detector.calculate_iou(detection, ground_truth)
            if iou > 0.5:
                true_positives += 1
        return true_positives / len(ground_truths)

    def evaluate_AP(self, detections, ground_truths):
        precision = self.evaluate_precision(detections, ground_truths)
        recall = self.evaluate_recall(detections, ground_truths)
        return precision * recall / (precision + recall)