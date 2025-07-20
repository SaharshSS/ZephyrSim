#!/usr/bin/env python3
"""
ZephyrSim - Wind Controller Script
Controls wind zones with flight simulator-like capabilities
"""

import numpy as np
import time
import math
import random
import sys

# Try to import Isaac Sim modules, with fallbacks
try:
    import omni.isaac.core.utils.stage as stage_utils
    import omni.isaac.core.utils.prims as prim_utils
    import omni.usd
    from pxr import Gf, Usd, UsdGeom
    ISAAC_SIM_AVAILABLE = True
    print("✅ Isaac Sim modules loaded successfully")
except ImportError as e:
    print(f"⚠️  Isaac Sim not available: {e}")
    print("Running in simulation mode only")
    ISAAC_SIM_AVAILABLE = False

class WindZone:
    """Represents a wind zone with configurable parameters"""
    
    def __init__(self, zone_name, position, size=10.0):
        self.zone_name = zone_name
        self.position = np.array(position)
        self.size = size
        
        # Wind parameters
        self.wind_speed = 5.0  # m/s
        self.wind_direction = np.array([1.0, 0.0, 0.0])  # Normalized direction
        self.turbulence_intensity = 0.1  # 0-1 scale
        self.wind_gust_frequency = 0.5  # Hz
        self.wind_gust_amplitude = 2.0  # m/s
        self.wind_gust_duration = 2.0  # seconds
        
        # Time tracking
        self.time = 0.0
        self.last_gust_time = 0.0
        self.gust_active = False
        self.gust_start_time = 0.0
        
        # Turbulence parameters
        self.turbulence_scale = 1.0
        self.turbulence_time = 0.0
        
    def set_wind_speed(self, speed):
        """Set wind speed in m/s"""
        self.wind_speed = max(0.0, speed)
        print(f"🌪️ {self.zone_name}: Wind speed set to {self.wind_speed} m/s")
        
    def set_wind_direction(self, direction):
        """Set wind direction as normalized vector"""
        direction = np.array(direction)
        magnitude = np.linalg.norm(direction)
        if magnitude > 0:
            self.wind_direction = direction / magnitude
            print(f"🧭 {self.zone_name}: Wind direction set to {self.wind_direction}")
        else:
            print(f"⚠️ {self.zone_name}: Invalid wind direction vector")
            
    def set_turbulence_intensity(self, intensity):
        """Set turbulence intensity (0-1)"""
        self.turbulence_intensity = max(0.0, min(1.0, intensity))
        print(f"🌀 {self.zone_name}: Turbulence intensity set to {self.turbulence_intensity}")
        
    def set_wind_gusts(self, frequency, amplitude, duration):
        """Set wind gust parameters"""
        self.wind_gust_frequency = max(0.0, frequency)
        self.wind_gust_amplitude = max(0.0, amplitude)
        self.wind_gust_duration = max(0.1, duration)
        print(f"💨 {self.zone_name}: Gusts set to {frequency}Hz, {amplitude}m/s, {duration}s")
        
    def get_wind_vector_at_position(self, position, dt):
        """Get wind vector at a specific position"""
        # Check if position is within wind zone
        distance = np.linalg.norm(position - self.position)
        if distance > self.size:
            return np.zeros(3)
            
        # Update time
        self.time += dt
        self.turbulence_time += dt
        
        # Base wind vector
        base_wind = self.wind_direction * self.wind_speed
        
        # Add gusts
        gust_wind = self._calculate_gusts(dt)
        
        # Add turbulence
        turbulence_wind = self._calculate_turbulence(position, dt)
        
        # Combine all wind components
        total_wind = base_wind + gust_wind + turbulence_wind
        
        # Apply distance falloff (wind decreases at zone edges)
        falloff = 1.0 - (distance / self.size) ** 2
        falloff = max(0.0, falloff)
        
        return total_wind * falloff
        
    def _calculate_gusts(self, dt):
        """Calculate wind gust component"""
        if self.wind_gust_amplitude <= 0:
            return np.zeros(3)
            
        # Check if it's time for a new gust
        if not self.gust_active and (self.time - self.last_gust_time) > (1.0 / self.wind_gust_frequency):
            self.gust_active = True
            self.gust_start_time = self.time
            self.last_gust_time = self.time
            
        # Calculate gust strength
        gust_strength = 0.0
        if self.gust_active:
            gust_age = self.time - self.gust_start_time
            if gust_age < self.wind_gust_duration:
                # Gust envelope: quick rise, slow decay
                if gust_age < 0.2:
                    gust_strength = gust_age / 0.2  # Rise
                else:
                    gust_strength = 1.0 - ((gust_age - 0.2) / (self.wind_gust_duration - 0.2))  # Decay
                gust_strength = max(0.0, gust_strength)
            else:
                self.gust_active = False
                
        return self.wind_direction * self.wind_gust_amplitude * gust_strength
        
    def _calculate_turbulence(self, position, dt):
        """Calculate turbulence component using Perlin-like noise"""
        if self.turbulence_intensity <= 0:
            return np.zeros(3)
            
        # Simple turbulence using sine waves at different frequencies
        x_turb = (math.sin(self.turbulence_time * 2.1) * 0.5 + 
                  math.sin(self.turbulence_time * 3.7) * 0.3 + 
                  math.sin(self.turbulence_time * 5.3) * 0.2)
                  
        y_turb = (math.sin(self.turbulence_time * 1.9) * 0.5 + 
                  math.sin(self.turbulence_time * 4.1) * 0.3 + 
                  math.sin(self.turbulence_time * 6.7) * 0.2)
                  
        z_turb = (math.sin(self.turbulence_time * 2.7) * 0.5 + 
                  math.sin(self.turbulence_time * 3.3) * 0.3 + 
                  math.sin(self.turbulence_time * 4.9) * 0.2)
                  
        turbulence = np.array([x_turb, y_turb, z_turb]) * self.turbulence_intensity * self.wind_speed
        
        return turbulence
        
    def update_visual_indicators(self):
        """Update visual indicators in the stage"""
        if not ISAAC_SIM_AVAILABLE:
            return
            
        try:
            # Update wind direction arrow
            wind_prim_path = f"/World/{self.zone_name}/WindDirection"
            wind_prim = prim_utils.get_prim_at_path(wind_prim_path)
            if wind_prim:
                # Calculate rotation to point in wind direction
                forward = np.array([1.0, 0.0, 0.0])
                rotation = self._vector_to_rotation(forward, self.wind_direction)
                
                # Apply rotation
                from pxr import Gf
                transform = Gf.Matrix4d()
                transform.SetRotate(Gf.Rotation(Gf.Vec3d(0, 0, 1), rotation[2]))
                transform.SetRotateOnly(Gf.Rotation(Gf.Vec3d(0, 1, 0), rotation[1]) * transform.GetRotation())
                transform.SetRotateOnly(Gf.Rotation(Gf.Vec3d(1, 0, 0), rotation[0]) * transform.GetRotation())
                
                omni.usd.set_world_transform_matrix(wind_prim, transform)
                
            # Update speed indicator
            speed_prim_path = f"/World/{self.zone_name}/WindSpeedIndicator/SpeedIndicator"
            speed_prim = prim_utils.get_prim_at_path(speed_prim_path)
            if speed_prim:
                # Move indicator based on wind speed (0-20 m/s range)
                speed_ratio = min(1.0, self.wind_speed / 20.0)
                indicator_y = speed_ratio * 2.0 - 1.0  # -1 to 1 range
                
                from pxr import Gf
                transform = Gf.Matrix4d()
                transform.SetTranslate(Gf.Vec3d(0, indicator_y, 0))
                omni.usd.set_world_transform_matrix(speed_prim, transform)
                
            # Update turbulence indicator
            turb_prim_path = f"/World/{self.zone_name}/TurbulenceIndicator/TurbulenceSphere"
            turb_prim = prim_utils.get_prim_at_path(turb_prim_path)
            if turb_prim:
                # Scale based on turbulence intensity
                scale = 0.5 + self.turbulence_intensity * 0.5
                
                from pxr import Gf
                transform = Gf.Matrix4d()
                transform.SetScale(Gf.Vec3d(scale, scale, scale))
                omni.usd.set_world_transform_matrix(turb_prim, transform)
                
        except Exception as e:
            print(f"⚠️ Error updating visual indicators: {e}")
            
    def _vector_to_rotation(self, v1, v2):
        """Convert direction vector to rotation angles"""
        # Normalize vectors
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        # Calculate rotation axis and angle
        cross = np.cross(v1, v2)
        dot = np.dot(v1, v2)
        
        if np.linalg.norm(cross) < 1e-6:
            if dot > 0:
                return [0, 0, 0]  # Same direction
            else:
                return [0, 0, np.pi]  # Opposite direction
                
        axis = cross / np.linalg.norm(cross)
        angle = math.acos(np.clip(dot, -1, 1))
        
        # Convert to Euler angles (simplified)
        return [angle * axis[0], angle * axis[1], angle * axis[2]]

