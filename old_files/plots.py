import numpy as np
from scipy import integrate,optimize
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.switch_backend('agg')

# Set style of plots
plt.style.use('seaborn-talk')
# Set personal color cycle
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["xkcd:blue", "xkcd:red", "xkcd:green", "xkcd:orange", "xkcd:violet", "xkcd:teal", "xkcd:brown"])

L_solar = 3.828E26 # Watts
camera_dist = 10E6*3.086E16# 10 Mpc to m
flux_to_L = 4*np.pi*np.power(camera_dist,2)/L_solar # Flux to Solar Luminosity


def SED_plot(dirc, inst_file, out_dirc ='./', img_name="SED.png", components=['total','transparent','stellar','dust_emission'], SKIRT_ver=9):
	flux_components = ['total','transparent','stellar','stellar_scattered',
						'dust_emission','dust_scattered']
	flux_labels = ['Total','Transparent','Direct Stellar','Scattered Stellar','Dust Emiss.',
					'Dust Emiss. Scattered']
	data = np.genfromtxt(dirc+inst_file)
	wavelength = data[:,0] # microns
	# SKIRT 8 & 9 have different formats for their SED data
	if SKIRT_ver == 9:
		total_flux = data[:,1]*flux_to_L # lambda*F_lambda (W/m2)
		transparent_flux = data[:,2]*flux_to_L # lambda*F_lambda (W/m2)
		direct_star_flux = data[:,3]*flux_to_L # lambda*F_lambda (W/m2)
		scattered_star_flux = data[:,4]*flux_to_L # lambda*F_lambda (W/m2)
		dust_emission_flux = data[:,5]*flux_to_L # lambda*F_lambda (W/m2)
		dust_scattered_flux = data[:,6]*flux_to_L # lambda*F_lambda (W/m2)
	else:
		total_flux = data[:,1]*flux_to_L # lambda*F_lambda (W/m2)
		direct_star_flux = data[:,2]*flux_to_L # lambda*F_lambda (W/m2)
		scattered_star_flux = data[:,3]*flux_to_L # lambda*F_lambda (W/m2)
		dust_emission_flux = data[:,4]*flux_to_L # lambda*F_lambda (W/m2)
		dust_scattered_flux = data[:,5]*flux_to_L # lambda*F_lambda (W/m2)
		transparent_flux= data[:,6]*flux_to_L # lambda*F_lambda (W/m2)

	all_fluxes = [total_flux,transparent_flux,direct_star_flux,scattered_star_flux,dust_emission_flux, dust_scattered_flux]


	for i in components:
		if i in flux_components:
			index = flux_components.index(i)
			name = flux_labels[index]
			flux = all_fluxes[index]
			plt.plot(wavelength, flux, label=name)

	plt.xscale('log')
	plt.yscale('log')
	plt.ylim([1E-4*np.power(10,np.ceil(np.log10(np.max(total_flux)))),np.power(10,np.ceil(np.log10(np.max(total_flux))))])
	plt.xlabel(r'$\lambda \, [\mu m]$')
	plt.ylabel(r'$\lambda L_{\lambda} \,[W/m^2]$')
	plt.legend()
	plt.savefig(out_dirc+img_name)
	plt.close()


def UV_continuum(x, beta):
	return np.power(x,beta)


# TO DO: FIX IRX-beta values
def calc_IRXBeta(dirc, inst_file):
	data = np.genfromtxt(dirc+inst_file)
	wavelength = data[:,0] # microns
	total_flux = data[:,1]*flux_to_L # lambda*F_lambda (W/m2)


	# F_UV is the neutral flux density at 0.15 microns
	UV_lambda = 0.15 
	idx = (np.abs(wavelength - UV_lambda)).argmin()	
	F_UV = total_flux[idx]
	# F_IR is the total dust flux integrated over 8-1000 microns
	IR_lambda = [8., 1000.]
	idx1 = (np.abs(wavelength - IR_lambda[0])).argmin()	
	idx2 = (np.abs(wavelength - IR_lambda[1])).argmin()	
	F_IR = integrate.simps(total_flux[idx1:idx2+1],wavelength[idx1:idx2+1])
	# beta_UV is rest-frame UV continuum slope from 0.15 microns and 0.23 microns
	beta_UV,_ = optimize.curve_fit(UV_continuum, wavelength, total_flux)
	beta_UV=beta_UV[0]

	print "IRX",F_IR/F_UV
	print "beta",beta_UV