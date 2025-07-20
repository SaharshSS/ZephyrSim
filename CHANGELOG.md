# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [Unreleased]

### Added
- **Flight Simulator Wind System**: Complete overhaul of wind simulation with professional-grade capabilities
  - Configurable wind zones with 3D directional control
  - Realistic wind speed ranges (0-20+ m/s)
  - Advanced turbulence simulation with configurable intensity (0-1 scale)
  - Wind gust system with frequency, amplitude, and duration control
  - Distance-based wind falloff for realistic zone boundaries
  - Visual wind indicators (direction arrows, speed bars, turbulence spheres)
  - Preset wind conditions: Calm, Moderate, Stormy, Turbulent

- **Enhanced Wind Zone Asset** (`assets/wind_zone.usd`)
  - Wind speed and direction parameters
  - Turbulence intensity and gust frequency controls
  - Visual wind direction arrow with arrowhead
  - Wind speed indicator bar with dynamic positioning
  - Turbulence visualization sphere
  - Multiple wind particle effects
  - Physics integration for collision detection

- **Wind Controller Script** (`scripts/wind_controller.py`)
  - `WindZone` class with comprehensive wind parameter management
  - Real-time wind vector calculations at any position
  - Perlin-like turbulence noise generation
  - Wind gust envelope simulation (quick rise, slow decay)
  - Dynamic visual indicator updates
  - `WindController` class for managing multiple wind zones
  - Interactive wind condition presets and custom settings

- **Enhanced Drone Controller** (`scripts/fly_to_waypoints.py`)
  - Integration with wind controller system
  - Realistic wind force calculations including drag effects
  - Air density and cross-sectional area physics
  - Relative velocity calculations for accurate wind effects
  - Real-time wind force feedback and status display
  - Enhanced status reporting with wind force vectors

### Changed
- **Project Focus**: Removed bird simulation features to focus exclusively on wind and drone flight
  - Deleted `assets/bird.usd` asset
  - Removed bird references from `main_stage.usd`
  - Updated README.md to reflect wind-focused simulation
  - Streamlined project structure for wind simulation emphasis

### Technical Details
- **Wind Physics**: 
  - Air density: 1.225 kg/m³
  - Drag coefficient calculations
  - Cross-sectional area considerations
  - Relative velocity wind effects
- **Wind Zone Parameters**:
  - Wind speed: 0-20+ m/s
  - Wind direction: Full 3D normalized vectors
  - Turbulence intensity: 0-1 scale
  - Gust frequency: 0.1-2.0 Hz
  - Gust amplitude: 0-10+ m/s
  - Gust duration: 0.1-5.0 seconds
- **Visual Indicators**:
  - Dynamic wind direction arrows
  - Real-time speed indicator bars
  - Scalable turbulence spheres
  - Wind particle effects

### Files Added
- `scripts/wind_controller.py` - Complete wind simulation system

### Files Modified
- `assets/wind_zone.usd` - Enhanced with flight simulator parameters
- `scripts/fly_to_waypoints.py` - Integrated wind physics
- `main_stage.usd` - Removed bird references
- `README.md` - Updated to reflect wind-focused features

### Files Removed
- `assets/bird.usd` - Bird simulation asset (no longer needed)

### [0.1.3](https://github.com/SaharshSS/ZephyrSim/compare/v0.1.2...v0.1.3) (2025-07-20)

## [0.1.0] - 2024-07-19

### Added
- Initial ZephyrSim project structure
- Basic drone asset with quadcopter geometry
- Open field environment with terrain and obstacles
- Simple waypoint navigation system
- Basic physics scene configuration
- Project documentation and README

### Files Created
- `assets/drone.usd` - Basic quadcopter drone
- `assets/wind_zone.usd` - Initial wind zone (basic version)
- `environments/open_field.usd` - Open field environment
- `main_stage.usd` - Main simulation stage
- `scripts/fly_to_waypoints.py` - Basic waypoint navigation
- `README.md` - Project documentation