class WindController:
    """Main wind controller managing multiple wind zones"""
    
    def __init__(self):
        self.wind_zones = {}
        self.time = 0.0
        self.dt = 0.016  # 60 FPS
        
    def add_wind_zone(self, zone_name, position, size=10.0):
        """Add a new wind zone"""
        self.wind_zones[zone_name] = WindZone(zone_name, position, size)
        print(f"🌪️ Added wind zone: {zone_name} at {position}")
        
    def get_wind_at_position(self, position):
        """Get total wind vector at a position from all zones"""
        total_wind = np.zeros(3)
        
        for zone in self.wind_zones.values():
            wind = zone.get_wind_vector_at_position(position, self.dt)
            total_wind += wind
            
        return total_wind
        
    def update(self):
        """Update all wind zones"""
        self.time += self.dt
        
        for zone in self.wind_zones.values():
            zone.update_visual_indicators()
            
    def create_preset_wind_conditions(self, preset_name):
        """Create preset wind conditions"""
        if preset_name == "calm":
            for zone in self.wind_zones.values():
                zone.set_wind_speed(2.0)
                zone.set_turbulence_intensity(0.05)
                zone.set_wind_gusts(0.1, 1.0, 1.0)
                
        elif preset_name == "moderate":
            for zone in self.wind_zones.values():
                zone.set_wind_speed(8.0)
                zone.set_turbulence_intensity(0.2)
                zone.set_wind_gusts(0.3, 3.0, 2.0)
                
        elif preset_name == "stormy":
            for zone in self.wind_zones.values():
                zone.set_wind_speed(15.0)
                zone.set_turbulence_intensity(0.6)
                zone.set_wind_gusts(0.8, 8.0, 3.0)
                
        elif preset_name == "turbulent":
            for zone in self.wind_zones.values():
                zone.set_wind_speed(6.0)
                zone.set_turbulence_intensity(0.8)
                zone.set_wind_gusts(1.2, 5.0, 1.5)
                
        print(f"🌪️ Applied {preset_name} wind conditions")

