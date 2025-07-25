# ZephyrSim Quick Reference

Quick reference for common ZephyrSim operations and parameters.

---

## 🚁 Basic Drone Control

### DroneController Creation
```python
from scripts.fly_to_waypoints import DroneController
controller = DroneController()
```

### Set Target & Fly
```python
controller.set_target([x, y, z])  # Position in meters
result = controller.calculate_control(0.016)  # 60 FPS timestep

# Check if reached
if result['target_reached']:
    print("Target reached!")
```

### Result Dictionary
```python
result = {
    'position': [x, y, z],           # Current position
    'velocity': [vx, vy, vz],        # Current velocity
    'target_reached': bool,          # True if at target
    'distance': float,               # Distance to target (m)
    'wind_force': [fx, fy, fz],      # Wind force (N)
    'control_acceleration': [ax, ay, az]  # Control acceleration
}
```

---

## 🌪️ Wind Controller

### Basic Setup
```python
from scripts.wind_controller import WindController
wind = WindController()

# Add wind zone
wind.add_wind_zone("Zone1", [x, y, z], radius)

# Get wind zone
zone = wind.wind_zones["Zone1"]
```

### Wind Configuration
```python
# Basic wind parameters
zone.set_wind_speed(speed_m_per_s)
zone.set_wind_direction([x, y, z])  # Normalized automatically
zone.set_turbulence_intensity(0.0_to_1.0)
zone.set_wind_gusts(frequency_hz, amplitude_m_per_s, duration_s)

# Get wind at position
wind_vector = wind.get_wind_at_position([x, y, z])
```

### Quick Presets
```python
wind.create_preset_wind_conditions("calm")      # 2 m/s, low turbulence
wind.create_preset_wind_conditions("moderate")  # 8 m/s, medium turbulence
wind.create_preset_wind_conditions("stormy")    # 15 m/s, high turbulence
wind.create_preset_wind_conditions("turbulent") # 6 m/s, extreme turbulence
```

---

## 🌀 Advanced Wind Effects

### Tornado
```python
zone.tornado_enabled = True
zone.tornado_center = np.array([x, y, z])
zone.tornado_radius = 8.0         # Radius of max wind (m)
zone.tornado_strength = 40.0      # Max tangential speed (m/s)
zone.tornado_updraft = 20.0       # Max updraft (m/s)
```

### Microburst
```python
zone.microburst_enabled = True
zone.microburst_center = np.array([x, y, z])
zone.microburst_radius = 8.0      # Effect radius (m)
zone.microburst_strength = 25.0   # Downdraft strength (m/s)
zone.microburst_duration = 1.5    # Duration (s)
```

### Gust Front
```python
zone.gustfront_enabled = True
zone.gustfront_center = np.array([x, y, z])
zone.gustfront_radius = 12.0      # Effect radius (m)
zone.gustfront_strength = 18.0    # Wind speed increase (m/s)
zone.gustfront_duration = 2.0     # Duration (s)
```

### Dryden Turbulence
```python
zone.dryden_sigma = 2.0          # Turbulence intensity (m/s)
zone.dryden_L = 200.0            # Scale length (m)
zone.dryden_V = 10.0             # Mean wind speed (m/s)
```

---

## 📍 Common Flight Patterns

### Simple Waypoint Flight
```python
waypoints = [[0,5,0], [10,8,5], [20,10,10], [0,5,0]]
for waypoint in waypoints:
    controller.set_target(waypoint)
    while True:
        result = controller.calculate_control(0.016)
        if result['target_reached']:
            break
        time.sleep(0.016)
```

### Circular Pattern
```python
import numpy as np
waypoints = []
for i in range(num_points):
    angle = 2 * np.pi * i / num_points
    x = radius * np.cos(angle)
    z = radius * np.sin(angle)
    waypoints.append([x, height, z])
```

### Grid Search
```python
waypoints = []
for x in range(-size//2, size//2+1, spacing):
    for z in range(-size//2, size//2+1, spacing):
        waypoints.append([x, height, z])
```

---

## 🔧 Default Parameters

