"""Analyse the data of the width"""

import os

import numpy as np
import matplotlib.pyplot as plt
from numpy.core.shape_base import block

#### TO FILL ####
FOLDER = "/Volumes/GUILLAUME/TP rheologie/uflu 1/water_C001H001S0001"

#### TO FILL ####

data_file = "width.csv"

data = np.genfromtxt(os.path.join(FOLDER, data_file), delimiter=",")

plt.figure()
plt.plot(data[:, 0], data[:, 1], ".k")
plt.show(block=True)