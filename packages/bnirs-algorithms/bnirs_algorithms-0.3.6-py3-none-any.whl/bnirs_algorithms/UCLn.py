from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pkg_resources

class UCLn:

    def __init__(self, sds) -> None:

        path = pkg_resources.resource_filename('bnirs_algorithms', 'values.csv')
        df = pd.read_csv(path, index_col="wavelength", skiprows=[1])

        self.ext_coeffs = df.loc[780:900][["hbo2_extinction", "hhb_extinction", "cco_extinction"]].values

        self.water_absorption = df.loc[780:900][["h2o_absorption"]].values.reshape(-1)
        self.ext_coeffs_inv = np.linalg.pinv(self.ext_coeffs)

        self.wavelengths = df.loc[780:900].index.values

        self.dpf_wavelength_dependency = np.array(df.loc[780:900]["dpf_dep_780"].values)

        self.dpf = None
        self.first_spectrum = None

        self.sds = sds

    def constant_dpf(self, type):

        dpf_types = {
        "baby_head": 4.99,
        "adult_head": 6.26,
        "adult_arm": 4.16,
        "adult_leg": 5.51,
        }

        assert type in dpf_types

        wl_dep = self.dpf_wavelength_dependency / self.dpf_wavelength_dependency[np.where(self.wavelengths == 807)[0]]

        self.dpf = dpf_types[type] * wl_dep
    
    def water_fitting(self, WF):

        wl_dep = self.dpf_wavelength_dependency / self.dpf_wavelength_dependency[np.where(self.wavelengths == 830)[0]]

        self.dpf = 10 * WF / ( 0.85* self.sds) * wl_dep
    
    def diffusion_equation(self, WF, HHb, HbO2, a, b, ref_wavelength):
        
        mu_a = np.log(10)*self.ext_coeffs[:, [0, 1]] @ np.array([HbO2, HHb]) + self.water_absorption *  WF

        mu_s = b * (wavelengths/ref_wavelength) ** -a
        
        self.dpf = 1/2 * np.sqrt(3*mu_s/mu_a)

    def calc_conc_single(self, spectrum, spectrum_wavelengths):

        assert self.dpf is not None

        if self.first_spectrum is None:
            self.first_spectrum = spectrum
            return np.array([0, 0, 0])
        
        attenuation = np.log10(self.first_spectrum / spectrum)

        attenuation_interp = interp1d(spectrum_wavelengths, attenuation.T, kind="cubic")(self.wavelengths).T

        return self.ext_coeffs_inv @ np.divide(attenuation_interp, self.dpf*self.sds)
    
    def calc_concs(self, spectra, spectra_wavelengths):

        result = np.zeros((spectra.shape[0], 3))

        for idx, spectrum in enumerate(spectra):
            result[idx, :] = self.calc_conc_single(spectrum, spectra_wavelengths)
        
        return result

if __name__ == "__main__":

    ucln = UCLn(sds=3)

    wavelengths = ucln.wavelengths

    ucln.constant_dpf("baby_head")
    plt.plot(wavelengths, ucln.dpf)

    ucln.water_fitting(0.95)
    plt.plot(wavelengths, ucln.dpf)

    ucln.diffusion_equation(0.7, 0.04, 0.02, 1, 2, 1000)
    plt.plot(wavelengths, ucln.dpf)

    plt.show()
