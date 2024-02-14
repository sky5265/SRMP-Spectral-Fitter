#plot data from fitting
from support_functions import *
from import_data import *
from fitting import *

real_mu_s, real_sigma_s = plot(samples, sampler)

c = 3.0E5
velocity = (np.mean(real_mu_s)-true_wavelength)/true_wavelength * c
out = open('Results.txt','w')
out.write('Real mean is at ' + str(np.mean(real_mu_s)) + '\n' + 'Velocity is '+ str(velocity) + ' km/s')