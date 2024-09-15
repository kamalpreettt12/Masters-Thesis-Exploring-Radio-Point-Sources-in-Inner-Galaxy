**Exploring Radio Point Sources in the Inner Galaxy**

#### Script to make Spectral Index Map

This Python script calculates the spectral index and associated errors for a set of FITS files containing image data. It processes the data by reading multiple FITS files, converting flux densities and frequencies to log scale, and performing a linear fit to calculate the spectral index at each pixel. The resulting spectral index map and error map are saved as FITS files.

#### Features:
- **Input**: User-specified FITS files containing image data and their corresponding frequency values from the headers.
- **Processing**: The script calculates the spectral index and associated errors for each pixel by performing a linear regression of log(flux density) vs. log(frequency).
- **Thresholding**: Pixels with flux densities below a user-defined threshold are blanked (set to NaN).
- **Output**: Two FITS files are created – one containing the spectral indices map and the other containing the error map.
