import re
import numpy as np
import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from flask import Flask, request, app, render_template
from werkzeug.utils import secure_filename

model = keras.models.load_model(r"crime1.h5", compile=False)
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html', methods=['GET'])
def contact():
    return render_template('contact.html')
@app.route('/prediction.html', methods=['GET'])
def prediction():
    return render_template('prediction.html')

from PIL import Image
@app.route('/predict.html',methods=['GET'])
def predict1():
    return render_template('predict.html')

@app.route('/predict.html', methods=['POST'])
def predict():
    result = ""
    if request.method == 'POST':
        try:
            file = request.files['image']
            if file:
                # Check if the file has an allowed image extension
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    file_path = os.path.join('uploads', secure_filename(file.filename))
                    file.save(file_path)
                    img = Image.open(file_path)
                    img = img.convert('RGB')  # Ensure the image is in RGB format
                    img = img.resize((64, 64))  # Resize the image to the model's expected size
                    x = keras.preprocessing.image.img_to_array(img)
                    x = np.expand_dims(x, axis=0)
                    pred = np.argmax(model.predict(x), axis=1)
                    op = ['Fighting', 'Arrest', 'Vandalism', 'Assault', 'Stealing', 'Arson', 'NormalVideos', 'Abuse', 'Explosion', 'Robbery', 'Burglary', 'Shooting', 'Shoplifting', 'RoadAccidents']
                    result = 'The predicted output is ' + str(op[pred[0]])
                else:
                    result = 'Invalid image format. Supported formats: png, jpg, jpeg, gif.'
            else:
                result = 'No image file provided.'
        except Exception as e:
            result = f'An error occurred: {str(e)}'
    return render_template("prediction.html", prediction=result)

if __name__ == '__main__':
    app.run(host='127.0.0.1')
