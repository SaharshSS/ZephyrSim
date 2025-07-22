#!/usr/bin/env python3
"""
ZephyrSim - Fly to Waypoints Script
Controls a drone to fly between predefined waypoints in Isaac Sim
"""

import numpy as np
import time
import math
import sys


# Try to import Isaac Sim modules, with fallbacks
try:
    import omni.isaac.core.utils.stage as stage_utils
    import omni.isaac.core.utils.prims as prim_utils
    from omni.isaac.core.robots import Robot
    import omni.usd
    from pxr import Gf
    ISAAC_SIM_AVAILABLE = True
    print("✅ Isaac Sim modules loaded successfully")
except ImportError as e:
    print(f"⚠️  Isaac Sim not available: {e}")
    print("Running in simulation mode only")
    ISAAC_SIM_AVAILABLE = False

# Import wind controller
try:
    from scripts.wind_controller import WindController
    from scripts.wind_tuning import tune_wind
    WIND_CONTROLLER_AVAILABLE = True
    print("✅ Wind controller loaded successfully")
except ImportError as e:
    print(f"⚠️  Wind controller not available: {e}")
    WIND_CONTROLLER_AVAILABLE = False

class DroneController:
    """Simple drone controller for waypoint navigation with wind effects"""
    
    def __init__(self, drone_prim_path="/World/Drone"):
        self.drone_prim_path = drone_prim_path
        self.current_position = np.array([0.0, 5.0, 0.0])
        self.current_velocity = np.array([0.0, 0.0, 0.0])
        self.target_position = np.array([0.0, 5.0, 0.0])
        self.max_velocity = 5.0  # m/s
        self.max_acceleration = 2.0  # m/s²
        self.position_tolerance = 0.5  # meters
        self.velocity_tolerance = 0.1  # m/s
        
        # Drone physics properties
        self.mass = 1.5  # kg
        self.drag_coefficient = 0.3
        self.cross_sectional_area = 0.1  # m²
        self.air_density = 1.225  # kg/m³
        
        # Wind controller
        self.wind_controller = None
        if WIND_CONTROLLER_AVAILABLE:
            self.wind_controller = WindController()
            # Add wind zones (matching main_stage.usd)
            self.wind_controller.add_wind_zone("WindZone1", [20, 10, 0], 10.0)
            self.wind_controller.add_wind_zone("WindZone2", [-15, 15, 30], 12.0)
            print("🌪️ Wind zones initialized")
        
    def set_target(self, target_position):
        """Set the target waypoint position"""
        self.target_position = np.array(target_position)
        print(f"🎯 Target set to: {self.target_position}")
        
    def get_current_position(self):
        """Get current drone position from stage or simulation"""
        if ISAAC_SIM_AVAILABLE:
            try:
                drone_prim = prim_utils.get_prim_at_path(self.drone_prim_path)
                if drone_prim:
                    # Get world transform
                    world_transform = omni.usd.get_world_transform_matrix(drone_prim)
                    position = world_transform.ExtractTranslation()
                    self.current_position = np.array([position[0], position[1], position[2]])
            except Exception as e:
                print(f"⚠️  Error getting drone position from stage: {e}")
                print("Using simulated position")
        
        return self.current_position.copy()
        
    def calculate_wind_force(self, position, velocity):
        """Calculate wind force on the drone"""
        if not self.wind_controller:
            return np.zeros(3)
            
        # Get wind vector at drone position
        wind_velocity = self.wind_controller.get_wind_at_position(position)
        
        # Calculate relative velocity (drone velocity - wind velocity)
        relative_velocity = velocity - wind_velocity
        
        # Calculate drag force
        relative_speed = np.linalg.norm(relative_velocity)
        if relative_speed > 0:
            drag_force = -0.5 * self.air_density * self.drag_coefficient * self.cross_sectional_area * relative_speed * relative_velocity
        else:
            drag_force = np.zeros(3)
            
        # Add wind force (simplified)
        wind_force = wind_velocity * self.mass * 0.1  # Wind affects drone like a force
        
        return drag_force + wind_force
        
    def calculate_control(self, dt):
        """Calculate control inputs for waypoint navigation with wind effects"""
        current_pos = self.get_current_position()
        position_error = self.target_position - current_pos
        distance = np.linalg.norm(position_error)
        
        # Simple proportional control
        if distance > self.position_tolerance:
            # Calculate desired velocity (proportional to error)
            desired_velocity = position_error * 2.0  # Proportional gain
            
            # Limit velocity
            velocity_magnitude = np.linalg.norm(desired_velocity)
            if velocity_magnitude > self.max_velocity:
                desired_velocity = desired_velocity * (self.max_velocity / velocity_magnitude)
                
            # Calculate acceleration
            velocity_error = desired_velocity - self.current_velocity
            control_acceleration = velocity_error * 5.0  # Proportional gain for velocity
            
            # Calculate wind forces
            wind_force = self.calculate_wind_force(current_pos, self.current_velocity)
            wind_acceleration = wind_force / self.mass
            
            # Combine control and wind accelerations
            total_acceleration = control_acceleration + wind_acceleration
            
            # Limit total acceleration
            acc_magnitude = np.linalg.norm(total_acceleration)
            if acc_magnitude > self.max_acceleration:
                total_acceleration = total_acceleration * (self.max_acceleration / acc_magnitude)
                
            # Update velocity
            self.current_velocity += total_acceleration * dt
            
            # Update position
            self.current_position += self.current_velocity * dt
            
            # Update wind controller
            if self.wind_controller:
                self.wind_controller.update()
            
            return {
                'position': self.current_position,
                'velocity': self.current_velocity,
                'target_reached': False,
                'distance': distance,
                'wind_force': wind_force,
                'control_acceleration': control_acceleration
            }
        else:
            # Target reached, stop
            self.current_velocity = np.zeros(3)
            return {
                'position': self.current_position,
                'velocity': self.current_velocity,
                'target_reached': True,
                'distance': distance,
                'wind_force': np.zeros(3),
                'control_acceleration': np.zeros(3)
            }
    
    def update_drone_position(self, new_position):
        """Update drone position in the stage or simulation"""
        self.current_position = np.array(new_position)
        
        if ISAAC_SIM_AVAILABLE:
            try:
                drone_prim = prim_utils.get_prim_at_path(self.drone_prim_path)
                if drone_prim:
                    # Set world transform
                    transform = Gf.Matrix4d()
                    transform.SetTranslate(Gf.Vec3d(new_position[0], new_position[1], new_position[2]))
                    omni.usd.set_world_transform_matrix(drone_prim, transform)
            except Exception as e:
                print(f"⚠️  Error updating drone position in stage: {e}")

