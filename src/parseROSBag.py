# %%
from bagpy import bagreader
import os
import sys

if __name__ == "__main__":
    """creates csvs from rosbag"""
    # add base folder path
    base_path = os.path.dirname(os.path.realpath(os.getcwd())) + "/"
    sys.path.append(base_path)

    # get filenames in dataset folder
    dataset_path = "datasets/amz-driverless-2017/"
    filename = [f for f in os.listdir(base_path + dataset_path) if f.endswith(".bag")][
        0
    ]

    # read rosbag
    b = bagreader(base_path + dataset_path + filename)

    # convert rosbag to csvs
    [
        b.message_by_topic(topic)
        for topic in b.topic_table["Topics"]
        if topic != "/velodyne_points"
    ]
