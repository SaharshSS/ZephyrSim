# ZephyrSim Documentation

Welcome to the comprehensive ZephyrSim documentation! This directory contains all the documentation you need to use, understand, and contribute to ZephyrSim.

---

## 📚 Documentation Structure

### 🚀 [Quick Reference](QUICK_REFERENCE.md)
**Start here!** Essential commands, parameters, and code templates for quick reference.
- Basic drone control
- Wind configuration 
- Common flight patterns
- Default parameters
- Troubleshooting

### 📖 [API Documentation](API_DOCUMENTATION.md) 
Complete reference for all public APIs, classes, and functions.
- DroneController API
- WindController API  
- WindZone API
- Physics models
- Configuration options

### 🔧 [Component Reference](COMPONENT_REFERENCE.md)
Detailed analysis of all components, scripts, and implementation details.
- Script-by-script breakdown
- Physics model implementations
- Performance considerations
- File structure

### 💡 [Usage Examples](USAGE_EXAMPLES.md)
Practical tutorials and examples for common use cases.
- Quick start examples
- Flight patterns
- Wind effects
- Data logging
- Performance optimization

---

## 🗺️ Navigation Guide

### New to ZephyrSim?
1. **Start with**: [Quick Reference](QUICK_REFERENCE.md) for basic commands
2. **Try examples**: [Usage Examples](USAGE_EXAMPLES.md) for hands-on learning
3. **Deep dive**: [API Documentation](API_DOCUMENTATION.md) for complete reference

### Developing with ZephyrSim?
1. **API Reference**: [API Documentation](API_DOCUMENTATION.md) for function signatures
2. **Implementation Details**: [Component Reference](COMPONENT_REFERENCE.md) for internals
3. **Code Examples**: [Usage Examples](USAGE_EXAMPLES.md) for patterns

### Contributing to ZephyrSim?
1. **Code Structure**: [Component Reference](COMPONENT_REFERENCE.md) 
2. **API Guidelines**: [API Documentation](API_DOCUMENTATION.md)
3. **Example Patterns**: [Usage Examples](USAGE_EXAMPLES.md)

---

## 🔍 Quick Search

### Common Topics
- **Basic Flight Control**: [Quick Reference](QUICK_REFERENCE.md#-basic-drone-control)
- **Wind Configuration**: [Quick Reference](QUICK_REFERENCE.md#-wind-controller)
- **Flight Patterns**: [Usage Examples](USAGE_EXAMPLES.md#custom-flight-patterns)
- **Troubleshooting**: [Usage Examples](USAGE_EXAMPLES.md#troubleshooting)
- **Physics Models**: [API Documentation](API_DOCUMENTATION.md#wind-physics-models)

### API References
- **DroneController**: [API Documentation](API_DOCUMENTATION.md#dronecontroller-api)
- **WindController**: [API Documentation](API_DOCUMENTATION.md#windcontroller-api)
- **WindZone**: [API Documentation](API_DOCUMENTATION.md#windzone-api)

### Advanced Features
- **Tornado Simulation**: [Usage Examples](USAGE_EXAMPLES.md#tornado-simulation)
- **Data Logging**: [Usage Examples](USAGE_EXAMPLES.md#flight-data-logger)
- **Performance Optimization**: [Usage Examples](USAGE_EXAMPLES.md#performance-optimization)

---

## 📄 File Descriptions

| File | Purpose | Best For |
|------|---------|----------|
| `QUICK_REFERENCE.md` | Cheat sheet with essential commands | Daily development, quick lookup |
| `API_DOCUMENTATION.md` | Complete API reference | Understanding functions, parameters |
| `COMPONENT_REFERENCE.md` | Implementation details | Understanding code structure |
| `USAGE_EXAMPLES.md` | Practical tutorials | Learning patterns, solving problems |

---

## 🛠️ Quick Start Template

```python
#!/usr/bin/env python3
"""ZephyrSim Quick Start Template"""

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

# Define mission
waypoints = [
    [0, 5, 0],      # Start
    [10, 8, 5],     # Waypoint 1
    [20, 10, 10],   # Waypoint 2
    [0, 5, 0]       # Return home
]

# Execute mission
dt = 0.016  # 60 FPS
for waypoint in waypoints:
    print(f"Flying to {waypoint}")
    controller.set_target(waypoint)
    
    while True:
        result = controller.calculate_control(dt)
        if result['target_reached']:
            print("✅ Reached!")
            break
        time.sleep(dt)

print("🎉 Mission complete!")
```

For more examples, see [Usage Examples](USAGE_EXAMPLES.md).

---

## 🔗 External Links

- **Main Repository**: [ZephyrSim on GitHub](https://github.com/SaharshSS/ZephyrSim)
- **Issues & Support**: [GitHub Issues](https://github.com/SaharshSS/ZephyrSim/issues)
- **NVIDIA Isaac Sim**: [Developer Documentation](https://developer.nvidia.com/isaac-sim)
- **OpenUSD**: [Official Documentation](https://openusd.org/release/index.html)

---

*ZephyrSim v0.1.8 - Happy flying! 🚁*