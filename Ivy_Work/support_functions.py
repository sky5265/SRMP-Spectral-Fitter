import numpy as np
import os
import sys
import emcee
import corner
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit


def normal_dist (x, mu, sigma, c):
  A = (1/(sigma*(2*np.pi)**0.5))
  B = -1*(x-mu)**2/(2*sigma**2)
  y = -1*A*np.exp(B)+ c
  return y

def loss_func (var, x, y_true):
    mu, sigma, c, err = var
    if err < 0 or err > 0.25 or 0 > sigma  or sigma > 5 or c < 0 or mu > 1 or -1 > mu:
        return -np.inf
    y_fitted = normal_dist(x = x, mu = mu, sigma = sigma, c = c)
    return -np.sum((y_true - y_fitted)**2)/err**2 - err
    


