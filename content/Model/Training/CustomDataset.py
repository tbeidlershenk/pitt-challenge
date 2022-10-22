import os
from PIL import Image
import torch
import pandas as pd
from torchvision import transforms
from torch.utils.data import Dataset

class CustomDataset(Dataset):
  def __init__(self, csv_file, root_dir):
    #root_dir will be root_dir where images are located
    self.root_dir = root_dir

    #transforms
    self.transform = transforms.Compose([
      transforms.RandomApply(
          torch.nn.ModuleList([
              transforms.RandomRotation(degrees=(0, 360)),
              transforms.RandomAutocontrast(),
              transforms.GaussianBlur(kernel_size=(5,9), sigma=(0.1, 5)),
          ]),
      ),

      transforms.ToTensor(),
    ])

    # import csv_file
    self.annotations = pd.read_csv(root_dir + "/" + csv_file)
    # self.data contains list of [image path, pill name]
    self.data = [list(i) for i in zip(self.annotations["images"], self.annotations["Name"])]
    print(self.data)

    # class map is dictionary of pill : id
    self.class_map = {}
    for name, target in zip(self.annotations["Name"].unique(), self.annotations["target"].unique()):
      self.class_map[name] = target
    #print(self.class_map)
  
  def __len__(self):
    return len(self.data)

  def __getitem__(self, idx):
    img_path, class_name = self.data[idx]
    img_path = os.path.join(self.root_dir, "clean_data/", img_path)
    image = Image.open(img_path)
    class_id = self.class_map[class_name]
    
    tensor_image = self.transform(image)

    class_id = torch.tensor([class_id])

    return tensor_image, class_id

