import cv2
import numpy as np
from tensorflow.keras import utils
from astroNN.datasets import load_galaxy10
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras import layers, optimizers

# First time downloading location will be ~/.astroNN/datasets/
images, labels = load_galaxy10()

# Convert the labels to categorical 10 classes
labels = utils.to_categorical(labels, 10)

# Convert to desirable type
labels = labels.astype(np.float32)
images = images.astype(np.float32)

# Function to remove noise from image
def remove_noise(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median blur to remove noise
    denoised = cv2.medianBlur(gray, 5)

    # Display the original and denoised images
    cv2.imshow(image)
    cv2.imshow(denoised)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return denoised

new_images=[]

for image in images:
    image=remove_noise(image)
    new_images.append(image)


train_idx, test_idx = train_test_split(np.arange(labels.shape[0]), test_size=0.1)
train_images, train_labels, test_images, test_labels = images[train_idx], labels[train_idx], images[test_idx], labels[test_idx]

def build_model():
    model = Sequential()
    model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=[50, 50, 3]))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(2, activation='softmax'))

    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizers.Adam(lr=0.01),
        metrics=['accuracy']
    )

    return model

# Train the best model
model=build_model()
model.fit(train_images, epochs=50, validation_data=train_labels)