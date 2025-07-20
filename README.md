![status](https://img.shields.io/badge/status-WIP-yellow.svg)

<p align="center">
  <img src="https://raw.githubusercontent.com/SaharshSS/zephyrsim/main/media/zephyrsim-banner.png" alt="ZephyrSim Logo" />
</p>

<p align="center">
  <b>Simulate drone flight through wind, GPS, and airspace—powered by NVIDIA Omniverse and OpenUSD.</b>
</p>

---

## 🌬️ ZephyrSim

**ZephyrSim** is an open-source drone simulation environment built in **NVIDIA Omniverse** and **OpenUSD**. It focuses on realistic aerial navigation through dynamic environments with wind, planes, and GPS imperfections—ideal for testing autonomous flight logic and perception systems.

---

## ✨ Features

- 🛰️ Realistic drone flight with simulated GPS & IMU
- 🌪️ Configurable wind zones and turbulence fields
- ✈️ Simulated airspace with moving planes
- 🎮 Path-planning with Python scripting
- 📷 Sensor support: RGB camera, depth, LIDAR, and noise modeling
- 📡 ROS2-ready (optional) for real-world testing integration

---

## 🛠️ Quick Start

### Prerequisites

- NVIDIA Omniverse Launcher (latest)
- Isaac Sim installed
- Python 3.10+
- Git & basic CLI tools

### Clone & Launch

```bash
git clone https://github.com/yourusername/zephyrsim.git
cd zephyrsim

# Launch Isaac Sim and run the control script
./python.sh scripts/fly_to_waypoints.py
```
