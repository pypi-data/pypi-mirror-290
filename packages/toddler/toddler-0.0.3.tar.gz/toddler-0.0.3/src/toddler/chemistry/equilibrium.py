import cantera as ct
import numpy as np

gas1 = ct.Solution("gri30.yaml")
major = gas1["H2"]

Ts = np.linspace(1000, 3000, 100)
diss_eq_mole = np.zeros(Ts.shape)
diss_eq_mass = np.zeros(Ts.shape)
diss_rate = np.zeros(Ts.shape)
test_res = np.zeros(Ts.shape)

for i, T in enumerate(Ts):
    major.TPX = T, 350e2, "H2:1"
    major.equilibrate("TP")

    diss_eq_mole[i] = 1 - major.mole_fraction_dict()["H2"]
    diss_eq_mass[i] = 1 - major.mass_fraction_dict()["H2"]
    test_res[i] = major.gibbs_mole

    reac = ct.IdealGasConstPressureReactor(major)  # create a reactor containing the gas

    sim = ct.ReactorNet([reac])  # add the reactor to a new ReactorNet simulator
    sim.advance(1e-6)

    diss_rate[i] = gas1.X[1] / 1e-6
