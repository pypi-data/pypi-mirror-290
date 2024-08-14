from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import pkg_resources

class SRS:
    def __init__(self, sds_1, sds_2) -> None:

        path = pkg_resources.resource_filename('bnirs_algorithms', 'values.csv')
        df = pd.read_csv(path, index_col="wavelength", skiprows=[1])

        self.ext_coeffs = df[["HbO2", "HHb"]].values * 0.1
        self.ext_coeffs_inv = np.linalg.pinv(self.ext_coeffs)

        self.wavelengths = df.index.values

        self.sds_1 = sds_1
        self.sds_2 = sds_2

    def attenuation_slope(self, spectra_1, spectra_2, wavelengths_1, wavelengths_2):

        n_spectra = spectra_1.shape[0]

        slope_interp = np.zeros((n_spectra, self.wavelengths.size))

        for i in range(n_spectra):
            spectra_1_interp = interp1d(wavelengths_1, spectra_1[i, :], kind="linear")(self.wavelengths)
            spectra_2_interp = interp1d(wavelengths_2, spectra_2[i, :], kind="linear")(self.wavelengths)
            slope_interp[i, :] = np.log10(spectra_1_interp/spectra_2_interp)/(self.sds_2 - self.sds_1)

        return slope_interp
    
    def scaled_mu_a(self, attenuation_slope):
        const = 1/(3*(1 - self.wavelengths*0.00063))
        bracket = (np.log(10) * attenuation_slope - 2*np.log(self.sds_2/self.sds_1)/(self.sds_2 - self.sds_1))**2
        return const * bracket
    
    def calc_sto2(self, scaled_mu_a):
            
            result = (1 / np.log(10) * self.ext_coeffs_inv @ scaled_mu_a.T).T

            return result[:, 0]/(result[:, 0]+result[:, 1])
    
    def smooth(self, y, window):
        y = np.pad(y, (window//2, window-1-window//2), mode='edge')
        cumsum_vec = np.cumsum(np.insert(y, 0, 0)) 
        return (cumsum_vec[window:] - cumsum_vec[:-window]) / window