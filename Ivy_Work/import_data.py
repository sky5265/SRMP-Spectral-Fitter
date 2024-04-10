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
            
        plt.plot(wavelengths, fluxes, "b-")
        plt.xlabel("Wavelengths (Angstrom)")
        plt.ylabel("Flux ")
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] +'/ori_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        if Q_V != 'Q':
            plt.show()
        plt.close()
        
        idx = np.where ((wavelengths > x1) & (wavelengths < x2))

        wavelengths_window = wavelengths[idx]
        fluxes_window = fluxes[idx]
        
        plt.plot(wavelengths_window, fluxes_window, "b-")
        plt.xlabel("Wavelengths (Angstrom)")
        plt.ylabel("Flux ")
        if Q_V != 'Q':
            plt.show()
        plt.savefig('Results/Spectrum_'+ filename[:filename.index('.txt')] + '/window_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
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
        fluxes_normalized = (fluxes_window- np.mean(fluxes_window)/np.std(fluxes_window))
        wavelengths_windows[filename] = wavelengths_window
        fluxes_windows[filename] = fluxes_window
        wavelengths_normalizeds[filename] = wavelengths_normalized
        fluxes_normalizeds[filename] = fluxes_normalized  
            
    return wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds


