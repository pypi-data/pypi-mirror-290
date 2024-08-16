![Pranzo decoration](doc/logo/decoration.png)

# Pranzo

**Pranzo** is a Python library designed to study structural build-up at rest in cementitious materials by coupling data from isothermal calorimetry and rheometry experiments ([Michel et al. 2024](https://arxiv.org/html/2404.02850v1)). Its simplicity allows for quick data analysis, even during your lunch break.

## Table of Contents
- [License](#license)
- [Installation](#installation)
- [Basic Usage](#basic-usage)


## License

Copyright &copy; 2024 ETH Zurich (Luca Michel, Flavio Lorez \& David S. Kammer)

**Pranzo** is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

**Pranzo** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with **Pranzo**.  If not, see <https://www.gnu.org/licenses/>.


## Installation

### Requirements
- Python 3.7+
- numpy
- pandas
- h5py
- bamboost


### Installation using pip
```bash
pip install pranzo
```

### Installation in editable mode
```bash
git clone https://gitlab.ethz.ch/cmbm-public/toolboxes/pranzo
cd pranzo
pip install -e .
```

## Basic Usage

### Input

The input to Pranzo includes:
- **Calorimetry data**: Machine output file (`calo_fileid.csv`)
- **Rheometry data**: Machine output file (`rheo_fileid.csv`)
- **Meta data**: Written by the user (`meta_fileid.toml`)

An experiments consists of different measurements (calo, rheo). Ensure that each experiment has a unique identifier (`fileid`). 

The structure for `meta_fileid.toml` is given in `examples/meta_example.toml`.

While **Pranzo** is built to couple calorimetry and rheometry data, it can also be used for standalone calorimetry or rheometry experiments.


### Saving Data

Pranzo saves data in a [bamboost](https://www.bamboost.ch) database. Sample code to add an experiment to a database is given in the notebook `examples/example_usage.ipynb`.

Alternatively, save an experiment from the command line:
```bash
save_exp db_name data_dir file_id
```
- `db_name`: Name of the bamboost database
- `data_dir`: Directory containing the data files
- `file_id`: Identifier of the experiment

### Analyzing data

Below are basic examples of data analysis with pranzo. Further examples are given in the notebook `examples/example_usage.ipynb`.
```python
from bamboost import Manager
from pranzo import Analyzer

db = Manager('db_name')
exp = db['file_id']
a = Analyzer(exp)

# to quickly plot time evolutions
a.plot_Gt()
a.plot_ht()
a.plot_Ht()

# to access data arrays
rheo = a.rheo
t = rheo['time_s'][:]
G = rheo['storage_modulus_Pa'][:]

calo = a.calo
t = calo['time_s'][:]
h = calo['heat_flow_W'][:]
H = calo['heat_J'][:]

# to couple heat and storage modulus data
import numpy as np
import matplotlib.pyplot as plt

time = np.linspace(0, 4*3600, 10000)
G = rheo.interpolate('storage_modulus_Pa', time)
H = calo.interpolate('norm_heat_Jpgbinder', time)

plt.semilogy(H, G)
plt.show()
```