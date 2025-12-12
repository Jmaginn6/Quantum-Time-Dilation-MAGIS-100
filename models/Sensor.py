import numpy as np

class Sensor:
    def __init__(
            self,
            *,  # Interesting line - This forces all following parameters to be named arguments
            L: float,
            settings,
            seed:int
    ):

        # Basic geometry
        self.N_sensors = settings.N_sensors
        self.L = L

        # Evenly spaced sensors along the shaft
        self.z_sensors = np.linspace(0, L, self.N_sensors)

        # Timing of sensors readings
        self.sensor_dt = settings.sensor_dt  # seconds


        # Per-sensor rngs
        self._rngs = [
            np.random.default_rng((seed, k)) for k in range(self.N_sensors)
        ] #_ naming convention: Means dont touch this from the outside

        # Per sensor offsets
        sigma_acc = settings.sensor_accuracy

        # Sensor resolution
        self.sensor_resolution = settings.sensor_resolution

        # sensor random noise
        self.random_noise = settings.random_noise

        if sigma_acc is None or sigma_acc == 0:
            self.offsets = np.zeros(self.N_sensors)      # if there is no accuracy set then we get an array of zeros

        else:
            self.offsets = np.array([
                rng.uniform(-sigma_acc, + sigma_acc)
                for rng in self._rngs
            ])

    def measure(self, field, t_eval):
        """Measures what a temperature sensor would read the true field as. 
        Adds sensor offsets, quantised reading times and sensor resolution, random noise for each reading"""
        t_eval = np.asarray(t_eval)
        Nt = len(t_eval)

        # true temperatures at evaluation times
        T_true = np.zeros((self.N_sensors, Nt))
        for k, z in enumerate(self.z_sensors):
            T_true[k] = field.temperature(t_eval, z)

        # Sensor read times
        t_start_s = t_eval[0] * 3600.0
        t_end_s = t_eval[-1] * 3600.0

        t_sensor_s = np.arange(
            t_start_s,
            t_end_s + self.sensor_dt,
            self.sensor_dt
        )
        t_sensor = t_sensor_s / 3600.0  # convert to hours

        Ns = len(t_sensor)

        # ------------------------------------------------------------
        # Measured temperatures at sensor read times
        # ------------------------------------------------------------
        T_sensor = np.zeros((self.N_sensors, Ns))

        for k, (z, rng) in enumerate(zip(self.z_sensors, self._rngs)):
            # True temperature at sensor read times
            T_k = field.temperature(t_sensor, z)

            # Add constant offset
            T_k = T_k + self.offsets[k]

            # Add random noise (per read)
            if self.random_noise is not None and self.random_noise > 0.0:
                noise = rng.normal(
                    loc=0.0,
                    scale=self.random_noise,
                    size=Ns
                )
                T_k = T_k + noise

            # Quantisation (optional)
            if self.sensor_resolution is not None:
                T_k = (
                    np.round(T_k / self.sensor_resolution)
                    * self.sensor_resolution
                )

            T_sensor[k] = T_k

        # ------------------------------------------------------------
        # Zero-order hold expansion to evaluation times
        # ------------------------------------------------------------
        T_meas = np.zeros((self.N_sensors, Nt))

        for i, t in enumerate(t_eval):
            # index of most recent sensor reading
            j = np.searchsorted(t_sensor, t, side="right") - 1
            j = max(j, 0)

            T_meas[:, i] = T_sensor[:, j]

        return T_true, T_meas
                            