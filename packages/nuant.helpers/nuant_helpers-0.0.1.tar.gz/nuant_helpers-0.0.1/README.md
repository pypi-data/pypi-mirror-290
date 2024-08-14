<div align="center">
  <img src="https://cdn.prod.website-files.com/6645c2bf1d8a88dfb078b41d/6645d629b58f71cda23ae53e_Logotype-Nuant.svg" alt="Logo">
  <h1>Nuant Helpers</h1>
</div>

# Introduction

This python library can help you manipulate Nuant data more easily.
This module is automatically available on your Nuant development environment (IDE / Dashboard).

# Helpers

List of all helpers available

## Simulation

### fetch_data

Fetch a result of the simulation with the timeseries preformatted with the merge of time and values files.

```python
from nuant.helpers import simulation

data_simulation = simulation.fetch_data("YOUR_SIMULATION_ID", "DATA_FILE_NAME", "YOUR_API_KEY")
```
