# %%
import os
import pandas as pd
import numpy as np
import sys


class extendedKFBatt:
    def __init__(self, N):
        """add parent path"""
        self.parentPath = os.getcwd()

        """number of iterations"""
        self.N = N

        """initial estimates"""
        """states: vx, vy, psidot, ax, ay"""
        self.xHat = np.array(
            [
                np.array([0.0]),
                np.array([0.0]),
                np.array([0.0]),
                np.array([0.0]),
                np.array([0.0]),
            ]
        )

        """initial covariance"""
        self.sigmaX = np.diag([1e-5, 1e-5, 1e-5, 1e-5, 1e-5])

        """process noise covariance"""
        vxVar = 1e1
        vyVar = 1e1
        psidotVar = 1e1
        axVar = 1e1
        ayVar = 1e1
        self.sigmaW = np.diag([vxVar, vyVar, psidotVar, axVar, ayVar])

        """sensor noise covariance"""
        """measurements: vx, vy, psidot, ax, ay"""
        self.sigmaV = np.array(
            [
                np.array([1e-3]),
                np.array([1e-3]),
                np.array([1e-3]),
                np.array([1e-3]),
                np.array([1e-3]),
            ]
        )

    def runKF(self):
        """import dataframe"""
        self.getAMZDataset()

        """limit timesteps"""
        self.N = min(self.N, len(self.df))

        """reserve storage for variables"""
        # states
        self.vx_store = np.zeros((self.N, 1)).flatten()
        self.vx_store[0] = self.xHat[0]
        self.vy_store = np.zeros((self.N, 1)).flatten()
        self.vy_store[0] = self.xHat[1]
        self.psidot_store = np.zeros((self.N, 1)).flatten()
        self.psidot_store[0] = self.xHat[2]
        self.ax_store = np.zeros((self.N, 1)).flatten()
        self.ax_store[0] = self.xHat[3]
        self.ay_store = np.zeros((self.N, 1)).flatten()
        self.ay_store[0] = self.xHat[4]

        # measurements
        self.vx_optical_store = np.zeros((self.N, 1)).flatten()
        self.vy_optical_store = np.zeros((self.N, 1)).flatten()
        self.psidot_imu_store = np.zeros((self.N, 1)).flatten()
        self.ax_imu_store = np.zeros((self.N, 1)).flatten()
        self.ay_imu_store = np.zeros((self.N, 1)).flatten()

        # kalman filter variables

        # create df
        self.storeDF = pd.DataFrame(
            {
                "vx": self.vx_store,
                "vy": self.vy_store,
                "psidot": self.psidot_store,
                "ax": self.ax_store,
                "ay": self.ay_store,
                "vx_optical": self.vx_optical_store,
                "vy_optical": self.vy_optical_store,
                "psidot_imu": self.psidot_imu_store,
                "ax_imu": self.ax_imu_store,
                "ay_imu": self.ay_imu_store,
            }
        )

        """iterate through KF"""
        # self.iterKF()

    def getAMZDataset(self):
        """returns amz driverless 2017 dataset as pandas dataframes"""
        # get path and filenames
        dataset_path = "datasets/amz-driverless-2017/"
        file_names_path = self.parentPath + "/" + dataset_path
        file_names = [f for f in os.listdir(file_names_path)]

        # create dict of data
        self.df = dict()
        for key in file_names:
            self.df[key.split(".")[0]] = pd.read_csv(file_names_path + key)

    def genMeasurement(self, i):
        # wheel_rpm
        nx_wheel = self.df["wheel_rpm"]["quaternion.x"][i]
        ny_wheel = self.df["wheel_rpm"]["quaternion.y"][i]
        nz_wheel = self.df["wheel_rpm"]["quaternion.z"][i]
        nw_wheel = self.df["wheel_rpm"]["quaternion.w"][i]

        # imu
        psidot_imu = self.df["imu"]["angular_velocity.z"][i]
        ax_imu = self.df["imu"]["linear_acceleration.x"][i]
        ay_imu = self.df["imu"]["linear_acceleration.y"][i]

        # optical speed sensor
        vx_optical = self.df["optical_speed_sensor"]["twist.linear.x"][i]
        vy_optical = self.df["optical_speed_sensor"]["twist.linear.y"][i]
        psidot_optical = self.df["optical_speed_sensor"]["twist.linear.x"][i]

        # gps
        px_gps = self.df["gps"]["latitude"][i]
        py_gps = self.df["gps"]["longitude"][i]

        z = np.array([vx_optical], [vy_optical], [psidot_imu], [ax_imu], [ay_imu])
        z = z + self.sigmaV @ np.random.randn(1, 1)
        return z.astype(float)

    def genSR(self, torque):
        pass

    def iterKF(self):
        pass


if __name__ == "__main__":
    if "__ipython__":
        # add base folder path
        sys.path.append(os.path.dirname(os.path.realpath(os.getcwd())))
        N = 100
        obj = extendedKFBatt(N)
        # change parent path to base folder
        obj.parentPath = os.path.dirname(os.getcwd())
        obj.runKF()

    print("Done")
