#plot data from fitting
from support_functions import *
from import_data import filenames, wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds, true_wavelength
from import_data import *
from fitting import sampless, samplers

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
        plt.savefig('Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'Normalized_fit_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()
      
        flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
        labels = ['mu', 'sigma', 'c', 'err']
        fig = corner.corner(flat_samples, labels=labels);
        plt.savefig('Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'Normalized_corner_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()

        real_mu_s_s[filename] = last_mu_s * np.std(wavelengths_windows[filename]) + np.mean(wavelengths_windows[filename])
        real_sigma_s_s[filename] = last_sigma_s * np.std(wavelengths_windows[filename]) 
        real_c_s_s[filename] = last_c_s* np.max(fluxes_windows[filename])
        
        x1 = np.linspace(lowerbound,upperbound,500)
        plt.scatter(wavelengths_windows[filename], fluxes_normalizeds[filename], color = "red", linewidth = 0.5, label = filename)
        labels_added = []
        for walker in range(len(last_mu_s)):
            mu = np.mean(real_mu_s_s[filename])
            sigma = np.mean(real_sigma_s_s[filename])
            c = last_c_s[walker]
            y_fitted = normal_dist(x = x1, mu = mu, sigma= sigma, c = c)
            if 'Fitted' not in labels_added:
                plt.plot(x1, y_fitted, color = 'green', linewidth = 0.1, label = 'Fitted')
                labels_added.append("Fitted")
            else:
                plt.plot(x1, y_fitted, color = 'green', linewidth = 2)
            print(c)
        plt.xlabel('x', fontsize = 20)
        plt.ylabel(r'y', fontsize = 20)
        plt.legend(fontsize = 10)
        plt.show()
        plt.savefig('Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'fit_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()
        print(y_fitted)

    return real_mu_s_s, real_sigma_s_s, real_c_s_s
    
real_mu_s_s, real_sigma_s_s, real_c_s_s = plot(sampless, samplers)

print(real_mu_s_s)
print(real_sigma_s_s)

for filename in filenames:
    c_light = 3.0E5
    velocity = (np.mean(real_mu_s_s[filename])-true_wavelength)/true_wavelength * c_light
    out = open('Spectrum_'+ filename[:filename.index('.txt')] +'/Results_' + filename[:filename.index('.txt')] + '.txt', 'w')
    out.write('Real mean is at ' + str(np.mean(real_mu_s_s[filename])) + '\n' + 'Velocity is '+ str(velocity) + ' km/s')
