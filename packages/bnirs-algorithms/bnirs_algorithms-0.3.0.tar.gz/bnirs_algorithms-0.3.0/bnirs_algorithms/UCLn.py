from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pkg_resources

class UCLn:

    def __init__(self, sds) -> None:

        path = pkg_resources.resource_filename('bnirs_algorithms', 'values.csv')
        df = pd.read_csv(path, index_col="wavelength", skiprows=[1])

        self.ext_coeffs = df.loc[780:901][["hbo2_extinction", "hhb_extinction", "cco_extinction"]]
        print(self.ext_coeffs)
        self.ext_coeffs = self.ext_coeffs.values
        self.water_extinction = df.loc[780:901][["h2o_absorption"]].values.reshape(-1)
        self.ext_coeffs_inv = np.linalg.pinv(self.ext_coeffs)

        self.wavelengths = df.index.values

        self.dpf_wavelength_dependency = np.array(df.loc[780:901]["dpf_dep_780"].values)

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

    def age_dependance(self, age):
        
        assert age >= 0 and age <= 50

        self.dpf = 223.3 + 0.05624 * age ** 0.8493 - 5.723e-7 * self.wavelengths ** 3 + 0.001245 * self.wavelengths ** 2 - 0.9025 * self.wavelengths
    
    def diffusion_equation(self, WF, HHb, HbO2, a, b, ref_wavelength):
        
        mu_a = (self.ext_coeffs[:, [0, 1]] @ np.array([HbO2, HHb]) + self.water_extinction *  WF)*np.log(10)
        print(mu_a.shape)
        mu_s = b * (wavelengths/ref_wavelength) ** (-1*a)
        print(mu_s.shape)
        mu_eff = np.sqrt(3*mu_s*mu_a)
        
        self.dpf = 1/2 * mu_eff / mu_a

    def calc_conc_single(self, spectrum, spectrum_wavelengths):

        assert self.dpf is not None

        if self.first_spectrum is None:
            self.first_spectrum = spectrum
            return np.array([0, 0, 0])
        
        attenuation = np.log10(self.first_spectrum / spectrum)

        attenuation_interp = interp1d(spectrum_wavelengths, attenuation.T, kind="linear")(self.wavelengths).T

        return  (1 / (self.sds * self.dpf)) * self.ext_coeffs_inv @ attenuation_interp
    
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

    ucln.water_fitting(0.9)
    plt.plot(wavelengths, ucln.dpf)

    ucln.age_dependance(0)
    plt.plot(wavelengths, ucln.dpf)

    ucln.diffusion_equation(0.9, 0.02, 0.02, 1, 2, 1000)
    plt.plot(wavelengths, ucln.dpf)

    plt.show()
