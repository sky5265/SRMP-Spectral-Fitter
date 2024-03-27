#run the code
from support_functions import *
from import_data import *
from tqdm import tqdm
import sys
from plot import *
sys.path.insert(1, '../Nahum_Fitting')
from mcmc_fitting import *
print("please put all your data files in a folder called 'data'")

filenames = []
for file in os.listdir('data'):
    if file.endswith('.txt'):
        filenames.append(file)

true_wavelength = 7775
lowerbound = 7500
upperbound = 7860

#true_wavelength = float(input('what is the true wavelength?'))
#lowerbound = float(input('what is the lowerbound?'))
#upperbound = float(input('what is the upperbound?'))

wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds = import_data(filenames, lowerbound, upperbound)

nwalkers = 20
answer = input("How many walkers do you want (20) ? ")
if is_integer(answer): 
    nwalkers = int(answer)
    answer2 = input("The current number of walkers is " + str(nwalkers) + ". Do you like that number of walkers? y/n: ")
    while answer2.lower() == 'n':
        nwalkers = int(input("How many walkers do you want (" +str(nwalkers)+ ") ? "))
        answer2 = input("The current number of walkers is " +str(nwalkers) + ". Do you like that number of walkers? y/n: ")


n_iterations =5000
answer = input("How many interations do you want (5000) ? ")
if is_integer(answer): 
    n_iterations = int(answer)
    answer2 = input("The current number of iterations is " + str(n_iterations) + ". Do you like that number of iterations? y/n: ")
    while answer2.lower() == 'n':
        n_iterations = int(input("How many iterations do you want (" +str(n_iterations)+ ")  ? "))
        answer2 = input("The current number of walkers is " + str(n_iterations) + ". Do you like that number of walkers? y/n: ")
    
mu_s, sigma_s, c_s, err_s = fitting(wavelengths_normalizeds, fluxes_normalizeds, nwalkers, loss_function, n_iterations, filenames)

real_mu_s_s, real_sigma_s_s, real_c_s_s = plot(mu_s, sigma_s, c_s, err_s, filenames, wavelengths_normalizeds, fluxes_normalizeds, wavelengths_windows, fluxes_windows, lowerbound, upperbound)

velocity_s = []
velocity_std_s = []

for filename in filenames:
    c_light = 3.0E5
    velocity = np.median(((real_mu_s_s[filename])-true_wavelength)/true_wavelength * c_light)
    velocity_std = np.std(((real_mu_s_s[filename])-true_wavelength)/true_wavelength * c_light)
    velocity_s.append(velocity)
    velocity_std_s.append(velocity_std)
    out = open('Results/Spectrum_'+ filename[:filename.index('.txt')] +'/Results_' + filename[:filename.index('.txt')] + '.txt', 'w')
    out.write('Real mean is at ' + str(np.median(real_mu_s_s[filename])) + '\n' + 'Velocity is '+ str(velocity) + ' km/s' + '\n' + 
    'Results of walkers:'+'\n'+ "Real mu's: " + str(real_mu_s_s[filename]) +'\n' + "Median of real mu's: " + str(np.median(real_mu_s_s[filename])) + '\n' + "Standard deviation of mu's: " + str(np.std(real_mu_s_s[filename])) + '\n\n'
    "Real sigma's: " + str(real_sigma_s_s[filename]) + '\n' + "Median of real sigma's: " + str(np.median(real_sigma_s_s[filename])) + "Standard deviation of sigma's: " + str(np.std(real_sigma_s_s[filename])))
    
filename = []
for file in filenames:
    file = file[:file.index('.txt')]
    filename.append(file)

plt.scatter([float(i) for i in filename], velocity_s)
plt.errorbar([float(i) for i in filename], velocity_s, velocity_std_s, ls='none')
plt.xlabel("time")
plt.ylabel("velocity ")
plt.savefig('Results' + '/Velocity_Over_Time' + '.pdf', bbox_inches='tight')
plt.close()

print("if you don't like the fit, please try again changing the window.")