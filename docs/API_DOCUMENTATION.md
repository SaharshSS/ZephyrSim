# ZephyrSim API Documentation

**Version:** 0.1.8  
**Project:** ZephyrSim - Drone Simulation Environment  
**Repository:** [ZephyrSim](https://github.com/SaharshSS/ZephyrSim)

---

## Table of Contents

1. [Overview](#overview)
2. [Core Components](#core-components)
3. [DroneController API](#dronecontroller-api)
4. [WindController API](#windcontroller-api)
5. [WindZone API](#windzone-api)
6. [Wind Physics Models](#wind-physics-models)
7. [Scene Components](#scene-components)
8. [Usage Examples](#usage-examples)
9. [Configuration](#configuration)

---

## Overview

ZephyrSim is an open-source drone simulation environment built with NVIDIA Isaac Sim and OpenUSD. It provides realistic drone flight simulation with advanced wind physics, GPS/IMU simulation, and dynamic environmental conditions.

### Key Features
- Realistic drone flight physics with wind effects
- Multiple wind physics models (Dryden turbulence, tornadoes, microbursts)
- Configurable wind zones and environmental conditions
- OpenUSD-based 3D scene management
- Python scripting API for custom flight behaviors

---

## Core Components

### Project Structure
```
ZephyrSim/
├── scripts/
│   ├── fly_to_waypoints.py    # Main drone control script
│   ├── wind_controller.py     # Wind physics and control
│   └── wind_tuning.py         # Wind parameter tuning
├── assets/
│   ├── drone.usd             # Drone 3D model
│   └── wind_zone.usd         # Wind zone visualization
├── environments/
│   └── open_field.usd        # Environment scene
└── main_stage.usd            # Main scene composition
```

---

## DroneController API

The `DroneController` class provides high-level control for drone navigation with wind physics integration.

### Class: DroneController

#### Constructor
```python
DroneController(drone_prim_path="/World/Drone")
```

**Parameters:**
- `drone_prim_path` (str): USD path to the drone primitive in the scene

**Properties:**
- `current_position` (np.array): Current drone position [x, y, z] in meters
- `current_velocity` (np.array): Current drone velocity [vx, vy, vz] in m/s
- `target_position` (np.array): Target waypoint position [x, y, z] in meters
- `max_velocity` (float): Maximum drone velocity (default: 5.0 m/s)
- `max_acceleration` (float): Maximum drone acceleration (default: 2.0 m/s²)
- `position_tolerance` (float): Waypoint arrival tolerance (default: 0.5 m)
- `mass` (float): Drone mass in kg (default: 1.5 kg)
- `drag_coefficient` (float): Aerodynamic drag coefficient (default: 0.3)

#### Methods

##### set_target(target_position)
Set the target waypoint position for the drone.

```python
controller.set_target([10, 8, 5])
```

**Parameters:**
- `target_position` (list/np.array): Target position [x, y, z] in meters

**Example:**
```python
# Navigate to a waypoint at 10m forward, 8m up, 5m right
controller.set_target([10, 8, 5])
```

##### get_current_position()
Get the current drone position from the simulation or stage.

```python
position = controller.get_current_position()
```

**Returns:**
- `np.array`: Current position [x, y, z] in meters

##### calculate_wind_force(position, velocity)
Calculate wind forces acting on the drone at a given position and velocity.

```python
wind_force = controller.calculate_wind_force(position, velocity)
```

**Parameters:**
- `position` (np.array): Drone position [x, y, z] in meters
- `velocity` (np.array): Drone velocity [vx, vy, vz] in m/s

**Returns:**
- `np.array`: Wind force vector [fx, fy, fz] in Newtons

**Physics Model:**
- Combines drag force and wind interaction
- Uses relative velocity between drone and wind
- Applies aerodynamic drag: F = -0.5 × ρ × Cd × A × |v_rel| × v_rel

##### calculate_control(dt)
Calculate control inputs and update drone state for waypoint navigation.

```python
result = controller.calculate_control(0.016)  # 60 FPS timestep
```

**Parameters:**
- `dt` (float): Time step in seconds

**Returns:**
- `dict`: Control result containing:
  - `position` (np.array): Updated drone position
  - `velocity` (np.array): Updated drone velocity
  - `target_reached` (bool): Whether target waypoint is reached
  - `distance` (float): Distance to target in meters
  - `wind_force` (np.array): Applied wind force
  - `control_acceleration` (np.array): Control acceleration

**Control Algorithm:**
1. Proportional position control
2. Velocity limiting
3. Wind force integration
4. Acceleration limiting
5. State integration

##### update_drone_position(new_position)
Update the drone's position in the USD stage.

```python
controller.update_drone_position([10, 8, 5])
```

**Parameters:**
- `new_position` (list/np.array): New position [x, y, z] in meters

---

## WindController API

The `WindController` class manages multiple wind zones and provides unified wind field access.

### Class: WindController

#### Constructor
```python
WindController()
```

**Properties:**
- `wind_zones` (dict): Dictionary of WindZone objects keyed by name
- `time` (float): Simulation time in seconds
- `dt` (float): Time step in seconds (default: 0.016)

#### Methods

##### add_wind_zone(zone_name, position, size=10.0)
Add a new wind zone to the controller.

```python
controller.add_wind_zone("MainWind", [0, 10, 0], 15.0)
```

**Parameters:**
- `zone_name` (str): Unique identifier for the wind zone
- `position` (list/np.array): Zone center position [x, y, z] in meters
- `size` (float): Zone radius in meters (default: 10.0)

##### get_wind_at_position(position)
Get the combined wind vector from all zones at a specific position.

```python
wind_vector = controller.get_wind_at_position([5, 8, 2])
```

**Parameters:**
- `position` (np.array): Query position [x, y, z] in meters

**Returns:**
- `np.array`: Combined wind velocity [vx, vy, vz] in m/s

##### update()
Update all wind zones and visual indicators.

```python
controller.update()
```

**Should be called each simulation frame to:**
- Update wind physics models
- Refresh visual indicators
- Advance time-dependent effects

##### create_preset_wind_conditions(preset_name)
Apply predefined wind condition presets to all zones.

```python
controller.create_preset_wind_conditions("stormy")
```

**Parameters:**
- `preset_name` (str): Preset name from:
  - `"calm"`: Light winds, minimal turbulence
  - `"moderate"`: Medium winds, some turbulence
  - `"stormy"`: Strong winds, high turbulence
  - `"turbulent"`: Moderate winds, extreme turbulence

**Preset Details:**

| Preset | Wind Speed | Turbulence | Gust Frequency | Gust Amplitude |
|--------|------------|------------|----------------|----------------|
| calm | 2.0 m/s | 0.05 | 0.1 Hz | 1.0 m/s |
| moderate | 8.0 m/s | 0.2 | 0.3 Hz | 3.0 m/s |
| stormy | 15.0 m/s | 0.6 | 0.8 Hz | 8.0 m/s |
| turbulent | 6.0 m/s | 0.8 | 1.2 Hz | 5.0 m/s |

---

## WindZone API

The `WindZone` class represents an individual wind zone with configurable physics parameters.

### Class: WindZone

#### Constructor
```python
WindZone(zone_name, position, size=10.0)
```

**Parameters:**
- `zone_name` (str): Zone identifier
- `position` (list/np.array): Zone center [x, y, z] in meters
- `size` (float): Zone radius in meters

#### Wind Configuration Methods

##### set_wind_speed(speed)
Set base wind speed for the zone.

```python
zone.set_wind_speed(12.0)  # 12 m/s wind
```

**Parameters:**
- `speed` (float): Wind speed in m/s (≥ 0)

##### set_wind_direction(direction)
Set primary wind direction vector.

```python
zone.set_wind_direction([1, 0, 0])  # Eastward wind
zone.set_wind_direction([0.707, 0, 0.707])  # Northeast wind
```

**Parameters:**
- `direction` (list/np.array): Direction vector [x, y, z] (will be normalized)

##### set_turbulence_intensity(intensity)
Set turbulence intensity level.

```python
zone.set_turbulence_intensity(0.3)  # 30% turbulence
```

**Parameters:**
- `intensity` (float): Turbulence intensity [0.0-1.0]

##### set_wind_gusts(frequency, amplitude, duration)
Configure wind gust parameters.

```python
zone.set_wind_gusts(0.5, 4.0, 2.0)  # 0.5 Hz, 4 m/s gusts, 2s duration
```

**Parameters:**
- `frequency` (float): Gust frequency in Hz
- `amplitude` (float): Gust amplitude in m/s
- `duration` (float): Gust duration in seconds

#### Advanced Wind Effects

##### Tornado Configuration
```python
zone.tornado_enabled = True
zone.tornado_center = np.array([10, 0, 10])
zone.tornado_radius = 8.0      # Radius of maximum wind
zone.tornado_strength = 40.0   # Maximum tangential wind speed
zone.tornado_updraft = 20.0    # Maximum updraft velocity
```

##### Gust Front Configuration
```python
zone.gustfront_enabled = True
zone.gustfront_center = np.array([20, 5, 20])
zone.gustfront_radius = 12.0
zone.gustfront_strength = 18.0
zone.gustfront_duration = 2.0
```

##### Microburst Configuration
```python
zone.microburst_enabled = True
zone.microburst_center = np.array([10, 5, 10])
zone.microburst_radius = 8.0
zone.microburst_strength = 25.0
zone.microburst_duration = 1.5
```

##### Dryden Turbulence Configuration
```python
zone.dryden_sigma = 2.0    # Turbulence intensity (m/s)
zone.dryden_L = 200.0      # Turbulence scale length (m)
zone.dryden_V = 10.0       # Mean wind speed (m/s)
```

#### Core Methods

##### get_wind_vector_at_position(position, dt)
Calculate wind velocity at a specific position with all effects combined.

```python
wind = zone.get_wind_vector_at_position([5, 8, 2], 0.016)
```

**Parameters:**
- `position` (np.array): Query position [x, y, z] in meters
- `dt` (float): Time step in seconds

**Returns:**
- `np.array`: Wind velocity [vx, vy, vz] in m/s

**Wind Components Combined:**
1. Vertical wind profile (logarithmic law)
2. Dryden turbulence model
3. Gust fronts
4. Microbursts
5. Perlin noise variations
6. Tornado effects
7. Wind gusts
8. Base turbulence

---

## Wind Physics Models

### Vertical Wind Profile
Models how wind speed varies with altitude using the logarithmic wind profile:

```
v(z) = v_ref * ln(z/z₀) / ln(z_ref/z₀)
```

**Parameters:**
- `z₀`: Surface roughness (default: 0.1 m)
- `z_ref`: Reference height (default: 10 m)
- `v_ref`: Reference wind speed

### Dryden Turbulence Model
Standard aerospace turbulence model generating correlated wind fluctuations:

```python
def dryden_turbulence(dt, state, sigma_u=1.0, L_u=200.0, V=10.0):
    """
    Generate Dryden turbulence
    
    Parameters:
    - dt: Time step (s)
    - state: Previous turbulence state dict
    - sigma_u: Turbulence intensity (m/s)
    - L_u: Turbulence scale length (m)  
    - V: Mean wind speed (m/s)
    
    Returns:
    - new_state: Updated turbulence state
    - turbulence_vector: Wind turbulence [u, v, w] (m/s)
    """
```

### Tornado Model
Realistic tornado wind field with:
- Tangential velocity profile
- Central updraft
- Exponential decay outside core

### Microburst Model
Localized downdraft with radial outflow:
- Strong central downdraft
- Radial surface outflow
- Time-dependent intensity

### Gust Front Model
Sudden wind speed increases:
- Rapid onset
- Exponential decay
- Directional consistency

---

## Scene Components

### USD Scene Structure

#### Main Stage (`main_stage.usd`)
Primary scene composition containing:
- World transform root
- Environment references
- Drone instance
- Wind zone placements
- Physics scene settings

#### Drone Asset (`assets/drone.usd`)
3D drone model with:
- Geometric representation
- Physical properties
- Animation capabilities

#### Wind Zone Asset (`assets/wind_zone.usd`)
Wind zone visualization containing:
- Directional indicators
- Speed gauges
- Turbulence visualizers
- Effect boundaries

#### Environment (`environments/open_field.usd`)
Base environment scene:
- Terrain geometry
- Ground plane
- Lighting setup
- Background elements

---

## Usage Examples

### Basic Drone Navigation

```python
#!/usr/bin/env python3
from scripts.fly_to_waypoints import DroneController
from scripts.wind_controller import WindController
from scripts.wind_tuning import tune_wind

# Initialize drone controller
controller = DroneController()

# Define flight path
waypoints = [
    [0, 5, 0],      # Start
    [10, 8, 5],     # Waypoint 1
    [20, 10, 10],   # Waypoint 2
    [0, 5, 0]       # Return
]

# Set up wind conditions
if controller.wind_controller:
    controller.wind_controller.create_preset_wind_conditions("moderate")
    tune_wind(controller.wind_controller)

# Simulation loop
dt = 0.016  # 60 FPS
waypoint_index = 0

for waypoint in waypoints:
    controller.set_target(waypoint)
    
    while True:
        result = controller.calculate_control(dt)
        controller.update_drone_position(result['position'])
        
        if result['target_reached']:
            break
            
        time.sleep(dt)
```

### Custom Wind Zone Setup

```python
from scripts.wind_controller import WindController

# Create wind controller
wind = WindController()

# Add multiple wind zones
wind.add_wind_zone("Valley", [0, 5, 0], 20.0)
wind.add_wind_zone("Mountain", [50, 15, 30], 15.0)

# Configure valley winds
valley_zone = wind.wind_zones["Valley"]
valley_zone.set_wind_speed(6.0)
valley_zone.set_wind_direction([1, 0, 0])
valley_zone.set_turbulence_intensity(0.2)

# Add tornado to mountain zone
mountain_zone = wind.wind_zones["Mountain"]
mountain_zone.tornado_enabled = True
mountain_zone.tornado_center = np.array([50, 5, 30])
mountain_zone.tornado_radius = 10.0
mountain_zone.tornado_strength = 35.0

# Query wind at specific position
position = [25, 8, 15]
wind_vector = wind.get_wind_at_position(position)
print(f"Wind at {position}: {wind_vector} m/s")
```

### Advanced Wind Physics Configuration

```python
def setup_storm_system(wind_controller):
    """Configure a complex storm system with multiple effects"""
    
    for zone_name, zone in wind_controller.wind_zones.items():
        # Base storm conditions
        zone.set_wind_speed(18.0)
        zone.set_wind_direction([0.8, 0.1, 0.6])  # Variable direction
        zone.set_turbulence_intensity(0.7)
        zone.set_wind_gusts(1.0, 12.0, 3.0)
        
        # Dryden turbulence for realism
        zone.dryden_sigma = 4.0
        zone.dryden_L = 150.0
        zone.dryden_V = 18.0
        
        # Gust front system
        zone.gustfront_enabled = True
        zone.gustfront_center = np.array([30, 5, 20])
        zone.gustfront_radius = 25.0
        zone.gustfront_strength = 25.0
        zone.gustfront_duration = 4.0
        
        # Microburst activity
        zone.microburst_enabled = True
        zone.microburst_center = np.array([15, 8, 10])
        zone.microburst_radius = 12.0
        zone.microburst_strength = 30.0
        zone.microburst_duration = 2.5
```

### Flight Data Analysis

```python
def analyze_flight_performance(controller, flight_duration):
    """Analyze drone performance under wind conditions"""
    
    dt = 0.016
    steps = int(flight_duration / dt)
    
    positions = []
    velocities = []
    wind_forces = []
    
    for step in range(steps):
        result = controller.calculate_control(dt)
        
        positions.append(result['position'].copy())
        velocities.append(result['velocity'].copy())
        wind_forces.append(result['wind_force'].copy())
        
        controller.update_drone_position(result['position'])
    
    # Analysis
    positions = np.array(positions)
    velocities = np.array(velocities)
    wind_forces = np.array(wind_forces)
    
    # Calculate statistics
    avg_speed = np.mean(np.linalg.norm(velocities, axis=1))
    max_wind_force = np.max(np.linalg.norm(wind_forces, axis=1))
    flight_distance = np.sum(np.linalg.norm(np.diff(positions, axis=0), axis=1))
    
    return {
        'average_speed': avg_speed,
        'maximum_wind_force': max_wind_force,
        'total_distance': flight_distance,
        'positions': positions,
        'velocities': velocities,
        'wind_forces': wind_forces
    }
```

---

## Configuration

### Wind Tuning Function
The `tune_wind()` function in `wind_tuning.py` provides a convenient way to apply comprehensive wind configurations:

```python
def tune_wind(controller):
    """Apply comprehensive wind tuning to all zones"""
    for zone in controller.wind_zones.values():
        # Basic wind parameters
        zone.set_wind_speed(10.0)
        zone.set_wind_direction([1, 0, 0])
        zone.set_turbulence_intensity(0.5)
        zone.set_wind_gusts(0.3, 4.0, 1.5)
        
        # Noise parameters
        zone.noise_scale = 0.07
        zone.noise_amplitude = 2.5
        zone.noise_time_speed = 0.12
        
        # Updraft configuration
        zone.updraft_center = np.array([5, 0, 5])
        zone.updraft_radius = 8.0
        zone.updraft_strength = 2.5
        
        # Wind shear
        zone.shear_y = 12.0
        zone.shear_thickness = 3.0
        zone.shear_vector = np.array([2.0, 0, 1.0])
        
        # Advanced effects
        zone.tornado_enabled = True
        zone.tornado_center = np.array([10, 0, 10])
        zone.tornado_radius = 8.0
        zone.tornado_strength = 40.0
        zone.tornado_updraft = 20.0
        
        # Dryden turbulence
        zone.dryden_sigma = 2.0
        zone.dryden_L = 200.0
        zone.dryden_V = 10.0
        
        # Gust front
        zone.gustfront_enabled = True
        zone.gustfront_center = np.array([20, 5, 20])
        zone.gustfront_radius = 12.0
        zone.gustfront_strength = 18.0
        zone.gustfront_duration = 2.0
        
        # Microburst
        zone.microburst_enabled = True
        zone.microburst_center = np.array([10, 5, 10])
        zone.microburst_radius = 8.0
        zone.microburst_strength = 25.0
        zone.microburst_duration = 1.5
```

### Simulation Parameters

| Parameter | Default | Unit | Description |
|-----------|---------|------|-------------|
| Simulation timestep | 0.016 | s | 60 FPS simulation rate |
| Drone mass | 1.5 | kg | Default drone mass |
| Max velocity | 5.0 | m/s | Maximum drone speed |
| Max acceleration | 2.0 | m/s² | Maximum drone acceleration |
| Position tolerance | 0.5 | m | Waypoint arrival threshold |
| Air density | 1.225 | kg/m³ | Standard atmospheric density |
| Drag coefficient | 0.3 | - | Drone aerodynamic drag |

### Error Handling

The API includes comprehensive error handling for:
- Missing Isaac Sim dependencies
- Invalid parameter values
- USD stage access failures
- Wind zone configuration errors
- Simulation stability issues

Example error handling:
```python
try:
    controller = DroneController()
    wind_result = controller.calculate_wind_force(position, velocity)
except ImportError as e:
    print(f"Missing dependency: {e}")
    # Fallback to simulation mode
except ValueError as e:
    print(f"Invalid parameter: {e}")
    # Use default values
except Exception as e:
    print(f"Simulation error: {e}")
    # Graceful degradation
```

---

This documentation provides comprehensive coverage of all public APIs, functions, and components in ZephyrSim. For additional examples and advanced usage patterns, refer to the included scripts and the project repository.