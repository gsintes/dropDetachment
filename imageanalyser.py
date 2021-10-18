"""Anlyse images of a droplet detachment and detect the neck width."""

import os
import time
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy.core.shape_base import block
from skimage.filters.thresholding import threshold_otsu

###### TO BE FILLED #######
FOLDER = "/Volumes/GUILLAUME/TP rheologie/uflu 1/water_C001H001S0001"
# FOLDER = "/Volumes/GUILLAUME/TP rheologie/uflu 1/peo2_C001H001S0001"
###### TO BE FILLED #######

def select_roi(im_name: str) -> List[Tuple[int, int]]:
    """Select graphically a region of interest."""
    plt.figure()
    im = mpimg.imread(os.path.join(FOLDER, im_name))
    plt.imshow(im, cmap="gray")
    plt.title("Select two opposing corners of the ROI")
    coords_in = plt.ginput(2)
    coords = []
    for point in coords_in:
        coords.append(tuple([int(x) for x in point]))
    plt.close()
    plt.ion()
    plt.imshow(crop_image(im, coords), cmap="gray")
    plt.draw()
    plt.pause(2)
    plt.close()
    return coords


def crop_image(im: np.ndarray, coord_lim: List[Tuple[int, int]]) -> np.ndarray:
    """Take an image and crop it according to the coordinates given."""
    xmin = min([coord_lim[0][0], coord_lim[1][0]])
    xmax = max([coord_lim[0][0], coord_lim[1][0]])
    ymin = min([coord_lim[0][1], coord_lim[1][1]])
    ymax = max([coord_lim[0][1], coord_lim[1][1]])
    return im[ymin : ymax, xmin:xmax]


def binerize(im: np.ndarray) -> np.ndarray:
    """Binerize an image using Otsu's method."""
    threshold = threshold_otsu(im)
    bin_im = (im > threshold) * 1
    return bin_im


def neck_detection(im: np.ndarray) -> int:
    """Detect the neck of the drop and return its width.""" 
    bin_im = binerize(im)
    edges = []
    for i in range(im.shape[0]):
        edges.append(limits_line(bin_im, i))
    edges = np.array(edges)
    width = edges[:, 1] - edges[:, 0]
    coord_edges = []
    for i in range(edges.shape[0]):
        for j in range(2):
            coord_edges.append([i, edges[i ,j]])
    coord_edges = np.array(coord_edges)
    plt.imshow(bin_im, cmap="gray")
    plt.plot(coord_edges[:, 1], coord_edges[:, 0], "*r")
    plt.draw()
    plt.pause(1)
    return min(width)


def limits_line(bin_im: np.ndarray, line: int) -> int:
    """Detect the edges of the drop at the line."""
    values = bin_im[line, :]
    diff = values[1:] - values[:-1]
    for i in range(len(diff)):
        if diff[i] == -1:
            left_lim = i
            break
    for i in range(len(diff) -1, 0, -1):
        if diff[i] == 1:
            right_lim = i
            break
    try:
        width = right_lim - left_lim
        if width >= 0:
            return (left_lim, right_lim)
        else:
            return (0, len(diff) - 1)
    except UnboundLocalError:
        return (0, len(diff) - 1)

 
if __name__ == "__main__":
    image_list = [os.path.join(FOLDER, f) for f in os.listdir(FOLDER) if f.endswith(".png")]
    limits = select_roi(image_list[-1])

    # test_im = crop_image(mpimg.imread(image_list[-5]), limits)
    # bin_im = binerize(test_im)
    # print(neck_detection(test_im))
    neck_widths = []
    plt.ion()
    plt.show()
    for im_name in image_list:
        im = mpimg.imread(im_name)
        im = crop_image(im, limits)
        neck_widths.append(neck_detection(im))
