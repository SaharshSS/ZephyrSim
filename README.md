<p align="center">
  <img src="https://raw.githubusercontent.com/SaharshSS/ZephyrSim/main/media/zephyrsim-banner.png" alt="Robot Coprocessor Banner" />
</p>

<p align="center">
  <b>Simulate drone flight through wind, GPS, and airspace—powered by NVIDIA Omniverse and OpenUSD.</b>
</p>

<p align="center">
  <a href="https://github.com/SaharshSS/ZephyrSim/releases">
    <img alt="Release" src="https://img.shields.io/github/v/release/SaharshSS/ZephyrSim?include_prereleases&style=flat-square">
  </a>
  <a href="https://github.com/SaharshSS/ZephyrSim/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/SaharshSS/ZephyrSim?style=flat-square">
  </a>
  <a href="https://github.com/SaharshSS/ZephyrSim/blob/main/LICENSE">
    <img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square">
  </a>
  <img alt="Status" src="https://img.shields.io/badge/status-WIP-yellow?style=flat-square">
  <img alt="Last Commit" src="https://img.shields.io/github/last-commit/SaharshSS/ZephyrSim?style=flat-square">
  <a href="https://developer.nvidia.com/nvidia-omniverse">
    <img alt="Omniverse" src="https://img.shields.io/badge/Omniverse-76B900?logo=nvidia&logoColor=fff&style=flat-square">
  </a>
</p>


---

## ZephyrSim

**ZephyrSim** is an open-source drone simulation environment built in **IsaacSim** and **OpenUSD**. It focuses on realistic aerial navigation through dynamic environments with wind, planes, and GPS imperfections—ideal for testing autonomous flight logic and perception systems.

---

## Features

- Realistic drone flight with simulated GPS & IMU
- Configurable wind zones and turbulence fields
- Simulated airspace with moving planes
- Path-planning with Python scripting
- Sensor support: Coming soon!
- ROS2-ready (optional) for real-world testing integration

## Wind Physics Models

### Vertical Wind Profile (Logarithmic Law)
The mean wind speed at height $z$ is:

$$
v(z) = v_{ref} \frac{\ln(z/z_0)}{\ln(z_{ref}/z_0)}
$$

- $z_0$: surface roughness (m)
- $v_{ref}$: wind speed at reference height $z_{ref}$
- $z$: current height (m)

This models how wind increases with altitude above the ground.

---

### Dryden Turbulence Model
A standard model for simulating atmospheric turbulence in flight simulation:

- Generates realistic, time-correlated wind fluctuations in all directions.
- Used in aerospace and UAV research.
- See: [Dryden Wind Turbulence Model (Wikipedia)](https://en.wikipedia.org/wiki/Dryden_wind_turbulence_model)

---

### Gust Fronts and Microbursts
- **Gust Front:** Sudden, strong, short-lived increase in wind speed, often in the main wind direction.
- **Microburst:** Localized, intense downdraft with outward radial wind at the surface.

Both are modeled as time- and position-dependent wind events:
- Gusts: $\vec{v}_{gust} = \vec{v}_{wind} \cdot S(t, d)$
- Microburst: $\vec{v}_{microburst} = [\text{outflow}, \text{down}, \text{outflow}]$

where $S(t, d)$ is a shape function of time and distance from the event center.

---

See the code for details and parameter tuning!

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

```
