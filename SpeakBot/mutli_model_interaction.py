import cv2

class MultiModalInteraction:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def capture_image(self):
        ret, frame = self.capture.read()
        return frame