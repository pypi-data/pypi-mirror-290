from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import pkg_resources

class SRS:
    def __init__(self, sds_1, sds_2, detectors_close=True) -> None:

        path = pkg_resources.resource_filename('bnirs_algorithms', 'values.csv')
        df = pd.read_csv(path, index_col="wavelength", skiprows=[1])

        self.ext_coeffs = df.loc[780:900][["hbo2_extinction", "hhb_extinction"]].values
        self.ext_coeffs_inv = np.linalg.pinv(self.ext_coeffs)

        self.wavelengths = df.loc[780:900].index.values

        self.sds_1 = sds_1
        self.sds_2 = sds_2
        self.detectors_close = detectors_close

    def _attenuation_slope(self, spectra_1, spectra_2, wavelengths_1, wavelengths_2):

        assert spectra_1.shape == spectra_2.shape

        slope_interp = np.zeros((spectra_1.shape[0], self.wavelengths.size))

        for i in range(spectra_1.shape[0]):
            spectra_1_interp = interp1d(wavelengths_1, spectra_1[i, :], kind="cubic")(self.wavelengths)
            spectra_2_interp = interp1d(wavelengths_2, spectra_2[i, :], kind="cubic")(self.wavelengths)
            slope_interp[i, :] = np.log10(spectra_1_interp/spectra_2_interp)/(self.sds_2 - self.sds_1)

        return slope_interp
    
    def _scaled_mu_a(self, attenuation_slope):
        const = 1/(3*(1 - self.wavelengths*0.00063))
        if self.detectors_close:
            bracket = (np.log(10) * attenuation_slope - 2/self.sds_2)**2
        else:
            bracket = (np.log(10) * attenuation_slope - 2*np.log(self.sds_2/self.sds_1)/(self.sds_2 - self.sds_1))**2
        return const * bracket
    
    def calc_sto2(self, spectra_1, spectra_2, wavelengths_1, wavelengths_2):
            
            attenuation_slope = self._attenuation_slope(spectra_1, spectra_2, wavelengths_1, wavelengths_2)

            scaled_mu_a = self._scaled_mu_a(attenuation_slope)

            result = (1 / np.log(10) * self.ext_coeffs_inv @ scaled_mu_a.T).T

            return result[:, 0]/(result[:, 0]+result[:, 1])