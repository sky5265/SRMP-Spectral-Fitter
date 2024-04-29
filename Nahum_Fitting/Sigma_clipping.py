import math
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt




data = np.loadtxt("../Ivy_Work/data/59788.25.txt")


wavelengths = data[:,0]
fluxes = data[:,1]

Rest_W=7775
window_low=7400
window_high=7900



def extract_window(wavelengths,fluxes,window_low, window_high):
    idx=np.where ((wavelengths>window_low) & (wavelengths<window_high))
    wavelengths_window=wavelengths[idx]
    fluxes_window=fluxes[idx]
    return wavelengths_window, fluxes_window



wavelengths_window, fluxes_window = (extract_window(wavelengths,fluxes,window_low, window_high))
print("wavelengths_window: "+str(wavelengths_window))
print("fluxes_window: "+str(fluxes_window))




    
    


y_smoothed=savgol_filter(fluxes_window, 30, 2)
print("y_smoothed: "+str(y_smoothed))
sig=np.std(y_smoothed - fluxes_window)
print("average diff: "+str(np.mean(y_smoothed - fluxes_window)) + " std: "+str(np.std(y_smoothed - fluxes_window)))
print("sig: "+str(sig))

n=3

w_to_keep = []
f_to_keep = []
for i in range(len(fluxes_window)):
    orig_flux = fluxes_window[i]
    smooth_y = y_smoothed[i]
    diff = abs(orig_flux - smooth_y)
    
    if diff < n*sig:
        w_to_keep.append(wavelengths_window[i])
        f_to_keep.append(fluxes_window[i])


    


plt.plot(wavelengths_window, fluxes_window, label = 'Raw Data', alpha = 0.6, linewidth = 3)
plt.plot(wavelengths_window, y_smoothed, label = 'Smoothed', alpha = 0.6, linewidth = 3)
plt.scatter(w_to_keep, f_to_keep, label = 'Sigma Clipped Y', alpha = 0.6)
plt.legend()
plt.show()