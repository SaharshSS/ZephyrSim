# wind_tuning.py
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