def main():
    """Main function to demonstrate wind controller"""
    print("🌪️ ZephyrSim - Wind Controller")
    print("=" * 50)
    
    # Initialize wind controller
    controller = WindController()
    
    # Add wind zones (matching the ones in main_stage.usd)
    controller.add_wind_zone("WindZone1", [20, 10, 0], 10.0)
    controller.add_wind_zone("WindZone2", [-15, 15, 30], 12.0)
    
    # Set up different wind conditions
    print("\n🎮 Wind Control Demo:")
    print("1. Calm conditions")
    print("2. Moderate wind")
    print("3. Stormy conditions")
    print("4. High turbulence")
    print("5. Custom wind")
    print("6. Exit")
    
    try:
        while True:
            choice = input("\nSelect wind condition (1-6): ").strip()
            
            if choice == "1":
                controller.create_preset_wind_conditions("calm")
            elif choice == "2":
                controller.create_preset_wind_conditions("moderate")
            elif choice == "3":
                controller.create_preset_wind_conditions("stormy")
            elif choice == "4":
                controller.create_preset_wind_conditions("turbulent")
            elif choice == "5":
                # Custom wind settings
                speed = float(input("Wind speed (m/s): "))
                direction = input("Wind direction (x,y,z): ").split(',')
                direction = [float(x) for x in direction]
                turbulence = float(input("Turbulence intensity (0-1): "))
                
                for zone in controller.wind_zones.values():
                    zone.set_wind_speed(speed)
                    zone.set_wind_direction(direction)
                    zone.set_turbulence_intensity(turbulence)
                    
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please select 1-6.")
                
            # Update wind zones
            controller.update()
            
            # Show wind at drone position
            drone_pos = np.array([0, 5, 0])
            wind = controller.get_wind_at_position(drone_pos)
            print(f"💨 Wind at drone position: {wind} m/s")
            
    except KeyboardInterrupt:
        print("\n🛑 Wind controller stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        
    print("🏁 Wind controller complete!")

if __name__ == "__main__":
    main() 