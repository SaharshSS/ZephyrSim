<p align="center">
  <img src="https://raw.githubusercontent.com/SaharshSS/ZephyrSim/main/media/zephyrsim-banner.png" alt="ZephyrSim Logo" />
</p>

<p align="center">
  <b>Simulate drone flight through wind, GPS, and airspace—powered by NVIDIA Omniverse and OpenUSD.</b>
</p>

<p align="center">
  <a href="https://github.com/SaharshSS/ZephyrSim/releases">
    <img alt="Release" src="https://img.shields.io/github/v/release/SaharshSS/ZephyrSim?include_prereleases">
  </a>
  <a href="https://github.com/SaharshSS/ZephyrSim/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/SaharshSS/ZephyrSim">
  </a>
  <a href="https://github.com/SaharshSS/ZephyrSim/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/SaharshSS/ZephyrSim">
  </a>
  <img alt="Status" src="https://img.shields.io/badge/status-WIP-yellow">
  <img alt="Last Commit" src="https://img.shields.io/github/last-commit/SaharshSS/ZephyrSim">
</p>

---

## 🌬️ ZephyrSim

**ZephyrSim** is an open-source drone simulation environment built in **IsaacLab** and **OpenUSD**. It focuses on realistic aerial navigation through dynamic environments with wind, planes, and GPS imperfections—ideal for testing autonomous flight logic and perception systems.

---

## ✨ Features

- 🛰️ Realistic drone flight with simulated GPS & IMU
- 🌪️ Configurable wind zones and turbulence fields
- ✈️ Simulated airspace with moving planes
- 🎮 Path-planning with Python scripting
- 📷 Sensor support: Coming soon!
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
git clone https://github.com/SaharshSS/zephyrsim.git
cd zephyrsim

# Launch Isaac Sim and run the control script
./python.sh scripts/fly_to_waypoints.py
