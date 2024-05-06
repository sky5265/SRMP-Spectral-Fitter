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

        
def plot_and_denormalize (mu_s, sigma_s, c_s, err_s, filenames, wavelengths_normalizeds, fluxes_normalizeds, wavelengths_windows, fluxes_windows, lowerbound, upperbound, Q_V = 'Q'):

    real_mu_s_s = {}
    real_sigma_s_s = {}
    real_c_s_s ={}
    
    for filename in filenames:

        last_mu_s = mu_s[filename][-1,:]
        last_sigma_s = sigma_s[filename][-1]
        last_c_s = c_s[filename][-1]
        last_err_s = err_s[filename][-1]

        plt = get_pretty_plot()
        x0 = np.linspace(-1.5,1.5,500)
        plt.plot(wavelengths_normalizeds[filename], fluxes_normalizeds[filename], color = sKy_colors['light blue'],  label = filename)
        plt.yticks([])
        plt.title('Normalized fit of '+ filename[:filename.index('.txt')], fontsize = 35, weight = 'bold', pad=20)
        labels_added = []
        for walker in range(len(last_mu_s)):
            mu = last_mu_s[walker]
            sigma = last_sigma_s[walker]
            c = last_c_s[walker]
            y_fitted = normal_dist(x = x0, mu = mu, sigma= sigma, c = c)
            if 'Fitted' not in labels_added:
                plt.plot(x0, y_fitted, color = sKy_colors['dark mute red'], linewidth = 0.1, label = 'Fitted')
                labels_added.append("Fitted")
            else:
                plt.plot(x0, y_fitted, color = sKy_colors['dark mute red'], linewidth = 2)
        plt.legend(fontsize = 15)
        if Q_V.upper() != 'Q':
            plt.show()
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'Normalized_fit_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()
      
        real_mu_s_s[filename] = last_mu_s * np.std(wavelengths_windows[filename]) + np.mean(wavelengths_windows[filename])
        real_sigma_s_s[filename] = last_sigma_s * np.std(wavelengths_windows[filename]) 
        real_c_s_s[filename] = last_c_s* np.std(fluxes_windows[filename]) + np.mean(fluxes_windows[filename])
        
        plt = get_pretty_plot()
        x1 = np.linspace(lowerbound,upperbound,500)
        plt.plot(wavelengths_windows[filename], fluxes_windows[filename], color = sKy_colors['light blue'], label = filename, )
        plt.yticks([])
        plt.title('Denormalized fit '+ filename[:filename.index('.txt')], fontsize = 35, weight = 'bold', pad=20)
        labels_added = []
        for walker in range(len(last_mu_s)):
            mu = last_mu_s[walker]
            sigma = last_sigma_s[walker]
            c = last_c_s[walker]
            y_fitted = normal_dist(x = x0, mu = mu, sigma= sigma, c = c) * np.std(fluxes_windows[filename]) + np.mean(fluxes_windows[filename])
            if 'Fitted' not in labels_added:
                plt.plot(x1, y_fitted, color = sKy_colors['dark mute red'], linewidth = 0.1, label = 'Fitted')
                labels_added.append("Fitted")
            else:
                plt.plot(x1, y_fitted, color = sKy_colors['dark mute red'], linewidth = 2)
        plt.xlabel(r'Wavelength ($\AA$)', fontsize = 20)
        plt.ylabel('Flux', fontsize = 20)
        plt.yticks([])
        plt.legend(fontsize = 15)
        if Q_V.upper() != 'Q':
            plt.show()
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] + '/' + 'fit_'+ filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()

    return real_mu_s_s, real_sigma_s_s, real_c_s_s

def write_velocities(filenames, true_wavelength, real_mu_s_s, real_sigma_s_s, Q_V = 'Q'):

    velocity_s = []
    velocity_std_s = []

    for filename in filenames:
        c_light = 3.0E5
        real_velocities = (real_mu_s_s[filename]-true_wavelength)/true_wavelength * c_light
        
        velocity = np.median(real_velocities)
        velocity_std = np.std(real_velocities) 

        velocity_s.append(velocity)
        velocity_std_s.append(velocity_std)
        out = open('Results/Spectrum_'+ filename[:filename.index('.txt')] +'/Results_' + filename[:filename.index('.txt')] + '.txt', 'w')
        out.write('Rest frame mean is at ' + str(np.median(real_mu_s_s[filename])) + '\nVelocity is '+ str(velocity) + ' km/s' + '\n' + 
        'Results of walkers:'+'\n'+ "Real mu's: " + str(real_mu_s_s[filename]) +'\n' + "Median of real mu's: " + str(np.median(real_mu_s_s[filename])) + "\nStandard deviation of mu's: " + str(np.std(real_mu_s_s[filename])) + '\n\n'
        "Real sigma's: " + str(real_sigma_s_s[filename]) + "\nMedian of real sigma's: " + str(np.median(real_sigma_s_s[filename])) + "\nStandard deviation of sigma's: " + str(np.std(real_sigma_s_s[filename])))
        
    filename = []
    for file in filenames:
        file = file[:file.index('.txt')]
        filename.append(file)
        
    colors = get_colors(2, 'chill')
    plt = get_pretty_plot()
    plt.title('Velocity of '+ str(true_wavelength) + '$\AA$ absorbtion line over time' , fontsize = 35, weight = 'bold', pad=30)
    plt.scatter([float(i) for i in filename], velocity_s, color = colors[0])
    plt.errorbar([float(i) for i in filename], velocity_s, velocity_std_s, ls='none')
    plt.xlabel("Time", fontsize = 25)
    plt.ylabel("Velocity (km/s)", fontsize = 25)
    if Q_V.upper() != 'Q':
            plt.show()
    plt.savefig('Results' + '/Velocity_Over_Time' + '.pdf', bbox_inches='tight')
    plt.close()
  
