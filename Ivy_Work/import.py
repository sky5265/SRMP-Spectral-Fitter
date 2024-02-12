#enter filename, rest wavelength
from support_functions import *
import matplotlib


filename = 'data/59793.29.txt'
wavelengths, fluxes = import_data(filename)
true_wavelength = 7775
lowerbound = 7500
upperbound = 7860
wavelengths_window, fluxes_window, wavelengths_normalized, fluxes_normalized = window_range(wavelengths, fluxes, lowerbound, upperbound)