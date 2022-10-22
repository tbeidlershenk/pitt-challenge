import torch
from torch import nn
import torch.nn.functional as F
 
class ConvNeuralNetwork(nn.Module):
   def __init__(self):
       super().__init__()
       self.cnn_layers = nn.Sequential(
           nn.Conv2d(1, 3, kernel_size=3, stride=1, padding=1),
           nn.BatchNorm2d(3),
           nn.ReLU(inplace=True),
           nn.AvgPool2d(kernel_size=2, stride=2),
           nn.Conv2d(3, 6, kernel_size=3, stride=1, padding=1),
           nn.BatchNorm2d(6),
           nn.ReLU(inplace=True),
           nn.AvgPool2d(kernel_size=2, stride=2)
       )
       self.linear_layers = nn.Sequential(
           nn.Linear(294, 100),
           nn.Linear(100, 10)
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