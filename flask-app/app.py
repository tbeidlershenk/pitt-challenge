from flask import Flask, request, jsonify
import torch_utils as tu
 
app = Flask(__name__)
 
ALLOWED = ['bmp', 'jpeg', 'png']
 
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
       data = {'prediction': prediction, 'class_name': str(prediction)}
       return jsonify(data)
   except Exception as e:
       print(str(e))
       return jsonify({'error': 'error during prediction'})