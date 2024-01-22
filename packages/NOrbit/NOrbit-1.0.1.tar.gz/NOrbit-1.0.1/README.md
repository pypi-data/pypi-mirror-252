[![codecov](https://codecov.io/gh/Lukas-Orion/NOrbit/graph/badge.svg?token=ZR0LVVUXDU)](https://codecov.io/gh/Lukas-Orion/NOrbit)
# NOrbit
NOrbit is a Python package designed for simulating the N-body problem using a Runge-Kutta 4th order integration scheme. The code provides functions for converting between Keplerian and Cartesian coordinates, calculating accelerations, calculating derivatives, and simulating the orbits of objects in an N-body system.

## Installation
Clone the repository and install the required dependencies using the following commands:
```sh
pip install NOrbit
```

or with plotting dependencies
```sh
pip install NOrbit[plot]
```

## Usage

Here's an example of how to use the NOrbit package:
```python
import numpy as np
from src.NOrbit import NOrbit, Object
```

```python
planets_inner_solar_system = Object.planets_inner_solar_system # list of orbital elements and masses of inner solar system planets

m_sun = 1.0 # mass of sun in solar masses

solar_system = NOrbit(object_elements = planets_inner_solar_system, m_primary = m_sun) # base model of solar system
```

```python
dt = 1/100 # time-step of integration
n_orbits = 100 # number of orbits of first planet (Merkury) around Sun

inner_solar_system_positions = solar_system.orbit(dt = dt, n_orbits = n_orbits)[0] # orbital position calculations for inner planets and Sun
```
For a more detailed example, please check the Example Notebook (`NOrbit example.ipynb`)

## Objects
    Object.mercury
    Object.venus
    Object.earth
    Object.mars
    Object.jupiter
    Object.saturn
    Object.uranus
    Object.neptune
### Grouped Objects
    Object.planets_solar_system
    Object.planets_solar_system_names
    
    Object.planets_inner_solar_system
    Object.planets_inner_solar_system_names
    Object.planets_outer_solar_system
    Object.planets_outer_solar_system_names


## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
