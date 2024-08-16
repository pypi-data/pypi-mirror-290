from enum import Enum


class RheoFields(Enum):
    TIME = "time_s"
    G = "storage_modulus_Pa"
    NFORCE = "normal_force_N"
    TAU = "shear_stress_Pa"
    GAMMA = "shear_strain_pc"
    GAMMAGOT = "strain_rate_1ps"


class CaloFields(Enum):
    TIME = "time_s"
    HEAT = "heat_J"
    HEATFLOW = "heat_flow_W"
    NORMHEAT = "norm_heat_Jpgbinder"
    NORMHEATFLOW = "norm_heat_flow_Wpgbinder"
    TEMPERATURE = "temperature_degC"
