# ---------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------

from dataclasses import dataclass
import numpy as np
from scipy import constants as const

# ---------------------------------------------------------------
# MODEL PARAMETERS
# ---------------------------------------------------------------

@dataclass
class ModelParams:

    # Geometry
    z_min: float = 0.0
    z_max: float = 100.0 
    L_shaft: float = z_max - z_min    
    # Interrogation Time (2T = 2s)  
    T: float = 1.0  
    # Gravitational acceleration
    g: float = 9.80665

    # Laser wavevector (Sr clock)
    WaveVector: float = (2*np.pi)/(698e-9)

    # Cloud positions & velocities
    # A at top of shaft height = 100m, velocity = -20ms-1 down
    A_z0: float = 100.0
    A_v0: float = -20.0
    # B at bottom of shaft height = 0m, velocity = 40ms-1 down
    B_z0: float = 0.0
    B_v0: float = +40.0

    # Constants
    h_bar: float = const.h/(2*np.pi)
    c: float = const.c
    w0: float = 2*np.pi*4.29228e14  # clock freq


#params = ModelParams()
#print("Model Parameters Initialised!")