### Drone Physics
| Parameter | Default | Unit | Description |
|-----------|---------|------|-------------|
| mass | 1.5 | kg | Drone mass |
| max_velocity | 5.0 | m/s | Maximum speed |
| max_acceleration | 2.0 | m/s² | Maximum acceleration |
| position_tolerance | 0.5 | m | Waypoint arrival threshold |
| drag_coefficient | 0.3 | - | Aerodynamic drag |
| air_density | 1.225 | kg/m³ | Air density |

### Simulation Settings
| Parameter | Default | Description |
|-----------|---------|-------------|
| dt | 0.016 | Time step (60 FPS) |
| coordinate_system | Y-up | Isaac Sim standard |
| gravity | [0, -9.81, 0] | Gravity vector |

---

## 🎯 Coordinate System

```
Y
↑
│   Z
│  ↗
│ /
│/
└────────→ X

X: Forward/East
Y: Up
Z: Right/North
```

### Common Positions
- Start: `[0, 5, 0]` (5m above origin)
- Forward: `[10, 5, 0]` (10m east)
- Up: `[0, 15, 0]` (15m altitude)
- Right: `[0, 5, 10]` (10m north)

---

## 🌬️ Wind Direction Vectors

```python
# Cardinal directions
EAST = [1, 0, 0]
WEST = [-1, 0, 0]
NORTH = [0, 0, 1]
SOUTH = [0, 0, -1]
UP = [0, 1, 0]
DOWN = [0, -1, 0]

# Diagonal winds
NORTHEAST = [0.707, 0, 0.707]
NORTHWEST = [-0.707, 0, 0.707]
SOUTHEAST = [0.707, 0, -0.707]
SOUTHWEST = [-0.707, 0, -0.707]
```

---

## 📊 Quick Diagnostics

### Check System Status
```python
# Isaac Sim availability
try:
    import omni.isaac.core.utils.stage as stage_utils
    print("✅ Isaac Sim available")
except ImportError:
    print("❌ Isaac Sim not available - using standalone mode")

# Wind controller
try:
    from scripts.wind_controller import WindController
    print("✅ Wind controller available")
except ImportError:
    print("❌ Wind controller not available")
```

### Test Basic Functionality
```python
controller = DroneController()
controller.set_target([5, 8, 3])
result = controller.calculate_control(0.016)
print(f"Position: {result['position']}")
print(f"Distance: {result['distance']:.1f}m")
```

---

## 🔍 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ImportError: No module named 'omni'` | Run within Isaac Sim or use standalone mode |
| `ImportError: No module named 'scripts'` | Add scripts to Python path: `sys.path.append('./scripts')` |
| `ImportError: No module named 'noise'` | Install: `pip install noise` (optional) |
| Wind effects not working | Check wind controller initialization in DroneController |
| Drone not moving | Check target is different from current position |
| Simulation too slow | Increase dt or reduce update frequency |

---

## 🚀 Quick Start Template

```python
#!/usr/bin/env python3
import sys
import time
import numpy as np

# Setup
sys.path.append('./scripts')
from fly_to_waypoints import DroneController
from wind_tuning import tune_wind

# Create controller
controller = DroneController()

# Setup wind (optional)
if controller.wind_controller:
    controller.wind_controller.create_preset_wind_conditions("moderate")
    tune_wind(controller.wind_controller)

# Define flight path
waypoints = [
    [0, 5, 0],      # Start
    [10, 8, 5],     # Waypoint 1
    [20, 10, 10],   # Waypoint 2
    [0, 5, 0]       # Return
]

# Fly mission
dt = 0.016
for waypoint in waypoints:
    print(f"Flying to {waypoint}")
    controller.set_target(waypoint)
    
    while True:
        result = controller.calculate_control(dt)
        if result['target_reached']:
            print("Reached!")
            break
        time.sleep(dt)

print("Mission complete!")
```

---

## 📚 Documentation Links

- **Full API Documentation**: `API_DOCUMENTATION.md`
- **Component Reference**: `COMPONENT_REFERENCE.md`
- **Usage Examples**: `USAGE_EXAMPLES.md`
- **Project README**: `README.md`

---

*ZephyrSim v0.1.8 - For latest updates see [GitHub Repository](https://github.com/SaharshSS/ZephyrSim)*