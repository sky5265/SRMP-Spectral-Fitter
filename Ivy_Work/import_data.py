#enter filename, rest wavelength
import matplotlib.pyplot as plt
import numpy as np
import os

wavelengths_windows = {}
fluxes_windows = {}
wavelengths_normalizeds = {}
fluxes_normalizeds = {}

def import_data (filenames, x1, x2):
    for filename in filenames:
        data_loaded = np.loadtxt(input + '/' + filename)
        wavelengths = data_loaded[:,0]
        fluxes = data_loaded[:,1]
        
        if not os.path.isdir('Spectrum_'+filename[:filename.index('.txt')]):
            os.mkdir('Spectrum_'+filename[:filename.index('.txt')])
        
        plt.plot(wavelengths, fluxes, "b-")
        plt.xlabel("Wavelengths (Angstrom)")
        plt.ylabel("Flux ")
        plt.savefig('Spectrum_'+ filename[:filename.index('.txt')] +'/ori_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()
        
        idx = np.where ((wavelengths > x1) & (wavelengths < x2))

        wavelengths_window = wavelengths[idx]
        fluxes_window = fluxes[idx]

        wavelengths_normalized = (wavelengths_window - np.mean(wavelengths_window))/np.std(wavelengths_window)
        fluxes_normalized = (fluxes_window)/np.max(fluxes_window)

        wavelengths_windows[filename] = wavelengths_window
        fluxes_windows[filename] = fluxes_window
        wavelengths_normalizeds[filename] = wavelengths_normalized
        fluxes_normalizeds[filename] = fluxes_normalized

        plt.plot(wavelengths_window, fluxes_window, "b-")
        plt.xlabel("Wavelengths (Angstrom)")
        plt.ylabel("Flux ")
        plt.show()
        plt.savefig('Spectrum_'+ filename[:filename.index('.txt')] + '/window_' + filename[:filename.index('.txt')] + '.pdf', bbox_inches='tight')
        plt.close()

    return wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds

input = 'data'
filenames = []
for file in os.listdir(input):
    if file.endswith('.txt'):
        filenames.append(file)

true_wavelength = 7775
lowerbound = 7500
upperbound = 7860

wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds = import_data(filenames, lowerbound, upperbound)
