import os
from flask import Flask, request, jsonify, render_template

import keras
from keras.preprocessing import image
from keras import backend as K

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads'

model = None
graph = None

# Loading a keras model with flask
# https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html


def load_model():
    global model
    global graph
    model = keras.models.load_model("mnist_trained.h5")
    graph = K.get_session().graph


load_model()


def prepare_image(img):
    # Convert the image to a numpy array
    img = image.img_to_array(img)
    # Scale from 0 to 255
    img /= 255
    # Invert the pixels
    img = 1 - img
    # Flatten the image to an array of pixels
    image_array = img.flatten().reshape(-1, 28 * 28)
    # Return the processed feature array
    return image_array


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
            image_size = (28, 28)
            im = image.load_img(filepath, target_size=image_size, grayscale=True)

            # Convert the 2D image to an array of pixel values
            image_array = prepare_image(im)
            # print(image_array)

            # Get the tensorflow default graph and use it to make predictions
            global graph
            with graph.as_default():

                # Use the model to make a prediction
                predicted_digit = model.predict_classes(image_array)[0]
                data["prediction"] = str(predicted_digit)

                # indicate that the request was a success
                data["success"] = True
                return '''
                <!doctype html>
                            <html lang="en">

                            <head>
                            <!-- Required meta tags -->
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                            <!-- Bootstrap CSS -->
                            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
                                crossorigin="anonymous">

                            <title>Results:</title>
                            </head>

                            <body>
                            <div class="jumbotron">
                            <a href="" class="btn btn-primary btn-sm active" role="button" aria-pressed="true">Home</a>
                            <br>
                            <br>
                                <h1 class="display-4">Analysis Results:</h1>
                                <p class="lead"><strong>Outcome:</strong> '''+str(data["success"])+'''</p>
                                <p class="lead"><strong>Probability of detection:</strong> '''+str(data["prediction"])+'''</p>
                                
                            </div>
                            <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
                                crossorigin="anonymous"></script>
                            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49"
                                crossorigin="anonymous"></script>
                            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy"
                                crossorigin="anonymous"></script>
                            </body>
                        </html>
                '''

    return render_template('index.html')

if __name__ == "__main__":
    app.run()
