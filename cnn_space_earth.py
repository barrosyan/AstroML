import cv2
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from kerastuner import HyperModel
import kerastuner
import pandas as pd
import numpy as np
import keras
import astroNN
from astroNN.datasets import load_galaxy10
from tensorflow.keras import utils
import requests

def getting_space_data():
    # To load images and labels (will download automatically at the first time)
    # First time downloading location will be ~/.astroNN/datasets/
    images, labels = load_galaxy10()

    # To convert the labels to categorical 10 classes
    labels = utils.to_categorical(labels, 10)

    # To convert to desirable type
    labels = labels.astype(np.float32)
    images = images.astype(np.float32) 

def getting_earth_data():
    # Define API endpoint and parameters
    url = 'https://api.nasa.gov/planetary/earth/imagery'
    longitude = -122.4194
    latitude = 37.7749
    date = '2023-07-05'  # Date of the desired satellite image
    dim = 0.1  # The width and height of the image in degrees
    api_key = 'YOUR_API_KEY' #Get from here - https://api.nasa.gov/

    # Construct the request URL
    request_url = f"{url}?lon={longitude}&lat={latitude}&date={date}&dim={dim}&api_key={api_key}"

    # Send the request
    response = requests.get(request_url)

    # Save the image to a file
    with open('satellite_image.jpg', 'wb') as file:
        file.write(response.content)

class CNNHyperModel(HyperModel):
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes

    def build(self, hp):
        model = Sequential()
        model.add(Conv2D(filters=hp.Int('conv1_filters', min_value=16, max_value=128, step=16),
                         kernel_size=hp.Choice('conv1_kernel', values=[3, 5]),
                         activation='relu',
                         input_shape=self.input_shape))
        model.add(MaxPooling2D(pool_size=2))

        for i in range(hp.Int('num_conv_layers', min_value=1, max_value=3)):
            model.add(Conv2D(filters=hp.Int(f'conv{i+2}_filters', min_value=16, max_value=128, step=16),
                             kernel_size=hp.Choice(f'conv{i+2}_kernel', values=[3, 5]),
                             activation='relu'))
            model.add(MaxPooling2D(pool_size=2))

        model.add(Flatten())
        model.add(Dense(units=hp.Int('dense_units', min_value=32, max_value=256, step=32), activation='relu'))
        model.add(Dense(units=self.num_classes, activation='softmax'))

        model.compile(optimizer=Adam(hp.Choice('learning_rate', values=[1e-2, 1e-3])),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        return model

def remove_noise(image, image_type):
    if image_type == 'space':
        # Apply noise removal techniques for space images
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        median_filtered = cv2.medianBlur(grayscale_image, 3)
        gaussian_filtered = cv2.GaussianBlur(median_filtered, (5, 5), 0)
        bilateral_filtered = cv2.bilateralFilter(gaussian_filtered, 9, 75, 75)
        denoised_image = cv2.fastNlMeansDenoising(bilateral_filtered, None, 10, 10, 7)
        denoised_image = cv2.cvtColor(denoised_image, cv2.COLOR_GRAY2BGR)
    elif image_type == 'satellite':
        # Convert image to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        # Apply Non-local Means Denoising
        denoised_image = cv2.fastNlMeansDenoising(grayscale_image, None, h=10, templateWindowSize=7, searchWindowSize=21)
    
        # Convert the denoised image back to color
        denoised_image = cv2.cvtColor(denoised_image, cv2.COLOR_GRAY2BGR)
    else:
        raise ValueError("Invalid image type specified.")
    
    return denoised_image

input_shape = (128, 128, 3)  # Specify the input shape according to your image dimensions
num_classes = 10  # Specify the number of classes for classification

hypermodel = CNNHyperModel(input_shape, num_classes)

tuner = kerastuner.tuners.Hyperband(
    hypermodel,
    objective='val_accuracy',
    max_epochs=10,
    seed=42,
    directory='tuner_results',
    project_name='cnn_tuning'
)

def prepare_data_from_file(file_path):
    # Read the input file
    data = pd.read_csv(file_path)
    
    # Extract images, labels, and image types from the file
    images = []
    labels = []
    image_types = []
    
    for row in data.itertuples():
        image_path = row.image_path
        label = row.label
        image_type = row.image_type
        
        # Load the image
        image = cv2.imread(image_path)
        
        # Check if the image is loaded successfully
        if image is not None:
            # Store the image, label, and image type
            images.append(image)
            labels.append(label)
            image_types.append(image_type)
    
    # Convert the lists to numpy arrays
    images = np.array(images)
    labels = np.array(labels)
    image_types = np.array(image_types)
    
    return images, labels, image_types

def main(images, image_types, labels)
    # Remove noise from each image
    processed_images = [remove_noise(image, image_type) for image, image_type in zip(images, image_types)]

    # Convert the images and labels to numpy arrays
    processed_images = np.array(processed_images)
    labels = np.array(labels)

    # Perform one-hot encoding if required
    labels = keras.utils.to_categorical(labels, num_classes)

    # Perform the hyperparameter search
    tuner.search(processed_images, labels, validation_split=0.2)

    # Retrieve the best model
    best_model = tuner.get_best_models(num_models=1)[0]

    # Train the best model with the optimal hyperparameters
    best_model.fit(processed_images, labels, epochs=10, validation_split=0.2)