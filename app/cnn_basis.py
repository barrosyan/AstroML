import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import keras
from keras.layers import Dropout
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Activation
import os
import pickle
from datetime import datetime
import requests

testfolder='test'
trainfolder='train'

train_datagen=ImageDataGenerator(rescale=1./255,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)
test_datagen=ImageDataGenerator(rescale=1./255)

train_generator=train_datagen.flow_from_directory(
    directory=r'train',
    target_size=(50,50),
    batch_size=50,
    class_mode='categorical'
)

test_generator=train_datagen.flow_from_directory(
    directory=r'test',
    target_size=(50,50),
    batch_size=50,
    class_mode='categorical'
)

model=Sequential()
model.add(Conv2D(64, kernel_size=(10,10),activation='relu',input_shape=[50,50,3]))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Conv2D(256,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10,activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

history=model.fit_generator(train_generator,
                   steps_per_epoch=16,
                   epochs=50,
                   validation_data=test_generator,
                   validation_steps=16
)