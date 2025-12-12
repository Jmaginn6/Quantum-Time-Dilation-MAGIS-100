# ---------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------

from dataclasses import dataclass

# ---------------------------------------------------------------
# Simulation Settings
# ---------------------------------------------------------------

@dataclass
class SimulationSettings:
    # Overall simulation settings
    # Setting all settings to none so we set them in Main.ipynb for each run
    # Ensures that we know exactly what we are inputting everytime
    hours: float | None = None # total simulation time in hours
    frep: float | None = None # frequency of shots in HZ
    start_hr: float | None = None # starting hours of the day (0.0 to 24.0)

    # Sensor settings
    sensor_dt: float | None = None # sensor data time interva; in seconds (how often it updates)
    N_sensors: int | None = None # how many sensors in the simulaiton
    random_noise: float | None = None # random fluctuations in sensor data (std dev)
    sensor_resolution: float | None = None # sensor resolution (quantization level)
    sensor_accuracy: float | None = None # constant offset error in sensor data (drift per time frame)

    # To ensure that we have them set for each run:
    def validate(self):
        # find the missing variables
        missing = [
            name for name, value in vars(self).items()
            if value is None
        ]
        if missing:
            raise ValueError(
                f"SimulationSettings is missing values for: {missing}"
            )
#settings = SimulationSettings()





    
