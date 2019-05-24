import keras
#######################################################################################################################
# The hierarchy of dataset directary should be as follow:
# dataset
#   --> train
#       --> 0_Stroma
#       --> 1_Non_ROI
#       --> 2_Tumour
#       --> 3_Lymphocyte
#   --> valid
#       --> 0_Stroma
#       --> 1_Non_ROI
#       --> 2_Tumour
#       --> 3_Lymphocyte
train_dataset_path = './dataset/train'
valid_dataset_path = './dataset/valid'

# training data generator
train_datagen = keras.preprocessing.image.ImageDataGenerator(zca_whitening=False, horizontal_flip=True, vertical_flip=True)
train_generator = train_datagen.flow_from_directory(train_dataset_path, target_size=(224, 224), batch_size=64, shuffle=True, seed=10, class_mode='categorical')

# validation data generator
valid_datagen = keras.preprocessing.image.ImageDataGenerator(zca_whitening=False, horizontal_flip=False, vertical_flip=False)
valid_generator = valid_datagen.flow_from_directory(train_dataset_path, target_size=(224, 224), batch_size=64, shuffle=False, seed=10, class_mode='categorical')

# model training and validation
model = keras.applications.mobilenet.MobileNet(include_top=True, weights=None, classes=4)
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.fit_generator(train_generator, epochs=2, verbose=1, validation_data=valid_generator)
model.save('../models/MobileNet.hdf5')