# %%
from src.funcs import getAMZDataset

if "__ipython__":
    %load_ext autoreload
    %autoreload 2

if __name__ == "__main__":
    # get dataset
    data = getAMZDataset()
    wheel_rpm = data["wheel_rpm"]
    imu = data["imu"]
    optical_speed_sensor = data["optical_speed_sensor"]
    gps = data["gps"]


