from random import shuffle
from ConvNeuralNetwork import ConvNeuralNetwork
from CustomDataset import CustomDataset
from createDateframe import create_dictionary, linkNameNDC, top_8_df
from manipulateImage import img_crop_black
from top_8_annotation_creator import create_df
import pandas as pd
import os
import torch
from CustomDataset import CustomDataset
from torch.utils.data import DataLoader
from train_test import train, test

# create ideal dataframe
all_labels = pd.read_csv("content/PillDataset/all_labels.csv")
directory_ref = pd.read_csv("content/PillDataset/directory_consumer_grade_images.csv", dtype={"NDC11":str})

dict_ndc_name = create_dictionary(directory_ref)
all_labels = linkNameNDC(all_labels, dict_ndc_name)

top_8_df = top_8_df(all_labels)

if(not os.path.exists("content/PillDataset/clean_data")):
    # Create clean image dataset
    for index, row in top_8_df.iterrows():
        img_crop_black("content/PillDataset/" + row["image_path"])

create_df(top_8_df)
        
# create dataset
dataset = CustomDataset("top_8_annotations.csv", "content/PillDataset")

train_set, test_set = torch.utils.data.random_split(dataset, [400, 101])

batch_size = 10

train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=1, shuffle=True)

# test model
model = ConvNeuralNetwork()
model = train(model, 5, train_loader)
test(model, test_set)