from flask import Flask, request, render_template
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np

app = Flask(__name__)

# Load pre-trained model
model = keras.models.load_model('model.h5')

# Define image preprocessing function
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    return image

# Define classification function
def classify_image(image):
    image = preprocess_image(image)
    prediction = model.predict(image[np.newaxis, :])
    return np.argmax(prediction)

# Index route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        image = Image.open(image_file)
        prediction = classify_image(image)
        return render_template('result.html', prediction=prediction)
    return render_template('index.html')

# Run application
if __name__ == '__main__':
    app.run(debug=True)