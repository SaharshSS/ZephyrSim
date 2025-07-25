# ZephyrSim Component Reference

This document provides detailed information about all components, scripts, and assets in the ZephyrSim project.

---

## Table of Contents

1. [Scripts Overview](#scripts-overview)
2. [Asset Components](#asset-components)
3. [Environment Components](#environment-components)
4. [Utility Functions](#utility-functions)
5. [Physics Models](#physics-models)
6. [Visualization Components](#visualization-components)

---

## Scripts Overview

### `fly_to_waypoints.py`

**Purpose:** Main drone navigation and control script with waypoint-based flight planning.

**Key Components:**

#### `DroneController` Class
- **Location:** Lines 36-185
- **Dependencies:** numpy, Isaac Sim modules (optional), WindController
- **Key Features:**
  - Proportional control for waypoint navigation
  - Wind force integration
  - Real-time position tracking
  - Aerodynamic drag modeling

**Physics Properties:**
```python
# Default drone characteristics
mass = 1.5 kg
drag_coefficient = 0.3
cross_sectional_area = 0.1 m²
air_density = 1.225 kg/m³
```

**Control Parameters:**
```python
max_velocity = 5.0 m/s
max_acceleration = 2.0 m/s²
position_tolerance = 0.5 m
velocity_tolerance = 0.1 m/s
```

#### `print_status()` Function
- **Location:** Lines 185-192
- **Purpose:** Formatted console output for flight status
- **Parameters:** waypoint_index, total_waypoints, position, distance, velocity, wind_force, control_acc

#### `main()` Function
- **Location:** Lines 194-287
- **Features:**
  - Predefined waypoint course
  - Wind condition setup
  - 60 FPS simulation loop
  - Comprehensive error handling

**Default Flight Path:**
```python
waypoints = [
    [0, 5, 0],      # Start position
    [10, 8, 5],     # Waypoint 1
    [20, 10, 10],   # Waypoint 2 (enters wind zone)
    [15, 15, 15],   # Waypoint 3
    [5, 12, 8],     # Waypoint 4
    [0, 5, 0]       # Return to start
]
```

---

### `wind_controller.py`

**Purpose:** Advanced wind physics simulation with multiple atmospheric models.

#### Global Functions

##### `dryden_turbulence(dt, state, sigma_u, L_u, V)`
- **Location:** Lines 33-43
- **Model:** Standard aerospace turbulence model
- **Implementation:** First-order Markov process
- **Returns:** Updated state and turbulence vector

**Mathematical Model:**
```
τ = L_u / V
φ = exp(-dt / τ)
u = φ * u_prev + σ_u * sqrt(1 - φ²) * noise
```

#### `WindZone` Class
- **Location:** Lines 45-384
- **Capabilities:** Individual wind zone with comprehensive atmospheric effects

**Core Wind Effects:**

1. **Vertical Wind Profile**
   - Model: Logarithmic boundary layer
   - Implementation: `v(z) = v_ref * ln(z/z₀) / ln(z_ref/z₀)`
   - Default z₀: 0.1 m (surface roughness)

2. **Dryden Turbulence**
   - Industry-standard turbulence model
   - Correlated fluctuations in all axes
   - Configurable intensity and scale

3. **Tornado Model**
   - Tangential velocity with radial decay
   - Central updraft component
   - Realistic wind speed profile

4. **Microburst Model**
   - Downdraft with radial outflow
   - Time-dependent intensity
   - Surface interaction effects

5. **Gust Front Model**
   - Sudden wind speed increases
   - Exponential decay profile
   - Directional consistency

**Visual Indicators:**
- Wind direction arrows
- Speed gauges
- Turbulence sphere scaling
- Tornado visualization cylinders

#### `WindController` Class
- **Location:** Lines 386-511
- **Purpose:** Multi-zone wind field management
- **Features:**
  - Zone composition
  - Preset configurations
  - Unified wind field access

**Preset Wind Conditions:**

| Preset | Speed (m/s) | Turbulence | Gust Freq (Hz) | Gust Amp (m/s) |
|--------|-------------|------------|----------------|----------------|
| calm | 2.0 | 0.05 | 0.1 | 1.0 |
| moderate | 8.0 | 0.2 | 0.3 | 3.0 |
| stormy | 15.0 | 0.6 | 0.8 | 8.0 |
| turbulent | 6.0 | 0.8 | 1.2 | 5.0 |

---

### `wind_tuning.py`

**Purpose:** Predefined wind parameter configurations for testing and demonstration.

#### `tune_wind(controller)` Function
- **Location:** Lines 3-38
- **Purpose:** Apply comprehensive wind settings to all zones
- **Effects Applied:**
  - Base wind parameters
  - Noise characteristics
  - Updraft configurations
  - Wind shear effects
  - Advanced phenomena (tornadoes, microbursts, gust fronts)

**Applied Parameters:**
```python
# Base wind
wind_speed = 10.0 m/s
wind_direction = [1, 0, 0]  # Eastward
turbulence_intensity = 0.5

# Gust characteristics
gust_frequency = 0.3 Hz
gust_amplitude = 4.0 m/s
gust_duration = 1.5 s

# Tornado configuration
tornado_radius = 8.0 m
tornado_strength = 40.0 m/s
tornado_updraft = 20.0 m/s

# Microburst parameters
microburst_radius = 8.0 m
microburst_strength = 25.0 m/s
microburst_duration = 1.5 s
```

---

## Asset Components

### `drone.usd`

**Purpose:** 3D drone model with physical properties for simulation.

**Content Structure:**
- Geometric mesh representation
- Material and texture definitions
- Physical collision bounds
- Animation-ready hierarchy

**Coordinate System:**
- Forward: +X axis
- Up: +Y axis
- Right: +Z axis

**Default Placement:** (0, 5, 0) in main scene

### `wind_zone.usd`

**Purpose:** Visual representation and interaction bounds for wind zones.

**Components:**
- Zone boundary visualization
- Wind direction indicators
- Speed measurement displays
- Turbulence intensity indicators

**Visual Elements:**
- Directional arrows showing wind flow
- Speed gauge with 0-20 m/s range
- Turbulence sphere with intensity scaling
- Optional tornado visualization cylinders

**Default Instances:**
- WindZone1: Position (20, 10, 0), Size 10.0m
- WindZone2: Position (-15, 15, 30), Size 12.0m

---

## Environment Components

### `open_field.usd`

**Purpose:** Base environment scene providing terrain and atmospheric context.

**Components:**
- Ground plane geometry
- Terrain features
- Lighting setup
- Background elements
- Physics materials

**Environment Properties:**
- Scale: Large open area suitable for drone navigation
- Lighting: Realistic outdoor illumination
- Physics: Ground collision and interaction surfaces

### `main_stage.usd`

**Purpose:** Primary scene composition combining all elements.

**Scene Hierarchy:**
```
World/
├── OpenField/          # Base environment
├── Drone/              # Drone instance at (0, 5, 0)
├── WindZone1/          # Wind zone at (20, 10, 0)
├── WindZone2/          # Wind zone at (-15, 15, 30)
└── physicsScene/       # Physics simulation settings
```

**Physics Settings:**
- Gravity: (0, -1, 0) at 9.81 m/s²
- Solver iterations: High precision
- Time stepping: Real-time compatible

---

## Utility Functions

### Print and Display Functions

#### `print_status()` in `fly_to_waypoints.py`
```python
def print_status(waypoint_index, total_waypoints, position, distance, velocity, wind_force, control_acc):
    """
    Display formatted flight status information
    
    Output format:
    📍 Waypoint X/Y
       Position: [x, y, z]
       Distance: X.XXm
       Velocity: [vx, vy, vz] m/s
       Wind Force: [fx, fy, fz] N
       Control Acc: [ax, ay, az] m/s²
    """
```

### Vector and Transform Utilities

#### `_vector_to_rotation()` in `wind_controller.py`
```python
def _vector_to_rotation(self, v1, v2):
    """
    Convert direction vectors to rotation angles
    
    Parameters:
    - v1: Source direction vector
    - v2: Target direction vector
    
    Returns:
    - [rx, ry, rz]: Euler angles in radians
    
    Algorithm:
    1. Normalize input vectors
    2. Calculate rotation axis via cross product
    3. Calculate rotation angle via dot product
    4. Convert to Euler angles
    """
```

---

## Physics Models

### Aerodynamic Drag Model

**Implementation:** `DroneController.calculate_wind_force()`

**Formula:**
```
F_drag = -0.5 * ρ * Cd * A * |v_rel| * v_rel
```

**Parameters:**
- ρ (rho): Air density = 1.225 kg/m³
- Cd: Drag coefficient = 0.3
- A: Cross-sectional area = 0.1 m²
- v_rel: Relative velocity (drone - wind)

### Wind Profile Models

#### Logarithmic Boundary Layer
```python
z0 = 0.1  # Surface roughness (m)
z_ref = 10.0  # Reference height (m)
v_ref = wind_speed  # Reference wind speed
z = max(0.1, position[1])  # Current height

log_profile = v_ref * np.log(z/z0) / np.log(z_ref/z0)
```

#### Dryden Turbulence
```python
tau = L_u / V  # Time constant
phi = exp(-dt / tau)  # Correlation factor
u = phi * u_prev + sigma_u * sqrt(1 - phi**2) * noise
```

### Tornado Wind Field

**Tangential Velocity:**
```python
if dist < tornado_radius:
    speed = tornado_strength * (dist / tornado_radius)
else:
    speed = tornado_strength * exp(-(dist - tornado_radius) / tornado_radius)
```

**Updraft Component:**
```python
updraft = tornado_updraft * exp(-dist / (tornado_radius * 0.7))
```

---

## Visualization Components

### Wind Direction Indicators

**Purpose:** Visual representation of wind flow direction in 3D space.

**Implementation:**
- Arrow-shaped primitives
- Real-time rotation based on wind direction
- Color coding for wind speed intensity

### Speed Gauges

**Purpose:** Quantitative display of wind speed magnitude.

**Features:**
- Linear scale from 0-20 m/s
- Position-based indicator movement
- Real-time updates

### Turbulence Visualizers

**Purpose:** Visual indication of turbulence intensity levels.

**Implementation:**
- Sphere scaling based on intensity
- Dynamic size changes
- Color variations for intensity levels

### Tornado Visualization

**Purpose:** 3D representation of tornado wind effects.

**Components:**
- Cylindrical core representation
- Height scaling (30m default)
- Radius visualization
- Position tracking

---

## Error Handling and Fallbacks

### Isaac Sim Dependency Management

```python
try:
    import omni.isaac.core.utils.stage as stage_utils
    # ... other Isaac Sim imports
    ISAAC_SIM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Isaac Sim not available: {e}")
    ISAAC_SIM_AVAILABLE = False
```

### Wind Controller Fallbacks

```python
try:
    from scripts.wind_controller import WindController
    WIND_CONTROLLER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Wind controller not available: {e}")
    WIND_CONTROLLER_AVAILABLE = False
```

### Graceful Degradation

When dependencies are missing:
- Simulation continues in standalone mode
- Wind effects are disabled gracefully
- Position tracking uses internal simulation
- Visual updates are skipped safely

---

## Performance Considerations

### Simulation Timing

**Target Framerate:** 60 FPS (dt = 0.016s)

**Performance Optimizations:**
- Efficient vector operations using NumPy
- Minimal USD stage access
- Cached wind calculations
- Optimized visual update frequency

### Memory Usage

**Wind Zone Storage:**
- Minimal state variables per zone
- Efficient NumPy array operations
- Garbage collection friendly

**Visual Indicators:**
- Lazy creation of visualization prims
- Conditional updates based on changes
- Optimized transformation calculations

---

This component reference provides detailed implementation information for all ZephyrSim components. For high-level API usage, refer to the main API Documentation.