from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
import os
from flask import Flask, request, send_file

app = Flask(__name__)

# Load image
def load_image(image_path):
    return Image.open(image_path)

# Apply transformations and filters
def apply_transformations(img):
    img_flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    img_rotated = img.rotate(45)
    img_resized = img.resize((800, 600))
    img_blurred = img.filter(ImageFilter.BLUR)
    img_grayscale = img.convert('L')
    return img_flipped, img_rotated, img_resized, img_blurred, img_grayscale

# Text overlay
def add_text_overlay(img, text):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 30)
    draw.text((10, 10), text, font=font)
    return img

# Color adjustments
def adjust_colors(img, brightness=1.5, contrast=1.5, saturation=1.5):
    enhancer = ImageEnhance.Brightness(img)
    img_brightened = enhancer.enhance(brightness)
    enhancer = ImageEnhance.Contrast(img_brightened)
    img_contrasted = enhancer.enhance(contrast)
    enhancer = ImageEnhance.Color(img_contrasted)
    img_saturated = enhancer.enhance(saturation)
    return img_saturated

# Batch processing
def batch_process(images):
    for image_file in images:
        img = load_image(image_file)
        img_resized = img.resize((800, 600))
        img_resized.save(f'resized_{image_file}')

# Web interface
@app.route('/upload', methods=['POST'])
def upload_image():
    image_file = request.files['image']
    img = load_image(image_file)
    img_transformed = apply_transformations(img)[2]  # Resized image
    img_transformed.save('transformed_image.jpg')
    return send_file('transformed_image.jpg')

if __name__ == '__main__':
    app.run(debug=True)