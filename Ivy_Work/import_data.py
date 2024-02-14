#enter filename, rest wavelength
import matplotlib.pyplot as plt
import numpy as np
import os

def import_data (filenames, x1, x2):
    for filename in filenames:
        os.mkdir('Spectrum_'+filename)
        data_loaded = np.loadtxt(input + '/' + filename)
        wavelengths = data_loaded[:,0]
        fluxes = data_loaded[:,1]
        plt.plot(wavelengths, fluxes, "b-")
        plt.xlabel("Wavelengths (Angstrom)")
        plt.ylabel("Flux ")
        plt.savefig('Spectrum_'+ filename +'/ori_' + filename + '.pdf', bbox_inches='tight')
        plt.close()
        
        idx = np.where ((wavelengths > x1) & (wavelengths < x2))

        wavelengths_window = wavelengths[idx]
        fluxes_window = fluxes[idx]

        wavelengths_normalized = (wavelengths_window - np.mean(wavelengths_window))/np.std(wavelengths_window)
        fluxes_normalized = (fluxes_window)/np.max(fluxes_window)


        plt.plot(wavelengths_window, fluxes_window, "b-")
        plt.xlabel("Wavelengths (Angstrom)")
        plt.ylabel("Flux ")
        plt.show()
        plt.savefig('Spectrum_'+ filename + '/window_' + filename + '.pdf', bbox_inches='tight')
        plt.close()

    return wavelengths_window, fluxes_window, wavelengths_normalized, fluxes_normalized

input = 'data'
filenames = []
for file in os.listdir(input):
    if file.endswith('.txt'):
        filenames.append(file)

true_wavelength = 7775
lowerbound = 7500
upperbound = 7860
wavelengths_window, fluxes_window, wavelengths_normalized, fluxes_normalized = import_data(filenames, lowerbound, upperbound)

