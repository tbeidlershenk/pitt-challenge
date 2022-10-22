import traceback
from flask import Flask, request, jsonify
import torch_utils as tu
import pandas as pd

 
app = Flask(__name__)
 
ALLOWED = ['bmp', 'jpg', 'png']
 
def allowed_file(filename):
   ext = filename.rsplit('.')[1]
   if ext in ALLOWED:
       return True
   return False
 
@app.route('/predict', methods=['POST'])
def predict():
   if request.method == 'POST':
       file = request.files.get('file')
       if file is None or file.filename == "":
           return jsonify({'error': 'no file'})
       if not allowed_file(file.filename):
           return jsonify({'error': 'format not supported'})
 
   try:
       # load image
       bytes = file.read()
       
       # image -> tensor
       tensor = tu.img_to_tensor(bytes)
       print(tensor.shape)
       # predict
       prediction = tu.predict_img(tensor)
       top_8_df = pd.read_csv("top_8_annotations.csv")
       df_class_name = top_8_df[["Name", "target"]]
       df_class_name.drop_duplicates(inplace=True)
       dictionary = dict(zip(df_class_name.target, df_class_name.Name))

       data = {'prediction': prediction, 'class_name': dictionary[prediction]}
       return jsonify(data)
   except Exception as e:
       print(str(e))
       print(traceback.format_exc())
       return jsonify({'error': 'error during prediction'})