def print_status(waypoint_index, total_waypoints, position, distance, velocity, wind_force, control_acc):
    """Print formatted status information"""
    print(f"📍 Waypoint {waypoint_index + 1}/{total_waypoints}")
    print(f"   Position: [{position[0]:6.2f}, {position[1]:6.2f}, {position[2]:6.2f}]")
    print(f"   Distance: {distance:6.2f}m")
    print(f"   Velocity: [{velocity[0]:6.2f}, {velocity[1]:6.2f}, {velocity[2]:6.2f}] m/s")
    print(f"   Wind Force: [{wind_force[0]:6.2f}, {wind_force[1]:6.2f}, {wind_force[2]:6.2f}] N")
    print(f"   Control Acc: [{control_acc[0]:6.2f}, {control_acc[1]:6.2f}, {control_acc[2]:6.2f}] m/s²")

def main():
    """Main function to run waypoint navigation with wind effects"""
    print("🌬️ ZephyrSim - Fly to Waypoints (with Wind Effects)")
    print("=" * 60)
    
    # Define waypoints (x, y, z) in meters
    waypoints = [
        [0, 5, 0],      # Start position
        [10, 8, 5],     # Waypoint 1
        [20, 10, 10],   # Waypoint 2 (in wind zone)
        [15, 15, 15],   # Waypoint 3
        [5, 12, 8],     # Waypoint 4
        [0, 5, 0]       # Return to start
    ]
    
    # Initialize drone controller
    controller = DroneController()
    
    # Set up wind conditions if available
    if controller.wind_controller:
        print("\n🌪️ Setting up wind conditions...")
        controller.wind_controller.create_preset_wind_conditions("moderate")
        print("✅ Moderate wind conditions applied")
    
    # Call wind tuning function
    if controller.wind_controller:
        tune_wind(controller.wind_controller)
        print("✅ Wind tuning applied")
    
    # Simulation parameters
    dt = 0.016  # 60 FPS
    waypoint_index = 0
    waypoint_reached = True
    frame_count = 0
    
    print(f"🚁 Starting navigation with {len(waypoints)} waypoints")
    print(f"🎯 Initial position: {waypoints[0]}")
    print(f"⚙️  Simulation mode: {'Isaac Sim' if ISAAC_SIM_AVAILABLE else 'Standalone'}")
    print(f"🌪️  Wind effects: {'Enabled' if WIND_CONTROLLER_AVAILABLE else 'Disabled'}")
    print("-" * 60)
    
    # Main simulation loop
    try:
        while waypoint_index < len(waypoints):
            # Set target if we've reached the current waypoint
            if waypoint_reached:
                target = waypoints[waypoint_index]
                controller.set_target(target)
                print(f"\n🛫 Flying to waypoint {waypoint_index + 1}: {target}")
                waypoint_reached = False
            
            # Calculate control
            control_result = controller.calculate_control(dt)
            
            # Update drone position in stage
            controller.update_drone_position(control_result['position'])
            
            # Check if waypoint reached
            if control_result['target_reached']:
                waypoint_reached = True
                waypoint_index += 1
                print(f"\n✅ Reached waypoint {waypoint_index}! Distance: {control_result['distance']:.2f}m")
                
                if waypoint_index < len(waypoints):
                    print(f"🎯 Next waypoint: {waypoints[waypoint_index]}")
                else:
                    print("🎉 All waypoints completed!")
            
            # Print status every 60 frames (1 second at 60 FPS)
            frame_count += 1
            if frame_count % 60 == 0:
                print_status(waypoint_index, len(waypoints), 
                           control_result['position'], 
                           control_result['distance'],
                           control_result['velocity'],
                           control_result['wind_force'],
                           control_result['control_acceleration'])
            
            # Simulate time step
            time.sleep(dt)
            
    except KeyboardInterrupt:
        print("\n🛑 Navigation interrupted by user")
    except Exception as e:
        print(f"❌ Error during navigation: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🏁 Navigation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main() 