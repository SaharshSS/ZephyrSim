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

class DroneController:
    """Simple drone controller for waypoint navigation"""
    
    def __init__(self, drone_prim_path="/World/Drone"):
        self.drone_prim_path = drone_prim_path
        self.current_position = np.array([0.0, 5.0, 0.0])
        self.current_velocity = np.array([0.0, 0.0, 0.0])
        self.target_position = np.array([0.0, 5.0, 0.0])
        self.max_velocity = 5.0  # m/s
        self.max_acceleration = 2.0  # m/s²
        self.position_tolerance = 0.5  # meters
        self.velocity_tolerance = 0.1  # m/s
        
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
        
    def calculate_control(self, dt):
        """Calculate control inputs for waypoint navigation"""
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
            acceleration = velocity_error * 5.0  # Proportional gain for velocity
            
            # Limit acceleration
            acc_magnitude = np.linalg.norm(acceleration)
            if acc_magnitude > self.max_acceleration:
                acceleration = acceleration * (self.max_acceleration / acc_magnitude)
                
            # Update velocity
            self.current_velocity += acceleration * dt
            
            # Update position
            self.current_position += self.current_velocity * dt
            
            return {
                'position': self.current_position,
                'velocity': self.current_velocity,
                'target_reached': False,
                'distance': distance
            }
        else:
            # Target reached, stop
            self.current_velocity = np.zeros(3)
            return {
                'position': self.current_position,
                'velocity': self.current_velocity,
                'target_reached': True,
                'distance': distance
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

def print_status(waypoint_index, total_waypoints, position, distance, velocity):
    """Print formatted status information"""
    print(f"📍 Waypoint {waypoint_index + 1}/{total_waypoints}")
    print(f"   Position: [{position[0]:6.2f}, {position[1]:6.2f}, {position[2]:6.2f}]")
    print(f"   Distance: {distance:6.2f}m")
    print(f"   Velocity: [{velocity[0]:6.2f}, {velocity[1]:6.2f}, {velocity[2]:6.2f}] m/s")

def main():
    """Main function to run waypoint navigation"""
    print("🌬️ ZephyrSim - Fly to Waypoints")
    print("=" * 50)
    
    # Define waypoints (x, y, z) in meters
    waypoints = [
        [0, 5, 0],      # Start position
        [10, 8, 5],     # Waypoint 1
        [20, 10, 10],   # Waypoint 2
        [15, 15, 15],   # Waypoint 3
        [5, 12, 8],     # Waypoint 4
        [0, 5, 0]       # Return to start
    ]
    
    # Initialize drone controller
    controller = DroneController()
    
    # Simulation parameters
    dt = 0.016  # 60 FPS
    waypoint_index = 0
    waypoint_reached = True
    frame_count = 0
    
    print(f"🚁 Starting navigation with {len(waypoints)} waypoints")
    print(f"🎯 Initial position: {waypoints[0]}")
    print(f"⚙️  Simulation mode: {'Isaac Sim' if ISAAC_SIM_AVAILABLE else 'Standalone'}")
    print("-" * 50)
    
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
                           control_result['velocity'])
            
            # Simulate time step
            time.sleep(dt)
            
    except KeyboardInterrupt:
        print("\n🛑 Navigation interrupted by user")
    except Exception as e:
        print(f"❌ Error during navigation: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🏁 Navigation complete!")
    print("=" * 50)

if __name__ == "__main__":
    main() 