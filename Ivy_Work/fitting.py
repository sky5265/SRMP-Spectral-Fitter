#fitting process, output samples+sampler

from support_functions import *
from import_data import filenames, wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds

ndim = 4
nwalkers = 32
n_iterations = 5000

mu_reasonable = 0.1
sigma_reasonable = 1
c_reasonable = 0.6
err_reasonable = 0.03

def runwalker (nwalkers, ndim, n_iterations,mu_reasonable, sigma_reasonable, c_reasonable, err_reasonable):
    initial_guesses = []
    for filename in filenames:
        for walker in range(nwalkers):
            mu_guess = mu_reasonable * (1+np.random.random())
            sigma_guess = sigma_reasonable * (1+np.random.random())
            c_guess = c_reasonable * (1+np.random.random())
            err_guess = err_reasonable * (1+np.random.random())
            initial_guesses.append([mu_guess, sigma_guess, c_guess, err_guess])
        sampler = emcee.EnsembleSampler(nwalkers, ndim, loss_func, kwargs = {"y_true":fluxes_normalizeds[filename], "x":wavelengths_normalizeds[filename]})
        sampler.run_mcmc(initial_guesses, n_iterations, progress = True)
        return sampler
    
sampler = runwalker(nwalkers, ndim, n_iterations,mu_reasonable, sigma_reasonable, c_reasonable, err_reasonable)
samples = sampler.get_chain()