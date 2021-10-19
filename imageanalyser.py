"""Analyse images of a droplet detachment and detect the neck width."""

import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage.filters.thresholding import threshold_otsu

###### TO BE FILLED #######
# FOLDER = "/Volumes/GUILLAUME/TP rheologie/uflu 1/water_C001H001S0001"
FOLDER = "/Volumes/GUILLAUME/TP rheologie/uflu 1/peo2_C001H001S0001"
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
    plt.pause(0.5)
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


def edge_detection(im: np.ndarray) -> List[int]:
    """Detect the edge of the drop and return its widths along the vertical.""" 
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
    plt.pause(0.001)
    plt.clf()
    return width

def neck_detection(im: np.ndarray) -> int:
    """Detect the neck and return its width."""
    widths = edge_detection(im)
    diff = widths[1:] - widths[0: len(widths) - 1]
    for i, deriv in enumerate(diff):
        if deriv > 0:
            return widths[i]
    return -1

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

def save_data(widths: List[int]) -> None:
    """Save the data to a text file."""
    textfile = open(os.path.join(FOLDER,"width.csv"), "w")
    for i, element in enumerate(widths):
        textfile.write(f"{i}, {element}\n")
    textfile.close()


if __name__ == "__main__":
    image_list = [os.path.join(FOLDER, f) for f in os.listdir(FOLDER) if f.endswith(".png")]
    limits = select_roi(image_list[-1])
    neck_widths = []
    plt.ion()

    for im_name in image_list:
        im = mpimg.imread(im_name)
        im = crop_image(im, limits)
        neck_widths.append(neck_detection(im))
    plt.close()
    plt.ioff
    save_data(neck_widths)