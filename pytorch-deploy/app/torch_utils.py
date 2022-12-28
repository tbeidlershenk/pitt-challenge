import torch
import torchvision.transforms as tsf
from PIL import Image
import io
import numpy
from torch import nn
import torch.nn.functional as F

#load model
class ConvNeuralNetwork(nn.Module):
   def __init__(self):
       super().__init__()
       self.cnn_layers = nn.Sequential(
           nn.Conv2d(3, 3, kernel_size=8, stride=3, padding=1),
           nn.BatchNorm2d(3),
           nn.ReLU(inplace=True),
           nn.AvgPool2d(kernel_size=2, stride=2),
           nn.Conv2d(3, 6, kernel_size=8, stride=3, padding=1),
           nn.BatchNorm2d(6),
           nn.ReLU(inplace=True),
           nn.AvgPool2d(kernel_size=2, stride=2)
       )
       self.linear_layers = nn.Sequential(
           nn.Linear(150, 50),
           #nn.Linear(1000, 100),
           nn.Linear(50, 8)
       )
      
   def forward(self, x):
       x = self.cnn_layers(x)
       x = x.view(x.size(0), -1)
       x = self.linear_layers(x)
       return F.log_softmax(x)
 
   def predict(self, tensor):
       prediction = self.forward(tensor)
       print(prediction)
       return torch.argmax(prediction)


# turn image to tensor
def img_to_tensor(img_bytes):
   transform = tsf.Compose([
       #tsf.Grayscale(num_output_channels=1),
       tsf.Resize((224,224)),
       tsf.ToTensor()
       #tsf.Normalize((0.1307,),(0.3081,))
   ])
   image = img_bytes
   numpy.array(image).shape
   # reverse (white -> black)
   tensor = 1-transform(image).unsqueeze(0)
   print(tensor.shape)
   #print(tensor)
   return tensor

#predict
def predict_img(tensor):
   guess = model.predict(tensor)
   print(guess)
   return guess.item()

# load the model
model = ConvNeuralNetwork()
model.load_state_dict(torch.load("app/39_6state.pt"))
model.eval()