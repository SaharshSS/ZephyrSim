# ZephyrSim Usage Examples

This guide provides practical examples and tutorials for using ZephyrSim's APIs and components.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Basic Flight Control](#basic-flight-control)
3. [Wind Configuration](#wind-configuration)
4. [Advanced Wind Effects](#advanced-wind-effects)
5. [Custom Flight Patterns](#custom-flight-patterns)
6. [Data Analysis and Logging](#data-analysis-and-logging)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Minimal Example

```python
#!/usr/bin/env python3
"""Minimal ZephyrSim example - fly to a single waypoint"""

import sys
import time
import numpy as np

# Add scripts directory to path
sys.path.append('./scripts')

from fly_to_waypoints import DroneController

def main():
    # Create drone controller
    controller = DroneController()
    
    # Set target waypoint
    target = [10, 8, 5]  # 10m forward, 8m up, 5m right
    controller.set_target(target)
    
    print(f"Flying to {target}")
    
    # Simple control loop
    dt = 0.016  # 60 FPS
    for step in range(1000):  # Max 16.6 seconds
        result = controller.calculate_control(dt)
        
        if result['target_reached']:
            print("Target reached!")
            break
            
        # Print progress every second
        if step % 60 == 0:
            pos = result['position']
            dist = result['distance']
            print(f"Position: [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}], Distance: {dist:.1f}m")
        
        time.sleep(dt)

if __name__ == "__main__":
    main()
```

### Running with Isaac Sim

```bash
# Launch Isaac Sim and run the script
./python.sh scripts/fly_to_waypoints.py

# Or run standalone without Isaac Sim
python3 scripts/fly_to_waypoints.py
```

---

## Basic Flight Control

### Simple Waypoint Navigation

```python
#!/usr/bin/env python3
"""Basic waypoint navigation example"""

import sys
import time
import numpy as np
sys.path.append('./scripts')

from fly_to_waypoints import DroneController

def basic_flight():
    """Fly through a simple rectangular path"""
    
    controller = DroneController()
    
    # Define flight path
    waypoints = [
        [0, 5, 0],      # Start
        [10, 5, 0],     # East
        [10, 5, 10],    # East + North
        [0, 5, 10],     # North
        [0, 5, 0]       # Return home
    ]
    
    dt = 0.016
    
    for i, waypoint in enumerate(waypoints):
        print(f"\n=== Waypoint {i+1}/{len(waypoints)}: {waypoint} ===")
        controller.set_target(waypoint)
        
        start_time = time.time()
        while True:
            result = controller.calculate_control(dt)
            
            if result['target_reached']:
                elapsed = time.time() - start_time
                print(f"Reached waypoint in {elapsed:.1f} seconds")
                break
            
            time.sleep(dt)
    
    print("\nFlight complete!")

if __name__ == "__main__":
    basic_flight()
```

### Circular Flight Pattern

```python
def circular_flight(radius=10, height=8, num_points=12):
    """Fly in a circle at specified radius and height"""
    
    controller = DroneController()
    
    # Generate circular waypoints
    waypoints = []
    for i in range(num_points + 1):  # +1 to close the circle
        angle = 2 * np.pi * i / num_points
        x = radius * np.cos(angle)
        z = radius * np.sin(angle)
        waypoints.append([x, height, z])
    
    print(f"Flying circular pattern: radius={radius}m, height={height}m")
    
    dt = 0.016
    for i, waypoint in enumerate(waypoints):
        controller.set_target(waypoint)
        
        while True:
            result = controller.calculate_control(dt)
            if result['target_reached']:
                print(f"Waypoint {i+1}/{len(waypoints)} reached")
                break
            time.sleep(dt)

# Usage
circular_flight(radius=15, height=10, num_points=16)
```

### Spiral Ascent

```python
def spiral_ascent(max_height=20, radius=8, num_turns=3):
    """Fly in ascending spiral pattern"""
    
    controller = DroneController()
    
    # Generate spiral waypoints
    waypoints = []
    points_per_turn = 12
    total_points = num_turns * points_per_turn
    
    for i in range(total_points + 1):
        angle = 2 * np.pi * i / points_per_turn
        height = 5 + (max_height - 5) * i / total_points
        x = radius * np.cos(angle)
        z = radius * np.sin(angle)
        waypoints.append([x, height, z])
    
    print(f"Flying spiral ascent: {max_height}m max height, {num_turns} turns")
    
    dt = 0.016
    for waypoint in waypoints:
        controller.set_target(waypoint)
        
        while True:
            result = controller.calculate_control(dt)
            if result['target_reached']:
                break
            time.sleep(dt)

# Usage
spiral_ascent(max_height=25, radius=12, num_turns=2)
```

---

## Wind Configuration

### Basic Wind Setup

```python
#!/usr/bin/env python3
"""Wind configuration examples"""

import sys
sys.path.append('./scripts')

from wind_controller import WindController
from wind_tuning import tune_wind

def setup_light_wind():
    """Configure light wind conditions"""
    
    wind = WindController()
    wind.add_wind_zone("MainWind", [0, 10, 0], 25.0)
    
    zone = wind.wind_zones["MainWind"]
    zone.set_wind_speed(3.0)  # Light breeze
    zone.set_wind_direction([1, 0, 0])  # Eastward
    zone.set_turbulence_intensity(0.1)  # Minimal turbulence
    zone.set_wind_gusts(0.1, 1.0, 2.0)  # Rare, gentle gusts
    
    return wind

def setup_moderate_wind():
    """Configure moderate wind conditions"""
    
    wind = WindController()
    wind.add_wind_zone("MainWind", [0, 10, 0], 25.0)
    
    # Use preset
    wind.create_preset_wind_conditions("moderate")
    
    return wind

def setup_custom_wind():
    """Configure custom wind with multiple zones"""
    
    wind = WindController()
    
    # Valley wind zone
    wind.add_wind_zone("Valley", [0, 5, 0], 20.0)
    valley = wind.wind_zones["Valley"]
    valley.set_wind_speed(6.0)
    valley.set_wind_direction([0.8, 0.2, 0.6])  # Diagonal wind
    valley.set_turbulence_intensity(0.15)
    
    # Mountain wind zone with stronger conditions
    wind.add_wind_zone("Mountain", [30, 15, 20], 15.0)
    mountain = wind.wind_zones["Mountain"]
    mountain.set_wind_speed(12.0)
    mountain.set_wind_direction([0.6, -0.3, 0.8])  # Downslope wind
    mountain.set_turbulence_intensity(0.4)
    mountain.set_wind_gusts(0.5, 5.0, 3.0)  # Stronger gusts
    
    return wind

# Test wind at different positions
def test_wind_field(wind_controller):
    """Test wind velocities at various positions"""
    
    test_positions = [
        [0, 8, 0],      # Valley center
        [15, 10, 10],   # Between zones
        [30, 15, 20],   # Mountain center
        [50, 5, 0]      # Outside zones
    ]
    
    for pos in test_positions:
        wind_vec = wind_controller.get_wind_at_position(pos)
        wind_speed = np.linalg.norm(wind_vec)
        print(f"Position {pos}: Wind {wind_vec}, Speed {wind_speed:.1f} m/s")

# Usage example
if __name__ == "__main__":
    wind = setup_custom_wind()
    test_wind_field(wind)
```

### Dynamic Wind Changes

```python
def dynamic_wind_demo():
    """Demonstrate changing wind conditions during flight"""
    
    controller = DroneController()
    
    # Flight path through different wind conditions
    waypoints = [
        [0, 5, 0],      # Start in calm
        [20, 8, 10],    # Enter moderate wind
        [40, 12, 20],   # Strong wind area
        [0, 5, 0]       # Return to calm
    ]
    
    # Wind condition changes
    wind_changes = [
        (0, "calm"),
        (60, "moderate"),    # Change after 1 second
        (180, "stormy"),     # Change after 3 seconds
        (300, "calm")        # Calm down after 5 seconds
    ]
    
    dt = 0.016
    frame = 0
    waypoint_idx = 0
    change_idx = 0
    
    # Set initial target
    controller.set_target(waypoints[waypoint_idx])
    
    while waypoint_idx < len(waypoints):
        # Check for wind condition changes
        if (change_idx < len(wind_changes) and 
            frame >= wind_changes[change_idx][0]):
            
            condition = wind_changes[change_idx][1]
            if controller.wind_controller:
                controller.wind_controller.create_preset_wind_conditions(condition)
                print(f"Wind changed to: {condition}")
            change_idx += 1
        
        # Control drone
        result = controller.calculate_control(dt)
        
        if result['target_reached']:
            waypoint_idx += 1
            if waypoint_idx < len(waypoints):
                controller.set_target(waypoints[waypoint_idx])
                print(f"New target: {waypoints[waypoint_idx]}")
        
        frame += 1
        time.sleep(dt)

# Usage
dynamic_wind_demo()
```

---

## Advanced Wind Effects

### Tornado Simulation

```python
def tornado_encounter():
    """Simulate drone flying through tornado field"""
    
    controller = DroneController()
    
    if not controller.wind_controller:
        print("Wind controller not available")
        return
    
    # Add tornado zone
    controller.wind_controller.add_wind_zone("Tornado", [20, 5, 15], 20.0)
    tornado_zone = controller.wind_controller.wind_zones["Tornado"]
    
    # Configure tornado
    tornado_zone.tornado_enabled = True
    tornado_zone.tornado_center = np.array([20, 0, 15])
    tornado_zone.tornado_radius = 8.0
    tornado_zone.tornado_strength = 35.0
    tornado_zone.tornado_updraft = 25.0
    
    # Base wind conditions
    tornado_zone.set_wind_speed(12.0)
    tornado_zone.set_wind_direction([1, 0, 0])
    tornado_zone.set_turbulence_intensity(0.6)
    
    # Flight path through tornado area
    waypoints = [
        [0, 5, 15],     # Approach from west
        [10, 8, 15],    # Edge of tornado
        [20, 10, 15],   # Through tornado center
        [30, 8, 15],    # Exit tornado
        [40, 5, 15]     # Safe area
    ]
    
    print("Flying through tornado field...")
    
    dt = 0.016
    for waypoint in waypoints:
        controller.set_target(waypoint)
        
        while True:
            result = controller.calculate_control(dt)
            
            # Log extreme wind forces
            wind_magnitude = np.linalg.norm(result['wind_force'])
            if wind_magnitude > 20.0:
                pos = result['position']
                print(f"EXTREME WIND at [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}]: {wind_magnitude:.1f}N")
            
            if result['target_reached']:
                break
                
            time.sleep(dt)
    
    print("Tornado encounter complete!")

# Usage
tornado_encounter()
```

### Microburst Simulation

```python
def microburst_landing():
    """Simulate landing approach through microburst"""
    
    controller = DroneController()
    
    if not controller.wind_controller:
        print("Wind controller not available")
        return
    
    # Add microburst zone near landing area
    controller.wind_controller.add_wind_zone("Approach", [15, 8, 0], 15.0)
    zone = controller.wind_controller.wind_zones["Approach"]
    
    # Configure microburst
    zone.microburst_enabled = True
    zone.microburst_center = np.array([10, 5, 0])
    zone.microburst_radius = 8.0
    zone.microburst_strength = 20.0
    zone.microburst_duration = 3.0
    
    # Base conditions
    zone.set_wind_speed(8.0)
    zone.set_wind_direction([1, 0, 0])
    zone.set_turbulence_intensity(0.3)
    
    # Landing approach pattern
    waypoints = [
        [0, 15, 0],     # High approach
        [5, 12, 0],     # Descending
        [10, 8, 0],     # Through microburst
        [15, 5, 0],     # Final approach
        [20, 2, 0]      # Landing
    ]
    
    print("Landing approach through microburst...")
    
    dt = 0.016
    for i, waypoint in enumerate(waypoints):
        controller.set_target(waypoint)
        print(f"Approach phase {i+1}: Target {waypoint}")
        
        while True:
            result = controller.calculate_control(dt)
            
            # Monitor vertical forces during microburst
            if abs(result['wind_force'][1]) > 15.0:  # Strong vertical force
                pos = result['position']
                force_y = result['wind_force'][1]
                print(f"MICROBURST at [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}]: {force_y:.1f}N vertical")
            
            if result['target_reached']:
                break
                
            time.sleep(dt)
    
    print("Landing approach complete!")

# Usage
microburst_landing()
```

### Wind Shear Simulation

```python
def wind_shear_crossing():
    """Simulate crossing wind shear layers"""
    
    controller = DroneController()
    
    if not controller.wind_controller:
        print("Wind controller not available")
        return
    
    # Multiple zones for different altitudes
    zones = [
        ("LowLevel", [10, 3, 0], 25.0, [5.0, [1, 0, 0]]),      # Low altitude, east wind
        ("MidLevel", [10, 8, 0], 25.0, [10.0, [0.5, 0, 0.8]]), # Mid altitude, NE wind
        ("HighLevel", [10, 15, 0], 25.0, [15.0, [-0.8, 0, 0.6]]) # High altitude, NW wind
    ]
    
    for name, pos, size, (speed, direction) in zones:
        controller.wind_controller.add_wind_zone(name, pos, size)
        zone = controller.wind_controller.wind_zones[name]
        zone.set_wind_speed(speed)
        zone.set_wind_direction(direction)
        zone.set_turbulence_intensity(0.2)
    
    # Vertical climb through shear layers
    waypoints = [
        [10, 2, 0],     # Low level
        [10, 5, 0],     # Transition 1
        [10, 10, 0],    # Mid level
        [10, 13, 0],    # Transition 2
        [10, 18, 0],    # High level
        [10, 15, 0],    # Descent
        [10, 8, 0],     # Mid level return
        [10, 3, 0]      # Low level return
    ]
    
    print("Climbing through wind shear layers...")
    
    dt = 0.016
    for i, waypoint in enumerate(waypoints):
        controller.set_target(waypoint)
        altitude = waypoint[1]
        
        print(f"Phase {i+1}: Climbing to {altitude}m")
        
        while True:
            result = controller.calculate_control(dt)
            
            # Monitor wind direction changes
            wind_vec = result['wind_force']
            if np.linalg.norm(wind_vec) > 5.0:
                wind_dir = wind_vec / np.linalg.norm(wind_vec)
                print(f"Wind at {result['position'][1]:.1f}m: direction {wind_dir}")
            
            if result['target_reached']:
                break
                
            time.sleep(dt)
    
    print("Wind shear crossing complete!")

# Usage
wind_shear_crossing()
```

---

## Custom Flight Patterns

### Search Pattern

```python
def search_pattern(center=[0, 10, 0], size=20, spacing=4):
    """Fly a systematic search pattern"""
    
    controller = DroneController()
    
    # Generate grid search waypoints
    waypoints = [center]  # Start at center
    
    half_size = size // 2
    y = center[1]  # Maintain altitude
    
    # Create lawn-mower pattern
    for x_offset in range(-half_size, half_size + 1, spacing):
        if (x_offset // spacing) % 2 == 0:  # Even rows: south to north
            z_range = range(-half_size, half_size + 1, spacing)
        else:  # Odd rows: north to south
            z_range = range(half_size, -half_size - 1, -spacing)
        
        for z_offset in z_range:
            x = center[0] + x_offset
            z = center[2] + z_offset
            waypoints.append([x, y, z])
    
    print(f"Search pattern: {len(waypoints)} waypoints over {size}x{size}m area")
    
    dt = 0.016
    for i, waypoint in enumerate(waypoints):
        controller.set_target(waypoint)
        
        print(f"Search point {i+1}/{len(waypoints)}: {waypoint}")
        
        while True:
            result = controller.calculate_control(dt)
            if result['target_reached']:
                break
            time.sleep(dt)
    
    print("Search pattern complete!")

# Usage
search_pattern(center=[0, 8, 0], size=24, spacing=6)
```

### Figure-8 Pattern

```python
def figure_eight(center=[0, 8, 0], radius=10, num_points=24):
    """Fly a figure-8 pattern"""
    
    controller = DroneController()
    
    # Generate figure-8 waypoints
    waypoints = []
    for i in range(num_points + 1):
        t = 2 * np.pi * i / num_points
        
        # Parametric figure-8: x = a*sin(t), z = a*sin(t)*cos(t)
        x = center[0] + radius * np.sin(t)
        y = center[1]
        z = center[2] + radius * np.sin(t) * np.cos(t)
        
        waypoints.append([x, y, z])
    
    print(f"Flying figure-8 pattern with {num_points} waypoints")
    
    dt = 0.016
    for i, waypoint in enumerate(waypoints):
        controller.set_target(waypoint)
        
        while True:
            result = controller.calculate_control(dt)
            if result['target_reached']:
                break
            time.sleep(dt)
    
    print("Figure-8 pattern complete!")

# Usage
figure_eight(center=[0, 10, 0], radius=12, num_points=32)
```

### Obstacle Avoidance

```python
def obstacle_avoidance_demo():
    """Demonstrate basic obstacle avoidance"""
    
    controller = DroneController()
    
    # Define obstacles as [x, y, z, radius]
    obstacles = [
        [10, 8, 5, 3],   # Obstacle 1
        [20, 6, 15, 4],  # Obstacle 2
        [15, 12, 25, 2]  # Obstacle 3
    ]
    
    def check_collision(pos, obstacles, safety_margin=2.0):
        """Check if position collides with obstacles"""
        for obs in obstacles:
            obs_pos = np.array(obs[:3])
            obs_radius = obs[3] + safety_margin
            
            distance = np.linalg.norm(pos - obs_pos)
            if distance < obs_radius:
                return True, obs_pos
        return False, None
    
    def find_avoidance_point(current, target, obstacle_pos, radius=5.0):
        """Find point to avoid obstacle"""
        # Simple avoidance: go around obstacle
        to_obstacle = obstacle_pos - current
        to_target = target - current
        
        # Choose side based on cross product
        cross = np.cross(to_target[:2], to_obstacle[:2])  # 2D cross product
        side = 1 if cross > 0 else -1
        
        # Perpendicular direction
        perp = np.array([-to_obstacle[2], to_obstacle[1], to_obstacle[0]]) * side
        perp = perp / np.linalg.norm(perp) * radius
        
        avoidance_point = obstacle_pos + perp
        avoidance_point[1] = max(target[1], obstacle_pos[1] + 3)  # Stay above obstacle
        
        return avoidance_point
    
    # Original path
    original_waypoints = [
        [0, 5, 0],
        [30, 10, 30]
    ]
    
    # Process waypoints with obstacle avoidance
    waypoints = [original_waypoints[0]]
    
    for target in original_waypoints[1:]:
        current = waypoints[-1]
        
        # Check if direct path hits obstacle
        collision, obs_pos = check_collision(target, obstacles)
        
        if collision:
            print(f"Obstacle detected! Planning avoidance route...")
            avoidance = find_avoidance_point(current, target, obs_pos)
            waypoints.append(avoidance)
            print(f"Avoidance waypoint: {avoidance}")
        
        waypoints.append(target)
    
    print(f"Flight plan: {len(waypoints)} waypoints (including avoidance)")
    
    # Execute flight plan
    dt = 0.016
    for i, waypoint in enumerate(waypoints):
        controller.set_target(waypoint)
        print(f"Waypoint {i+1}/{len(waypoints)}: {waypoint}")
        
        while True:
            result = controller.calculate_control(dt)
            
            # Check for obstacle proximity during flight
            collision, _ = check_collision(result['position'], obstacles, safety_margin=1.0)
            if collision:
                print("WARNING: Close to obstacle!")
            
            if result['target_reached']:
                break
                
            time.sleep(dt)
    
    print("Obstacle avoidance flight complete!")

# Usage
obstacle_avoidance_demo()
```

---

## Data Analysis and Logging

### Flight Data Logger

```python
import json
import numpy as np
from datetime import datetime

class FlightDataLogger:
    """Log and analyze flight data"""
    
    def __init__(self, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flight_log_{timestamp}.json"
        
        self.filename = filename
        self.data = {
            'metadata': {
                'start_time': datetime.now().isoformat(),
                'version': '0.1.8'
            },
            'flight_data': []
        }
        
    def log_frame(self, time, controller_result, target, waypoint_index=None):
        """Log a single frame of flight data"""
        
        frame_data = {
            'time': time,
            'position': controller_result['position'].tolist(),
            'velocity': controller_result['velocity'].tolist(),
            'target': target,
            'distance_to_target': controller_result['distance'],
            'wind_force': controller_result['wind_force'].tolist(),
            'control_acceleration': controller_result['control_acceleration'].tolist(),
            'target_reached': controller_result['target_reached']
        }
        
        if waypoint_index is not None:
            frame_data['waypoint_index'] = waypoint_index
            
        self.data['flight_data'].append(frame_data)
    
    def save(self):
        """Save logged data to file"""
        self.data['metadata']['end_time'] = datetime.now().isoformat()
        self.data['metadata']['total_frames'] = len(self.data['flight_data'])
        
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        print(f"Flight data saved to {self.filename}")
    
    def analyze(self):
        """Perform basic flight analysis"""
        frames = self.data['flight_data']
        if not frames:
            return {}
        
        positions = np.array([f['position'] for f in frames])
        velocities = np.array([f['velocity'] for f in frames])
        wind_forces = np.array([f['wind_force'] for f in frames])
        
        # Calculate statistics
        speeds = np.linalg.norm(velocities, axis=1)
        wind_magnitudes = np.linalg.norm(wind_forces, axis=1)
        
        # Flight path analysis
        if len(positions) > 1:
            path_distances = np.linalg.norm(np.diff(positions, axis=0), axis=1)
            total_distance = np.sum(path_distances)
        else:
            total_distance = 0
        
        # Calculate direct distance
        if len(positions) > 0:
            direct_distance = np.linalg.norm(positions[-1] - positions[0])
            efficiency = direct_distance / max(total_distance, 1e-6)
        else:
            direct_distance = 0
            efficiency = 0
        
        analysis = {
            'flight_duration': len(frames) * 0.016,  # Assuming 60 FPS
            'total_distance_flown': total_distance,
            'direct_distance': direct_distance,
            'path_efficiency': efficiency,
            'average_speed': np.mean(speeds),
            'max_speed': np.max(speeds),
            'average_wind_force': np.mean(wind_magnitudes),
            'max_wind_force': np.max(wind_magnitudes),
            'altitude_range': [np.min(positions[:, 1]), np.max(positions[:, 1])],
            'final_position': positions[-1].tolist() if len(positions) > 0 else None
        }
        
        return analysis

def logged_flight_example():
    """Example flight with data logging"""
    
    controller = DroneController()
    logger = FlightDataLogger()
    
    # Set up wind conditions for interesting data
    if controller.wind_controller:
        controller.wind_controller.create_preset_wind_conditions("moderate")
    
    waypoints = [
        [0, 5, 0],
        [15, 8, 10],
        [30, 12, 5],
        [20, 6, -10],
        [0, 5, 0]
    ]
    
    dt = 0.016
    flight_time = 0
    waypoint_index = 0
    
    print("Starting logged flight...")
    
    # Execute flight with logging
    for waypoint in waypoints:
        controller.set_target(waypoint)
        
        while True:
            result = controller.calculate_control(dt)
            
            # Log this frame
            logger.log_frame(flight_time, result, waypoint, waypoint_index)
            
            if result['target_reached']:
                waypoint_index += 1
                break
            
            flight_time += dt
            time.sleep(dt)
    
    # Save and analyze
    logger.save()
    analysis = logger.analyze()
    
    print("\n=== Flight Analysis ===")
    for key, value in analysis.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")

# Usage
logged_flight_example()
```

### Wind Effect Analysis

```python
def wind_effect_analysis():
    """Analyze how different wind conditions affect flight performance"""
    
    # Test flight path
    test_waypoints = [
        [0, 5, 0],
        [20, 8, 15],
        [0, 5, 0]
    ]
    
    wind_conditions = ["calm", "moderate", "stormy", "turbulent"]
    results = {}
    
    for condition in wind_conditions:
        print(f"\nTesting wind condition: {condition}")
        
        controller = DroneController()
        logger = FlightDataLogger(f"wind_test_{condition}.json")
        
        # Apply wind condition
        if controller.wind_controller:
            controller.wind_controller.create_preset_wind_conditions(condition)
        
        # Fly test pattern
        dt = 0.016
        flight_time = 0
        
        for waypoint in test_waypoints:
            controller.set_target(waypoint)
            
            while True:
                result = controller.calculate_control(dt)
                logger.log_frame(flight_time, result, waypoint)
                
                if result['target_reached']:
                    break
                
                flight_time += dt
                time.sleep(dt / 10)  # Speed up for testing
        
        # Analyze results
        logger.save()
        analysis = logger.analyze()
        results[condition] = analysis
        
        print(f"Duration: {analysis['flight_duration']:.1f}s")
        print(f"Distance: {analysis['total_distance_flown']:.1f}m")
        print(f"Efficiency: {analysis['path_efficiency']:.2f}")
        print(f"Max wind: {analysis['max_wind_force']:.1f}N")
    
    # Compare results
    print("\n=== Wind Condition Comparison ===")
    print("Condition\tDuration\tDistance\tEfficiency\tMax Wind")
    print("-" * 60)
    
    for condition, data in results.items():
        print(f"{condition:10s}\t{data['flight_duration']:6.1f}s\t"
              f"{data['total_distance_flown']:6.1f}m\t"
              f"{data['path_efficiency']:8.2f}\t"
              f"{data['max_wind_force']:6.1f}N")

# Usage
wind_effect_analysis()
```

---

## Performance Optimization

### Efficient Wind Field Queries

```python
class OptimizedWindController:
    """Optimized wind controller with caching"""
    
    def __init__(self, base_controller):
        self.base_controller = base_controller
        self.cache = {}
        self.cache_size = 1000
        self.cache_tolerance = 0.5  # Cache hits within 0.5m
        
    def get_wind_at_position(self, position):
        """Get wind with spatial caching"""
        
        # Check cache for nearby positions
        pos_key = tuple(np.round(position / self.cache_tolerance) * self.cache_tolerance)
        
        if pos_key in self.cache:
            return self.cache[pos_key].copy()
        
        # Calculate wind
        wind = self.base_controller.get_wind_at_position(position)
        
        # Cache result
        if len(self.cache) >= self.cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[pos_key] = wind.copy()
        return wind

def performance_test():
    """Compare performance of optimized vs standard wind controller"""
    
    import time
    
    # Create controllers
    base_controller = WindController()
    base_controller.add_wind_zone("Test", [0, 10, 0], 20.0)
    base_controller.create_preset_wind_conditions("moderate")
    
    optimized_controller = OptimizedWindController(base_controller)
    
    # Test positions
    test_positions = []
    for i in range(1000):
        x = np.random.uniform(-25, 25)
        y = np.random.uniform(5, 15)
        z = np.random.uniform(-25, 25)
        test_positions.append([x, y, z])
    
    # Test standard controller
    start_time = time.time()
    for pos in test_positions:
        wind = base_controller.get_wind_at_position(pos)
    standard_time = time.time() - start_time
    
    # Test optimized controller
    start_time = time.time()
    for pos in test_positions:
        wind = optimized_controller.get_wind_at_position(pos)
    optimized_time = time.time() - start_time
    
    print(f"Standard controller: {standard_time:.3f}s")
    print(f"Optimized controller: {optimized_time:.3f}s")
    print(f"Speedup: {standard_time/optimized_time:.1f}x")

# Usage
performance_test()
```

### Batch Wind Calculations

```python
def batch_wind_calculation(wind_controller, positions):
    """Calculate wind at multiple positions efficiently"""
    
    # Convert to numpy array
    positions = np.array(positions)
    winds = np.zeros_like(positions)
    
    # Process in batches to minimize function call overhead
    batch_size = 100
    for i in range(0, len(positions), batch_size):
        batch = positions[i:i+batch_size]
        
        for j, pos in enumerate(batch):
            winds[i+j] = wind_controller.get_wind_at_position(pos)
    
    return winds

# Example usage
def efficient_path_planning():
    """Efficiently calculate wind effects along planned path"""
    
    controller = DroneController()
    
    if not controller.wind_controller:
        print("Wind controller not available")
        return
    
    # Generate detailed path
    start = np.array([0, 5, 0])
    end = np.array([30, 12, 20])
    num_points = 100
    
    # Linear interpolation
    path_points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        point = start + t * (end - start)
        path_points.append(point)
    
    # Batch calculate winds
    winds = batch_wind_calculation(controller.wind_controller, path_points)
    
    # Analyze path
    wind_magnitudes = np.linalg.norm(winds, axis=1)
    max_wind_idx = np.argmax(wind_magnitudes)
    
    print(f"Path analysis:")
    print(f"  Total points: {len(path_points)}")
    print(f"  Average wind: {np.mean(wind_magnitudes):.1f} m/s")
    print(f"  Maximum wind: {wind_magnitudes[max_wind_idx]:.1f} m/s at {path_points[max_wind_idx]}")
    
    # Find optimal path considering wind
    # (This is a simplified example - real path optimization would be more complex)
    high_wind_points = np.where(wind_magnitudes > np.mean(wind_magnitudes) + np.std(wind_magnitudes))[0]
    
    if len(high_wind_points) > 0:
        print(f"  High wind areas detected at {len(high_wind_points)} points")
        print(f"  Consider path adjustment around points: {high_wind_points[:5]}...")

# Usage
efficient_path_planning()
```

---

## Troubleshooting

### Common Issues and Solutions

```python
def diagnostic_check():
    """Run diagnostic checks for common issues"""
    
    print("ZephyrSim Diagnostic Check")
    print("=" * 30)
    
    # Check 1: Isaac Sim availability
    try:
        import omni.isaac.core.utils.stage as stage_utils
        print("✅ Isaac Sim modules available")
        isaac_available = True
    except ImportError as e:
        print("❌ Isaac Sim modules not available")
        print(f"   Error: {e}")
        print("   Solution: Run within Isaac Sim environment or use standalone mode")
        isaac_available = False
    
    # Check 2: Wind controller
    try:
        from scripts.wind_controller import WindController
        wind = WindController()
        print("✅ Wind controller available")
        wind_available = True
    except ImportError as e:
        print("❌ Wind controller not available")
        print(f"   Error: {e}")
        print("   Solution: Check scripts directory and imports")
        wind_available = False
    
    # Check 3: NumPy
    try:
        import numpy as np
        print("✅ NumPy available")
    except ImportError:
        print("❌ NumPy not available")
        print("   Solution: pip install numpy")
    
    # Check 4: Noise library (optional)
    try:
        from noise import pnoise3
        print("✅ Noise library available (enhanced turbulence)")
    except ImportError:
        print("⚠️  Noise library not available (basic turbulence only)")
        print("   Solution: pip install noise")
    
    # Check 5: Basic controller functionality
    if wind_available:
        try:
            from scripts.fly_to_waypoints import DroneController
            controller = DroneController()
            result = controller.calculate_control(0.016)
            print("✅ Basic controller functionality working")
        except Exception as e:
            print("❌ Controller functionality issue")
            print(f"   Error: {e}")
    
    # Check 6: File structure
    import os
    required_files = [
        'scripts/fly_to_waypoints.py',
        'scripts/wind_controller.py',
        'scripts/wind_tuning.py',
        'main_stage.usd'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if not missing_files:
        print("✅ All required files present")
    else:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
    
    print("\nDiagnostic complete!")
    
    return {
        'isaac_sim': isaac_available,
        'wind_controller': wind_available,
        'missing_files': missing_files
    }

def safe_controller_creation():
    """Safely create controller with fallbacks"""
    
    try:
        from scripts.fly_to_waypoints import DroneController
        controller = DroneController()
        
        # Test basic functionality
        test_result = controller.calculate_control(0.016)
        
        return controller, "Full functionality available"
        
    except ImportError as e:
        print(f"Import error: {e}")
        
        # Try minimal implementation
        class MinimalDroneController:
            def __init__(self):
                self.current_position = np.array([0, 5, 0])
                self.current_velocity = np.array([0, 0, 0])
                self.target_position = np.array([0, 5, 0])
                self.max_velocity = 5.0
                self.max_acceleration = 2.0
                
            def set_target(self, target):
                self.target_position = np.array(target)
                
            def calculate_control(self, dt):
                # Simple proportional control without wind
                error = self.target_position - self.current_position
                distance = np.linalg.norm(error)
                
                if distance > 0.5:
                    desired_vel = error * 2.0
                    vel_mag = np.linalg.norm(desired_vel)
                    if vel_mag > self.max_velocity:
                        desired_vel *= self.max_velocity / vel_mag
                    
                    self.current_velocity = desired_vel
                    self.current_position += self.current_velocity * dt
                    
                    return {
                        'position': self.current_position.copy(),
                        'velocity': self.current_velocity.copy(),
                        'target_reached': False,
                        'distance': distance,
                        'wind_force': np.zeros(3),
                        'control_acceleration': np.zeros(3)
                    }
                else:
                    return {
                        'position': self.current_position.copy(),
                        'velocity': np.zeros(3),
                        'target_reached': True,
                        'distance': distance,
                        'wind_force': np.zeros(3),
                        'control_acceleration': np.zeros(3)
                    }
        
        return MinimalDroneController(), "Minimal functionality (no wind effects)"
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, "Controller creation failed"

# Usage examples
if __name__ == "__main__":
    # Run diagnostics
    diagnostic_results = diagnostic_check()
    
    # Safe controller creation
    controller, status = safe_controller_creation()
    if controller:
        print(f"\nController created: {status}")
        
        # Test basic flight
        controller.set_target([5, 8, 3])
        for i in range(100):
            result = controller.calculate_control(0.016)
            if result['target_reached']:
                print("Test flight successful!")
                break
    else:
        print("Failed to create controller")
```

---

This usage guide provides comprehensive examples for all aspects of ZephyrSim. Start with the Quick Start section and progress through the examples based on your needs. Each example is self-contained and can be run independently.