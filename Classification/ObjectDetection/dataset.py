import os

class Dataset:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.classes = self.load_classes()

    def load_classes(self):
        classes_path = os.path.join(self.dataset_path, "classes.txt")
        with open(classes_path, "r") as f:
            return [line.strip() for line in f.readlines()]

    def load_images(self):
        images_path = os.path.join(self.dataset_path, "images")
        return [os.path.join(images_path, f) for f in os.listdir(images_path)]

    def load_annotations(self):
        annotations_path = os.path.join(self.dataset_path, "annotations")
        return [os.path.join(annotations_path, f) for f in os.listdir(annotations_path)]