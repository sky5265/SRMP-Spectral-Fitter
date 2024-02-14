#fitting process, output samples+sampler
from support_functions import *
from import_data import *
from import_data import fluxes_normalized

ndim = 4
nwalkers = 32
n_iterations = 5000

mu_reasonable = 0.1
sigma_reasonable = 1
c_reasonable = 0.6
err_reasonable = 0.03

sampler = runwalker(nwalkers, ndim, n_iterations,mu_reasonable, sigma_reasonable, c_reasonable, err_reasonable)
samples = sampler.get_chain()