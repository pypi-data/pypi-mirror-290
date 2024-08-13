from toddler.physics.const import h, c, k
import numpy as np


# Black body spectrum
def blackbody(wavelength, T):
    return 2 * h * c**2 / wavelength**5 / (np.exp(h * c / (wavelength * k * T)) - 1)
