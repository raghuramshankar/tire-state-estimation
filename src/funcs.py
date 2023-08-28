import os
import pandas as pd


def getAMZDataset():
    """returns amz driverless 2017 dataset as pandas dataframes"""
    # get path and filenames
    dataset_path = "datasets/amz-driverless-2017/"
    file_names_path = os.getcwd() + "/" + dataset_path
    file_names = [f for f in os.listdir(file_names_path)]

    # create dict of data
    data = dict()
    for key in file_names:
        data[key.split(".")[0]] = pd.read_csv(file_names_path + key)

    return data
