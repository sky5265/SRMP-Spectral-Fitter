#plot data from fitting
from support_functions import *
from import_data import filenames, wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds, true_wavelength
from import_data import *
from fitting import sampless, samplers
from tqdm import tqdm

real_mu_s_s = {}
real_sigma_s_s = {}
real_c_s_s ={}

def plot (sampless, samplers):
    for filename in filenames:
        samples = sampless[filename]
        sampler = samplers[filename]
        
        found_mu_s = samples[:, :, 0]
        found_sigma_s = samples[:, :, 1]
        found_c_s = samples[:, :, 2]
        found_err_s = samples[:, :, 3]

        last_mu_s = found_mu_s[-1,:]
        last_sigma_s = found_sigma_s[-1,:]
        last_c_s = found_c_s[-1,:]
        last_err_s = found_err_s[-1,:]

        x0 = np.linspace(-1.5,1.5,500)
        plt.scatter(wavelengths_normalizeds[filename], fluxes_normalizeds[filename], color = "red", linewidth = 0.5, label = filename)
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
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'Normalized_fit_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()
      
        flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
        labels = ['mu', 'sigma', 'c', 'err']
        fig = corner.corner(flat_samples, labels=labels);
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'Normalized_corner_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()

        real_mu_s_s[filename] = last_mu_s * np.std(wavelengths_windows[filename]) + np.mean(wavelengths_windows[filename])
        real_sigma_s_s[filename] = last_sigma_s * np.std(wavelengths_windows[filename]) 
        real_c_s_s[filename] = last_c_s* np.std(fluxes_windows[filename]) + np.mean(fluxes_windows[filename])
        
        x1 = np.linspace(lowerbound,upperbound,500)
        plt.scatter(wavelengths_windows[filename], fluxes_windows[filename], color = "red", linewidth = 0.5, label = filename)
        labels_added = []
        for walker in range(len(last_mu_s)):
            mu = last_mu_s[walker]
            sigma = last_sigma_s[walker]
            c = last_c_s[walker]
            y_fitted = normal_dist(x = x0, mu = mu, sigma= sigma, c = c) * np.std(fluxes_windows[filename]) + np.mean(fluxes_windows[filename])
            if 'Fitted' not in labels_added:
                plt.plot(x1, y_fitted, color = 'green', linewidth = 0.1, label = 'Fitted')
                labels_added.append("Fitted")
            else:
                plt.plot(x1, y_fitted, color = 'green', linewidth = 2)
        plt.xlabel('x', fontsize = 20)
        plt.ylabel(r'y', fontsize = 20)
        plt.yticks([])
        plt.legend(fontsize = 10)
        plt.show()
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'fit_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()

    return real_mu_s_s, real_sigma_s_s, real_c_s_s
    
real_mu_s_s, real_sigma_s_s, real_c_s_s = plot(sampless, samplers)

velocity_s = []
velocity_std_s = []

for filename in filenames:
    c_light = 3.0E5
    velocity = np.median(((real_mu_s_s[filename])-true_wavelength)/true_wavelength * c_light)
    velocity_std = np.std(((real_mu_s_s[filename])-true_wavelength)/true_wavelength * c_light)
    velocity_s.append(velocity)
    velocity_std_s.append(velocity_std)
    out = open('Results/Spectrum_'+ filename[:filename.index('.txt')] +'/Results_' + filename[:filename.index('.txt')] + '.txt', 'w')
    out.write('Real mean is at ' + str(np.median(real_mu_s_s[filename])) + '\n' + 'Velocity is '+ str(velocity) + ' km/s' + '\n' + 'Results of walkers:'+'\n'+ "Real mu's: " + str(real_mu_s_s[filename]) +'\n' + "Real sigma's: " + str(real_sigma_s_s[filename]) )
    
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

