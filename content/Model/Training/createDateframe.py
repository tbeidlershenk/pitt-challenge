import pandas as pd
import torch
from torch import nn
import torchvision
from torchvision import datasets
from torchvision import transforms
from torchvision.transforms import ToTensor
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from IPython.display import display

# Add pill_name column to all_labels
def create_dictionary(directory_ref):
    # Creates a dictionary of NDC11 IDs and Pill Name
    df_ndc_name = directory_ref[["NDC11", "Name"]].copy()
    df_ndc_name.drop_duplicates(inplace=True)
    dict_ndc_name = df_ndc_name.set_index("NDC11").to_dict()
    # display(df_ndc_name)
    #print(dict_ndc_name["Name"])
    return dict_ndc_name

# Extract PillType_ID to NDC11
def pillToNDC(pillType):
    first_part = pillType[0].split("_")[0]
    first_part = first_part.replace("-","")
    
    try:
        check_format = int(first_part)
    except ValueError: 
        image_name = pillType[1].split(".")[0]
        image_name = image_name.split("_")[0]
        
        if len(image_name.split("-")[1]) < 4:
            zero_to_add = 4 - len(image_name.split("-")[1])
            for i in range(zero_to_add):
                image_name = image_name[:6] + "0" + image_name[6:]
                
        if len(image_name.split("-")[0]) < 5:
            zero_to_add = 5 - len(image_name.split("-")[0])
            for i in range(zero_to_add):
                image_name = "0" + image_name
            
        first_part = image_name.replace("-", "")
        first_part = str(first_part)
        
    return first_part

def linkNameNDC(all_labels, dict_ndc_name):
    all_labels["NDC11"] = all_labels[["pilltype_id", "images"]].apply(pillToNDC, axis=1)

    all_labels
    #for key in dict_ndc_name.keys():
        
    # Link Name with NDC11
    name = []
    remove_rows = []
    not_found_num = 0
    for index, row in all_labels.iterrows():
        ndc = row["NDC11"]
        if len(str(ndc)) == 11:
            pill_name = dict_ndc_name["Name"][str(ndc)]
            name.append(pill_name.upper())
        else:
            not_found = True
            for key in (dict_ndc_name["Name"]).keys():
                if str(ndc) in key:
                    name.append(dict_ndc_name["Name"][str(key)].upper())
                    not_found = False
                    break
            if(not_found == True):
                #print(f"Pill ID {ndc} not found!")
                remove_rows.append(index)
                #print(f"Corresponding Row: {row}")
                not_found_num += 1
                
    #print(not_found_num)
    #print(len(all_labels["label"].unique()))

    all_labels.drop(remove_rows, inplace=True)
    all_labels["Name"] = name

    all_labels.reset_index(inplace=True, drop=True)

    return all_labels

def top_8_df(all_labels):
    top_8_df = all_labels[all_labels["Name"] == "LEVOTHYROXINE SODIUM"]
    top_8_df = pd.concat([top_8_df, all_labels[all_labels["Name"] == "LISINOPRIL"]])
    top_8_df = pd.concat([top_8_df, all_labels[all_labels["Name"] == "SIMVASTATIN"]])
    top_8_df = pd.concat([top_8_df, all_labels[all_labels["Name"] == "WARFARIN SODIUM"]])
    top_8_df = pd.concat([top_8_df, all_labels[all_labels["Name"] == "GLYBURIDE"]])
    top_8_df = pd.concat([top_8_df, all_labels[all_labels["Name"] == "PREDNISONE"]])
    top_8_df = pd.concat([top_8_df, all_labels[all_labels["Name"] == "SOTALOL HYDROCHLORIDE"]])
    top_8_df = pd.concat([top_8_df, all_labels[all_labels["Name"] == "RISPERIDONE TABLETS USP"]])
    return top_8_df








#image modifications
