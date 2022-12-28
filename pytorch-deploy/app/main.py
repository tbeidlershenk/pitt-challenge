import traceback
from flask import Flask, request, jsonify
from app.torch_utils import img_to_tensor, predict_img
import pandas as pd
from app.ConvNeuralNetwork import ConvNeuralNetwork
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image


app = Flask(__name__)
CORS(app)

ALLOWED = ['bmp', 'jpg', 'png', 'jpeg']


def allowed_file(filename):
    ext = filename.rsplit('.')[1]
    if ext in ALLOWED:
        return True
    return False


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.get_json()
        
        if file is None:
            return jsonify({'error': 'no file'})

        # if file.find("base64") == -1 or allowed_file("." + file[11:file.index(";base64")]):
        #     return jsonify({'error': 'format not supported'})
        
        print("File: ", file)
        data = file.split("base64")[1]
        im = Image.open(BytesIO(base64.b64decode(data)))

    try:
        # load image

        # image -> tensor
        tensor = img_to_tensor(im)
        print(tensor.shape)
        # predict
        prediction = predict_img(tensor)
        top_8_df = pd.read_csv("app/top_8_annotations.csv")
        df_class_name = top_8_df[["Name", "target"]]
        df_class_name.drop_duplicates(inplace=True)
        dictionary = dict(zip(df_class_name.target, df_class_name.Name))

        data = {'prediction': prediction, 'class_name': dictionary[prediction]}
        return jsonify(data)
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
        return jsonify({'error': 'error during prediction'})
