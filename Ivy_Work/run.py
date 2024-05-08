#run the code
from support_functions import *
from import_data import *
from tqdm import tqdm
from plot import *
sys.path.insert(1, '../Nahum_Fitting')
from mcmc_fitting import *
import warnings 
warnings.filterwarnings('ignore')

def universe(Q_V = 'Q'):

    print("please put all your data files in a folder called 'data'")

    filenames = []
    for file in os.listdir('data'):
        if file.endswith('.txt'):
            filenames.append(file)

    true_wavelength = 7775
    lowerbound = 7500
    upperbound = 7860

    #true_wavelength = float(input('what is the true wavelength?'))
    #lowerbound = float(input('what is the lowerbound?'))
    #upperbound = float(input('what is the upperbound?'))

    wavelengths_windows, fluxes_windows, wavelengths_normalizeds, fluxes_normalizeds = import_data(filenames, lowerbound, upperbound, Q_V = Q_V)

    nwalkers = 20
    if Q_V.upper() != 'Q':
        answer = input("How many walkers do you want (20) ? ")
        if is_integer(answer): 
            nwalkers = int(answer)
            answer2 = input("The current number of walkers is " + str(nwalkers) + "\nPress return to confirm: ")
            while len(answer2) > 0:
                nwalkers = int(input("How many walkers do you want (" +str(nwalkers)+ ") ? "))
                answer2 = input("The current number of walkers is " +str(nwalkers) + "\nPress return to confirm: ")


    n_iterations =5000
    if Q_V.upper() != 'Q':
        answer = input("How many interations do you want (5000) ? ")
        if is_integer(answer): 
            n_iterations = int(answer)
            answer2 = input("The current number of iterations is " + str(n_iterations) + "\nPress return to confirm: ")
            while len(answer2) > 0:
                n_iterations = int(input("How many iterations do you want (" +str(n_iterations)+ ")  ? "))
                answer2 = input("The current number of iterations is " + str(n_iterations) + "\nPress return to confirm: ")
        
    #finding fitted normalized values for fitted function
    mu_s, sigma_s, c_s, d_s, err_s = fitting(wavelengths_normalizeds, fluxes_normalizeds, nwalkers, loss_function, n_iterations, filenames, Q_V = Q_V)


    #getting fitted parameters in denormalized (physical) units, and plot fitted function over real spectrum
    real_mu_s_s, real_sigma_s_s, real_c_s_s = plot_and_denormalize(mu_s, sigma_s, c_s, d_s, err_s, filenames, wavelengths_normalizeds, fluxes_normalizeds, wavelengths_windows, fluxes_windows, lowerbound, upperbound, Q_V = Q_V)


    write_velocities(filenames, true_wavelength, real_mu_s_s, real_sigma_s_s, Q_V = Q_V)

    rerun = 'n'
    if Q_V.upper() != 'Q':
        rerun = input("Should I rerun the fit? (n)")
    return rerun


Q_V = input("Quiet or Verbose? (Q)")
if len(Q_V) == 0:
    Q_V = 'Q'

rerun = 'y'
while rerun != 'n' and len(rerun) > 0:
    rerun = universe(Q_V)





