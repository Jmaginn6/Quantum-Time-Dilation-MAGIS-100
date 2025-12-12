import numpy as np

class TemperatureField:
    def __init__(
        self,
        L: float = 100.0,  # m

        # Surface temperature parameters
        T_surface_mean_C: float = 14.0,
        T_surface_amp_C: float = 2.5,
        Surface_phase_shift: float = 15.0,  # hours

        # Bottom temperature parameters
        T_bottom_mean_C: float = 20.2,
        T_bottom_amp_C: float = 1.0,
        Bottom_phase_shift: float = 15.0,  # hours

        # Vertical profile shaping
        gamma: float = 1.0,   # >1 biases toward bottom, <1 toward top
        T_mid_amp_C: float = 0.0,
        Mid_phase_shift: float = 15.0,  # hours
    ):
        # Geometry
        self.L = L

        # Surface parameters (store internally in Kelvin)
        self.T_surface_mean_C = T_surface_mean_C + 273.15
        self.T_surface_amp_C = T_surface_amp_C
        self.surface_phase = Surface_phase_shift

        # Bottom parameters (store internally in Kelvin)
        self.T_bottom_mean_C = T_bottom_mean_C + 273.15
        self.T_bottom_amp_C = T_bottom_amp_C
        self.bottom_phase = Bottom_phase_shift

        # Vertical shaping
        self.gamma = gamma
        self.A_local = T_mid_amp_C
        self.local_phase = Mid_phase_shift
    

    # Top temperature:
    def surface_temperature(self, t_hours):
          """Temperature at the surface of the shaft as a function of time"""
          t = np.asarray(t_hours) # np.asarray - Convert input to array if it is not already
          return (self.T_surface_mean_C + self.T_surface_amp_C * np.sin(2 * np.pi * (t - self.surface_phase)/24 ))
    

    # Bottom temperature:
    def bottom_temperature(self, t_hours):
          """Temperature at the bottom of the shaft as a function of time"""
          t = np.asarray(t_hours)
          return (self.T_bottom_mean_C + self.T_bottom_amp_C * np.sin(2 * np.pi * (t - self.bottom_phase)/24 ))
    

    # Local temperature at depth z:
    def temperature(self, t_hours, z):
            """Temperature at depth z in the shaft as a function of time
            Notes: In order to recpver a purely linear gradient we must set the gamma = 1 and Amplitude = 0"""
            t = np.asarray(t_hours)
            z = np.asarray(z)
            
            # Boundary temperatures
            T_top = self.surface_temperature(t)
            T_bot = self.bottom_temperature(t)

            # Normalised height
            s = z/self.L

            # Vertical blending
            alpha = s ** self.gamma
            # Temperature weights
            T_base = (1.0 - alpha) * T_bot + (alpha * T_top)

            # Mid amplitude and phase with boundary consitions
            shape = s * (1 - s) # so at z=0 and z=L, shape = 0
            delta = (self.A_local * shape * np.sin(2 * np.pi * (t - self.local_phase)/24))
            return T_base + delta

