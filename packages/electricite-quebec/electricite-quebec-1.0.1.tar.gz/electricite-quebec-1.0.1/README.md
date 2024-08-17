# HydroQuebec API Client

This Python package provides an interface to fetch Quebec electricity demand data from the electricite-quebec data platform. It's designed for easy integration into data analysis workflows that require up-to-date information about electricity usage in Quebec.

## Installation

You can install the package using pip:

```bash
pip install hydroquebec
```


## Usage
To use this package, you need to obtain an API key from behdad.ehsani@hec.ca. Once you have the API key, you can fetch data as follows:

```python
from hydroquebec.api import Hydro_quebec_data

# Set your API key
api_key = 'your_api_key_here'

# Define the data type ('demand' is currently supported)
data_type = 'demand'

# Specify the start and end dates for the data
start_date = '2024-08-01'
end_date = '2024-08-01'

# Fetch the data
data_frame = Hydro_quebec_data(api_key, data_type, start_date, end_date)

# Print the first few rows of the DataFrame
print(data_frame.head())
```

## Contact
If you have any questions, please contact behdad.ehsani@hec.ca.