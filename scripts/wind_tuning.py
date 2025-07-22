# wind_tuning.py
import numpy as np

def tune_wind(controller):
    for zone in controller.wind_zones.values():
        zone.set_wind_speed(10.0)
        zone.set_wind_direction([1, 0, 0])
        zone.set_turbulence_intensity(0.5)
        zone.set_wind_gusts(0.3, 4.0, 1.5)
        zone.noise_scale = 0.07
        zone.noise_amplitude = 2.5
        zone.noise_time_speed = 0.12
        zone.updraft_center = np.array([5, 0, 5])
        zone.updraft_radius = 8.0
        zone.updraft_strength = 2.5
        zone.shear_y = 12.0
        zone.shear_thickness = 3.0
        zone.shear_vector = np.array([2.0, 0, 1.0])
        # Tornado!
        zone.tornado_enabled = True
        zone.tornado_center = np.array([10, 0, 10])  # Place tornado at (10, 0, 10)
        zone.tornado_radius = 8.0
        zone.tornado_strength = 40.0
        zone.tornado_updraft = 20.0
        zone.dryden_sigma = 2.0      # turbulence intensity (m/s)
        zone.dryden_L = 200.0        # turbulence scale (m)
        zone.dryden_V = 10.0         # mean wind speed (m/s)
        zone.gustfront_enabled = True
        zone.gustfront_center = np.array([20, 5, 20])
        zone.gustfront_radius = 12.0
        zone.gustfront_strength = 18.0
        zone.gustfront_duration = 2.0
        zone.microburst_enabled = True
        zone.microburst_center = np.array([10, 5, 10])
        zone.microburst_radius = 8.0
        zone.microburst_strength = 25.0
        zone.microburst_duration = 1.5
