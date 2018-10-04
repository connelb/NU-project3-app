import os
import numpy as np
from flask import Flask, request, jsonify, render_template

import keras
from keras.preprocessing import image
from keras import backend as K

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from jinja2 import Template


from keras.preprocessing.image import ImageDataGenerator

# from keras.preprocessing import image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads'

model = None
graph = None

# Loading a keras model with flask
# https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html


def load_model():
    global model
    global graph
    
    # model = keras.models.load_model("mnist_trained.h5")
    model = keras.models.load_model("avocado_model_trained.h5")
    graph = K.get_session().graph


load_model()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    data = {"success": False}
    if request.method == 'POST':
        # print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file to the uploads folder
            file.save(filepath)

            # Load the saved image using Keras and resize it to the mnist format of 28x28 pixels
            # image_size = (28, 28)
            image_size = (100, 100)
            # im = image.load_img(filepath, target_size=image_size, grayscale=True)
            im = image.load_img(filepath, target_size=image_size)

            # Convert the 2D image to an array of pixel values
            # image_array = prepare_image(im)
            # print(image_array)

            # Get the tensorflow default graph and use it to make predictions
            global graph
            with graph.as_default():
                test_image = image.img_to_array(im)
                test_image = np.expand_dims(test_image, axis = 0)
                # result = classifier.predict(test_image)


                # Use the model to make a prediction
                # predicted_digit = model.predict_classes(image_array)[0]
                predicted_digit = model.predict(test_image)
                # print('l',predicted_digit)
                data["prediction"] = str(predicted_digit[0][0])

                # indicate that the request was a successzz
                data["success"] = True

                if data["prediction"]  == "1.0":
                    return render_template('ripe.html')
                        # return '''<p>This avocado is ripe: '''+data["prediction"]+ '''</P>'''
                else:
                    if data["prediction"]  == "0.0":
                        return render_template('not_ripe.html')
                #         return '''<p>This avocado is NOT ripe: '''+data["prediction"]+ '''</P>'''
            
                # return '''

    return render_template('index.html')

if __name__ == "__main__":
    app.run()




# *******************************************************************
# Importing the Keras libraries and packages



                # # Initialising the CNN
                # classifier = Sequential()

                # # Step 1 - Convolution
                # classifier.add(Conv2D(32, (3, 3), input_shape = (100, 100, 3), activation = 'relu'))

                # # Step 2 - Pooling
                # classifier.add(MaxPooling2D(pool_size = (2, 2)))

                # # Adding a second convolutional layer
                # classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
                # classifier.add(MaxPooling2D(pool_size = (2, 2)))

                # # Step 3 - Flattening
                # classifier.add(Flatten())

                # # Step 4 - Full connection
                # classifier.add(Dense(units = 128, activation = 'relu'))
                # classifier.add(Dense(units = 1, activation = 'sigmoid'))

                # # Compiling the CNN
                # classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

                # # Part 2 - Fitting the CNN to the images


                # train_datagen = ImageDataGenerator(rescale = 1./255,
                #                                 shear_range = 0.2,
                #                                 zoom_range = 0.2,
                #                                 horizontal_flip = True)

                # test_datagen = ImageDataGenerator(rescale = 1./255)

                # training_set = train_datagen.flow_from_directory('Training',
                #                                                 target_size = (100, 100),
                #                                                 batch_size = 32,
                #                                                 class_mode = 'binary')

                # test_set = test_datagen.flow_from_directory('Test',
                #                             target_size = (100, 100),
                #                             batch_size = 32,
                #                             class_mode = 'binary')

                # classifier.fit_generator(training_set,
                #          steps_per_epoch = 100,
                #          epochs = 6,
                #          validation_data = test_set,
                #          validation_steps = 50)

                # test_image = image.img_to_array(im)
                # test_image = np.expand_dims(test_image, axis = 0)
                # result = classifier.predict(test_image)

                # classifier.save("avocado_model_trained2.h5")