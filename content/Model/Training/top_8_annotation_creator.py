from pandas.io.common import file_exists
import csv

def create_df(top_8_df):
    top_pill_names = top_8_df["Name"].unique().tolist()

    top_8_annotations = top_8_df[["Name", "images"]]
    name_to_number = []

    # gets pill name and corresponds to number to write to df
    for index, row in top_8_df.iterrows():
        pill_name = row["Name"]
        name_to_number.append(top_pill_names.index(pill_name))

    top_8_annotations["target"] = name_to_number

    top_8_annotations.to_csv("content/PillDataset/top_8_annotations.csv", index=False)
