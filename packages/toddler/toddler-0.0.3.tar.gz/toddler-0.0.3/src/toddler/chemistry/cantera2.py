from typing import Any
import cantera as ct
import numpy as np
import numpy.typing as npt


def get_solution(*gases):
    return ct.Solution("gri30.yaml")[gases]


def calculate_parameters(
    solution: ct.Solution, composition: dict[str, float], pressure_mbar, Tmap, **kwargs
) -> tuple[npt.NDArray[Any], ...]:
    solution.TPX = 3000, pressure_mbar * 100, {"H2": 1}

    param_list = [np.zeros(np.shape(Tmap)) for i in range(len(kwargs))]

    for index, T in np.ndenumerate(Tmap):
        composition_i = composition.copy()
        if any([type(v) == np.ndarray for v in composition.values()]):
            composition_i = {
                k: v[index] if type(v) == np.ndarray else v
                for k, v in composition.items()
            }
        solution.TPX = T, pressure_mbar * 100, composition_i

        for k, (key, valuefun) in enumerate(kwargs.items()):
            param_list[k][index] = valuefun(solution)

    return tuple(param_list)


def calculate_parameters_dict(pressure_mbar, Tmap, **kwargs) -> dict[str, np.ndarray]:
    param_list = calculate_parameters(pressure_mbar, Tmap, **kwargs)
    return dict(zip(kwargs.keys(), param_list))


def get_enthalpy_density(pressure_mbar, Tmap):
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        enthalpy=lambda major: major.enthalpy_mole * major.density_mole,
    )[0]


def get_specific_enthalpy(pressure_mbar, Tmap):
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        enthalpy=lambda major: major.enthalpy_mass,
    )[0]


def get_molar_enthalpy(pressure_mbar, Tmap):
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        enthalpy=lambda major: major.enthalpy_mole,
    )[0]


def get_net_production_rate(pressure_mbar, Tmap):
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        netprod=lambda major: -major.net_production_rates[major.species_index("H2")],
    )[0]


def get_rhocp(pressure_mbar, Tmap):
    # [J/K/m^3]
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        rhocp=lambda major: major.cp_mass * major.density_mass,
    )[0]


def get_heatrelease(pressure_mbar, Tmap):
    # [W/m^3]
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        heatrelease=lambda major: np.sum(major.heat_production_rates),
    )[0]


def get_thermalconductivity(pressure_mbar, Tmap):
    # [W/m/K]
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        thermalcond=lambda major: major.thermal_conductivity,
    )[0]


def prandtl(pressure_mbar, Tmap):
    return calculate_parameters(
        pressure_mbar,
        Tmap,
        prandtl=lambda major: major.cp_mass
        * major.viscosity
        / major.thermal_conductivity,
    )[0]


# map_thermalcond[i, j] = major.thermal_conductivity
# map_heatrelease[i, j] = np.sum(major.heat_production_rates)
# map_rhocp[i, j] = major.cp_mass * major.density_mass
# map_netprod[i, j] = -major.net_production_rates[major.species_index("H2")]
# # map_heatrelease[i,j] = major.heat_release_rate
# # Nhmap[i,j] = major.concentrations[major.species_index('H')] # major.density_mole * Nmap[i,j] #
# # Gmap[i,j] = major.enthalpy_mole / Tmap[i,j] #- Gref / 300
# map_massdiff[i, j] = major.binary_diff_coeffs[
#     major.species_index("H2"), major.species_index("H")
# ]
# # Rmap[i,j] = major.net_production_rates[major.species_index('H')]
# # Hmap[i,j] = major.heat_release_rate
# # Vmap[i,j] = major.viscosity

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import wedme

    wedme.dev()

    Tmap = np.linspace(300, 3000, 1000)
    for pressure in [100, 300, 500, 700, 1000]:
        val = prandtl(pressure, Tmap)
        plt.plot(Tmap, val, label=f"{pressure} mbar")
    plt.legend()
    # plt.ylim(0.5, 1.0)
    plt.xlabel("Temperature [K]")
    plt.ylabel("Prandtl number [-]")
    plt.show()
