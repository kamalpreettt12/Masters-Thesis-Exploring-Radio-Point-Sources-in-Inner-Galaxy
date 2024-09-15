import os
import numpy as np
from astropy.io import fits

# Prompt the user for input FITS files, output directories, and threshold value
fits_files = input("Enter the full paths of FITS files, separated by commas:\n").split(',')
output_spectral_map = input("Enter the full path where you want to save the spectral indices map (e.g., '/path/to/spectral_indices_map.fits'):\n")
output_errors_map = input("Enter the full path where you want to save the spectral indices errors map (e.g., '/path/to/errors_map.fits'):\n")
threshold = float(input("Enter the threshold value for blanking pixels (e.g., 0.002):\n"))

# Lists to store the flux densities and frequencies
flux_densities = []
frequencies = []

# Loop over the FITS files
for file in fits_files:
    file = file.strip()  # Remove any leading/trailing spaces
    # Open the FITS file
    hdul = fits.open(file)
    
    # Extract the data and append it to the list
    flux_densities.append(hdul[0].data)
    
    # Extract the frequency from the header and append it to the list
    frequencies.append(hdul[0].header['CRVAL3'])  # Adjust keyword if necessary

# Convert lists to 3D numpy array and process it
cube = np.squeeze(np.array(flux_densities))
frequencies = np.array(frequencies)

# Blank the pixels with negative or low flux density values (apply threshold)
cube[cube <= threshold] = np.nan

# Convert to log scale
log_frequencies = np.log10(frequencies)
log_flux_densities = np.log10(cube)

# Calculate spectral indices and errors
spectral_indices = []
spectral_errors = []

for i in range(log_flux_densities.shape[1]):
    for j in range(log_flux_densities.shape[2]):
        flux_density_values = log_flux_densities[:, i, j]
        # Linear fit (log(frequency) vs. log(flux density)) to get spectral index
        (spectral_index, _), covariance = np.polyfit(log_frequencies, flux_density_values, 1, cov=True)
        spectral_error = np.sqrt(np.diag(covariance))[0]
        
        spectral_indices.append(spectral_index)
        spectral_errors.append(spectral_error)

# Reshape indices and errors to 2D maps
spectral_indices_map = np.array(spectral_indices).reshape(cube.shape[1], cube.shape[2])
errors_map = np.array(spectral_errors).reshape(cube.shape[1], cube.shape[2])

# Write the spectral indices map to a FITS file
hdul = fits.open(fits_files[0])
header = hdul[0].header.copy()
header['NAXIS'] = 2
header['NAXIS1'] = spectral_indices_map.shape[1]
header['NAXIS2'] = spectral_indices_map.shape[0]
if 'NAXIS3' in header:
    del header['NAXIS3']

# Save spectral indices map
fits.writeto(output_spectral_map, spectral_indices_map, header, overwrite=True)
print(f"Spectral indices map saved to {output_spectral_map}")

# Save errors map
fits.writeto(output_errors_map, errors_map, header, overwrite=True)
print(f"Spectral indices errors map saved to {output_errors_map}")
