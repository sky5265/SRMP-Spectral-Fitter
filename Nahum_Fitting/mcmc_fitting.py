

def normal_dist (x, mu, sigma, c):
  A = (1/(sigma*(2*np.pi)**0.5))
  B = -1*(x-mu)**2/(2*sigma**2)
  y = -1*A*np.exp(B)+c
  
  return y

def loss_function(inp, x, y_true):
    mu, sigma, c, err = inp
    if err < 0 or err> 0.1 or c < 0 or mu < -10 or mu > 10 or sigma > 10 or sigma < 0:
       
        return -np.inf
    

    y_fitted=normal_dist(x = x, mu=mu, sigma=sigma, c=c)
    return np.sum(-1.0*(y_true-y_fitted)**2.0)/err-np.exp(err)
    
ndim = 4
nwalkers = 20
n_iterations = 5000

mu_reasonable = 4
sigma_reasonable = 3
c_reasonable=5.56
err_reasonable=0.01


initial_guesses = []
    for walker in range(nwalkers):
    mu_guess = mu_reasonable * (1+0.1*np.random.random())
    sigma_guess = sigma_reasonable * (1+0.1*np.random.random())
    c_guess = c_reasonable * (1+0.1*np.random.random())
    err_guess = err_reasonable * (1+0.1*np.random.random())
    initial_guesses.append([mu_guess, sigma_guess,c_guess, err_guess])

sampler = emcee.EnsembleSampler(nwalkers, ndim, loss_function, kwargs = {"y_true":fluxes_window_new, "x": wavelengths_window_new})
sampler.run_mcmc(initial_guesses, n_iterations, progress = True)


samples = sampler.get_chain()

found_mu_s = samples[:, :, 0]
found_sigma_s = samples[:, :, 1]
found_c_s = samples[:, :, 2]
found_err_s = samples[:, :, 3]


last_mu_s = found_mu_s[-1,:]
last_sigma_s = found_sigma_s[-1,:]
last_c_s= found_c_s[-1,:]
last_err_s= found_err_s[-1,:]



    
mean =y_fitted [0]
print(mean)

calculated_w = mean*np.std(wavelengths_window) + np.mean(wavelengths_window)
print(calculated_w)

actual_w = 7775
c = 3.0E5

v = c * (calculated_w - actual_w)/actual_w
print("The velocity is: "+str(v)+" km/s")

def Fitting_function(wavelengths, fluxes,Rest_W, window_low, window_high)
    
    
    def extract_window(wavelengths,fluxes,window_low, window_high)
        indx=np.where ((wavelengths>window_low) & (wavelengths<window_high))
        W_new=wavelengths(idx)
        F_new=Fluxes(idx)
        return W_new, F_new
    
    def fitting(W_new, F_new, Rest_W, ndim, nwalkers, loss_function, n_iterations)
        
        sampler = emcee.EnsembleSampler(nwalkers, ndim, loss_function, kwargs = {"y_true":F_new, "x": W_new})
        smpler.run_mcmc(Rest_W, n_iterations)
    
        samples=sampler.get_chain()
        
        mu_found=samples[:,:,0]
        sigma_found=samples[:,:,1]
        
        mu=mu_found[-1,:]
        sigma=sigma_found[-1,:]
        
        return mu, sigma
    
    def velocity_function(mu, sigma,Rest_W)
        
      
        
        c = 3.0E5

        v = c * (mu - Rest_W)/Rest_W
        return v
   

   return 
    
