import tensorflow as tf
import matplotlib.pyplot as plt

# Load model
model = tf.keras.models.load_model('handwritten_digit_recognition_model.h5')

# Evaluate model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc:.2f}')

# Plot predictions
predictions = model.predict(x_test)
plt.imshow(x_test[0], cmap='gray')
plt.title(f'Prediction: {np.argmax(predictions[0])}')
plt.show()