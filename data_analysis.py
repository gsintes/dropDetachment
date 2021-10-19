"""Analyse the data of the width"""

import os

import numpy as np
import matplotlib.pyplot as plt

#### TO FILL ####

FOLDER = "" # Add the path of the folder where the images are saved

#### TO FILL ####

#### READ DATA ####

data_file = "width.csv"
data = np.genfromtxt(os.path.join(FOLDER, data_file), delimiter=",")
t_step = data[:, 0]
width_pixel = data[:, 1] 



plt.figure()
plt.loglog(max(t_step) - t_step, width_pixel, ".k")
plt.show(block=True)