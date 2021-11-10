# Rheology practical sessions

This code is aimed for the analysis of data from the experimental sessions from the rheology class.
It is composed of three programs.

# Prerequisite

Install Python 3 on your computer and install all the modules describres in requirements.txt. (If you install anaconda Python distribution, you will have the modules already installed, else install them with pip or conda.)

# Drop detachment image analysis

imageanalyser.py is made to extract the width of the neck from a detaching droplet.

## Use instruction

Set the folder path in the code and run the program, on the first image, select two diagonally opposing corners to set the region of interest. The data will be saved in width.txt in the image folder.

## Image analysis techniques

The image are binarized using Otsu's method to separate the dark region of the droplet from the background, then the edges are detected and the first minumum of the width coming from the needle is found and returned. The program does this for all pictures in the folder.

# Data analysis from drop detachment

This code is for plotting purposes from image data. Once the image analysis is done, run this code setting the folder, and choosing the plots you want to show. 
To be able to re run the code, you need to close all plotting windows.

# Correction for viscosity measurement in Y channel

TPmicroflu.py is used to take into account the fact that the channel is not an Hele-Shaw cell. It will plot the corrected and scaling of the ratio of flow rates such as the two widths are equal. And once you estimated from your data the ratio of flow rates such as the widths are equal, you can use inverse_ratio_flow to use a dichotomy method to determine the ratio of viscosity you add in your sample.