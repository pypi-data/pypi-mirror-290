# bNIRS Algorithms

`bnirs_algorithms` is a Python package that provides implementations of several broadband near-infrared spectroscopy (bNIRS) algorithms.

## Features

- **UCLn**: An algorithm which calculates concentration changes of oxy/deoxyhaemoglobin and cytochrome-c-oxidase.
- **SRS**: An algorithm which makes use of measurements at multiple source-detector distances to calculate the absolute tissue oxygen saturation.

## Installation

You can install the `bnirs_algorithms` package directly from PyPI using:

```bash
pip install bnirs-algorithms
```

## Usage

Here are quick examples of how to use each of the algorithms:

1) **UCLn**

```python
from bnirs_algorithms.UCLn import UCLn

ucln = UCLn(sds=3)

ucln.constant_dpf("baby_head")

conc_changes = ucln.calc_concs(spectra, wavelengths)
```

2) **SRS**

```python
from bnirs_algorithms.SRS import SRS

srs = SRS(sds_1=2, sds_2=3, detectors_close=False)

sto2 = srs.calc_sto2(spectra_1, spectra_2, wavelengths_1, wavelengths_2)
```


