from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Dropout, Reshape
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np


img_width, img_height = 224, 224
num_classes = 3


train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    '/Users/anushkaverma/PycharmProjects/CMPSC448FinalProjectPentium/rain_data/train',
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='categorical',
    classes=['cloudy', 'rain', 'shine']  # Adjust class names
)


model = Sequential([
    Reshape((img_width, img_height * 3), input_shape=(img_width, img_height, 3)),
    Bidirectional(LSTM(256, return_sequences=True)),
    Dropout(0.5),
    Bidirectional(LSTM(256)),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


model.fit(train_generator, epochs=20, steps_per_epoch=len(train_generator))

model.save('rnn_image_classifier')

model_json = model.to_json()
with open("rnn_image_classifier.json", "w") as json_file:
    json_file.write(model_json)

model.save_weights("rnn_image_classifier_weights.h5")


loaded_model = model_from_json(model_json)
loaded_model.load_weights("rnn_image_classifier_weights.h5")
