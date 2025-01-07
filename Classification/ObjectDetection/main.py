import cv2
from object_detection import ObjectDetector

def main():
    model_name = "yolov3"
    dataset_path = "dataset"
    detector = ObjectDetector(model_name, dataset_path)

    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        if not ret:
            break

        detector.start_detection(frame)
        detector.detection_thread.join()
        detector.start_tracking(frame)
        detector.tracking_thread.join()
        detected_frame = detector.visualize_detections(frame, detector.detections)

        cv2.imshow("Object Detection", detected_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()