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
    
def import_data (filename):
    data = np.loadtxt(filename)
    wavelengths = data[:,0]
    fluxes = data[:,1]
    matplotlib.use('TkAgg')
    plt.plot(wavelengths, fluxes, "b-")
    plt.xlabel("Wavelengths (Angstrom)")
    plt.ylabel("Flux ")
    plt.show()
    plt.savefig('ori_data.pdf', bbox_inches='tight')
    return  wavelengths, fluxes

def window_range (wavelengths, fluxes, x1, x2):
    idx = np.where ((wavelengths > x1) & (wavelengths < x2))

    wavelengths_window = wavelengths[idx]
    fluxes_window = fluxes[idx]

    wavelengths_normalized = (wavelengths_window - np.mean(wavelengths_window))/np.std(wavelengths_window)
    fluxes_normalized = (fluxes_window)/np.max(fluxes_window)


    plt.plot(wavelengths_window, fluxes_window, "b-")
    plt.xlabel("Wavelengths (Angstrom)")
    plt.ylabel("Flux ")
    plt.show()

    plt.plot(wavelengths_normalized, fluxes_normalized, "b-")
    plt.xlabel("Wavelengths (Angstrom)")
    plt.ylabel("Flux ")
    plt.show()

    return wavelengths_window, fluxes_window, wavelengths_normalized, fluxes_normalized

def runwalker (nwalkers, ndim, n_iterations,mu_reasonable, sigma_reasonable, c_reasonable, err_reasonable):
    initial_guesses = []
    for walker in range(nwalkers):
        mu_guess = mu_reasonable * (1+np.random.random())
        sigma_guess = sigma_reasonable * (1+np.random.random())
        c_guess = c_reasonable * (1+np.random.random())
        err_guess = err_reasonable * (1+np.random.random())
        initial_guesses.append([mu_guess, sigma_guess, c_guess, err_guess])
    sampler = emcee.EnsembleSampler(nwalkers, ndim, loss_func, kwargs = {"y_true":fluxes_normalized, "x":wavelengths_normalized})
    sampler.run_mcmc(initial_guesses, n_iterations, progress = True)
    return sampler

def plot (samples, sampler):
    found_mu_s = samples[:, :, 0]
    found_sigma_s = samples[:, :, 1]
    found_c_s = samples[:, :, 2]
    found_err_s = samples[:, :, 3]

    plt.plot(range(0, len(found_mu_s)), found_mu_s, color = 'grey')
    plt.ylabel(r'mu', fontsize = 35)
    plt.xlabel("Iterations", fontsize = 35)
    plt.show()
    plt.close()

    plt.plot(range(0, len(found_sigma_s)), found_sigma_s, color = 'grey')
    plt.ylabel(r'sigma', fontsize = 35)
    plt.xlabel("Iterations", fontsize = 35)
    plt.show()
    plt.close()

    plt.plot(range(0, len(found_c_s)), found_c_s, color = 'grey')
    plt.ylabel(r'c', fontsize = 35)
    plt.xlabel("Iterations", fontsize = 35)
    plt.show()
    plt.close()

    plt.plot(range(0, len(found_err_s)), found_err_s, color = 'grey')
    plt.ylabel(r'err', fontsize = 35)
    plt.xlabel("Iterations", fontsize = 35)
    plt.show()
    plt.close()

    last_mu_s = found_mu_s[-1,:]
    last_sigma_s = found_sigma_s[-1,:]
    last_c_s = found_c_s[-1,:]
    last_err_s = found_err_s[-1,:]

    x0 = np.linspace(-1.5,1.5,500)
    plt.scatter(wavelengths_normalized, fluxes_normalized, color = "red", linewidth = 0.5, label = filename)
    labels_added = []
    for walker in range(len(last_mu_s)):
        mu = last_mu_s[walker]
        sigma = last_sigma_s[walker]
        c = last_c_s[walker]
        y_fitted = normal_dist(x = x0, mu = mu, sigma= sigma, c = c)
        if 'Fitted' not in labels_added:
            plt.plot(x0, y_fitted, color = 'green', linewidth = 0.1, label = 'Fitted')
            labels_added.append("Fitted")
        else:
            plt.plot(x0, y_fitted, color = 'green', linewidth = 2)

    plt.xlabel('x', fontsize = 20)
    plt.ylabel(r'y', fontsize = 20)
    plt.legend(fontsize = 10)
    plt.show()

    flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
    labels = ['mu', 'sigma', 'c', 'err']
    fig = corner.corner(flat_samples, labels=labels);

    last_mu_s = found_mu_s[-1,:]
    last_sigma_s = found_sigma_s[-1,:]
    last_err_s = found_err_s[-1,:]

    real_mu_s = last_mu_s * np.std(wavelengths_window) + np.mean(wavelengths_window)
    real_sigma_s = last_sigma_s * np.std(wavelengths_window) 

    return real_mu_s, real_sigma_s