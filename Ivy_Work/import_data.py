#enter filename, rest wavelength
from support_functions import *
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.rcParams['interactive'] == True

def user_input():
    lowerbound = float(input("lowerbound: "))
    upperbound = float(input("upperbound: "))
    return lowerbound, upperbound
    
def import_data (filenames, x1, x2, Q_V = 'Q'):
    wavelengths_windows = {}
    fluxes_windows = {}
    wavelengths_normalizeds = {}
    fluxes_normalizeds = {}
    for filename in filenames:
        data_loaded = np.loadtxt('data/' + filename)
        wavelengths = data_loaded[:,0]
        fluxes = data_loaded[:,1]
        
        if not os.path.isdir('Results'):
            os.mkdir('Results')
        if not os.path.isdir('Results/Spectrum_'+filename[:filename.index('.txt')]):
            os.mkdir('Results/Spectrum_'+filename[:filename.index('.txt')])
        
        
        colors = get_colors(3, 'chill')
        plt = get_pretty_plot()
        idx = np.where ((wavelengths > x1) & (wavelengths < x2))
        plt.plot(wavelengths, fluxes, "b-", linewidth = 3, color = colors[0], alpha = 0.4)
        plt.plot(wavelengths[idx], fluxes[idx], "b-", linewidth = 5, color = colors[0], alpha = 1.0)
        plt.xlabel(r'Wavelength ($\AA$)', fontsize = 30)
        plt.ylabel(r"Flux", fontsize = 30)
        plt.yticks([])
        plt.title("Original Spectrum ("+filename[:filename.index('.txt')]+")", fontsize = 40, weight = 'bold', pad=20)
        plt.vlines([x1, x2], min(fluxes), max(fluxes), linewidth = 2, color = colors[1])
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] +'/ori_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        if Q_V != 'Q':
            plt.show()
        plt.close()
        

        wavelengths_window = wavelengths[idx]
        fluxes_window = fluxes[idx]
        
        plt = get_pretty_plot()
        plt.plot(wavelengths_window, fluxes_window, "b-", linewidth = 3, color = colors[0])
        plt.xlabel(r'Wavelength ($\AA$)', fontsize = 30)
        plt.ylabel("Flux", fontsize = 30)
        plt.yticks([])
        plt.title("Window ("+filename[:filename.index('.txt')]+")", fontsize = 40, weight = 'bold', pad=20)
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] + '/window_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        if Q_V != 'Q':
            plt.show()
        plt.close()
        
        if Q_V != 'Q':
            answer = input("Workig on file " +filename+ ": Do you like the window? y/n (y): ") 
            while answer.lower() == "n": 
                lowerbound, upperbound = user_input()
                idx = np.where ((wavelengths > lowerbound) & (wavelengths < upperbound))
                wavelengths_window = wavelengths[idx]
                fluxes_window = fluxes[idx]
                plt.plot(wavelengths_window, fluxes_window, "b-")
                plt.xlabel("Wavelengths (Angstrom)")
                plt.ylabel("Flux ")
                plt.show()
                answer = input("Workig on file " +filename+ ": Do you like the new window? y/n (y): ")

        wavelengths_normalized = (wavelengths_window - np.mean(wavelengths_window))/np.std(wavelengths_window)
        fluxes_normalized = (fluxes_window- np.mean(fluxes_window))/np.std(fluxes_window)
        wavelengths_windows[filename] = wavelengths_window
        fluxes_windows[filename] = fluxes_window
        wavelengths_normalizeds[filename] = wavelengths_normalized
        fluxes_normalizeds[filename] = fluxes_normalized  
            
    return wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds


