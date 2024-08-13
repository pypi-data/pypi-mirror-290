from toddler.physics import const as _const


def pressure_to_density(pressure_Pascal, temperature=293):
    return pressure_Pascal * _const.N_A / (_const.R * temperature)


def pressure_to_molar_density(pressure_Pascal, temperature=293):
    return pressure_Pascal / (_const.R * temperature)
