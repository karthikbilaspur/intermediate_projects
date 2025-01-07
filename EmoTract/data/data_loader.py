import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def load_data(self):
        return self.data