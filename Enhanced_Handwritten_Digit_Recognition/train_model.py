import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Load MNIST dataset
mnist = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Data augmentation
datagen = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=False
)
datagen.fit(x_train)

# Normalize pixel values
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# Define CNN model
base_model = keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(28, 28, 1))
x = base_model.output
x = keras.layers.Flatten()(x)
x = keras.layers.Dense(128, activation='relu')(x)
x = keras.layers.Dropout(0.2)(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs=base_model.input, outputs=outputs)

# Freeze base layers
for layer in base_model.layers:
    layer.trainable = False

# Compile model
optimizer = keras.optimizers.AdamW(learning_rate=0.001, weight_decay=0.01)
model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train model
history = model.fit(datagen.flow(x_train, y_train, batch_size=32),
                    validation_data=(x_test, y_test), epochs=10)

# Save model
model.save('handwritten_digit_recognition_model.h5')