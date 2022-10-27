#coding: utf-8

"""Calculate the serie for the corrective factor of TP2 rheology."""

import numpy as np
import matplotlib.pyplot as plt

H = 100 # in um
W = 110 # in um

a = H / W
# a = 0.00001
nb_it = 100
precision = 0.001


def calc_A(nb_it: int) -> float:
    """Calculate the A coefficient"""
    A = 1 / 2
    serie = 0
    for n in range(1, nb_it + 1):
        serie += (48 / ((np.pi * n) ** 5) * (1 - (-1) ** n) * np.tanh(n * np.pi / (2 * a)))
    A -= a * serie
    return A


def calc_B(nb_it: int) -> float:
    """Calculate the B coefficient"""
    serie = 0
    for n in range(1, nb_it + 1):
        serie += (48 / ((np.pi * n) ** 5) * (1 - (-1) ** n) * (1 - 1 / np.cosh(n * np.pi / (2 * a))) ** 2 / np.tanh(n * np.pi / (2 * a)))
    serie = a * serie
    return serie


def ratio_flow(A, B, x):
    """Calculate the ratio of Q2 and Q1."""
    return  (1 / x) * (A + B * (x - 1) / (x + 1)) / (A - B * (x - 1) / (x + 1))



def inverse_ratio_flow(A, B, ratio, lim1, lim2):
    """
    Take the ratio of flow rate and return the ratio of viscosity.
    
    It solves the inverse problem by dichotomy.
    """
    
    mid = (lim1 + lim2) / 2
    r = ratio_flow(A, B, mid)
    delta = lim2 - lim1
    if delta < precision:
        return lim1
    if r > ratio:
        return inverse_ratio_flow(A, B, ratio, mid, lim2)
    return inverse_ratio_flow(A, B, ratio, lim1, mid)




if __name__ == "__main__":
    A = calc_A(nb_it)
    B = calc_B(nb_it)
    print("A: ", A)
    print("B: ", B)

    print(inverse_ratio_flow(A, B, 0.70, 0, 20))
    x = np.linspace(1, 10)
    ratio = ratio_flow(A, B, x)

    plt.figure()
    plt.plot(x, ratio, label="Corrected")
    plt.plot(x, 1/ x, label="Scaling")
    plt.legend()
    plt.xlabel("$\eta_2 / \eta_1$")
    plt.ylabel("$Q_2 / Q_1$")
    plt.show(block=True)
