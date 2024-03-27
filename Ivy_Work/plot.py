#plot data from fitting
from support_functions import *
from import_data import *
from tqdm import tqdm
import sys
sys.path.insert(1, '../Nahum_Fitting')
from mcmc_fitting import *

def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
        
        
def plot (mu_s, sigma_s, c_s, err_s, filenames, wavelengths_normalizeds, fluxes_normalizeds, wavelengths_windows, fluxes_windows, lowerbound, upperbound):

    real_mu_s_s = {}
    real_sigma_s_s = {}
    real_c_s_s ={}
    
    for filename in filenames:

        last_mu_s = mu_s[filename][-1,:]
        last_sigma_s = sigma_s[filename][-1]
        last_c_s = c_s[filename][-1]
        last_err_s = err_s[filename][-1]

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
  
