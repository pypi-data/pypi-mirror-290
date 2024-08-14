# DataSnap

DataSnap is a simple Python package designed to help data professionals get quick insights into their dataframes. It provides an overview of data shape, missing values, and column recommendations based on best practices for naming conventions.

## Features

- Overview of dataframe shape, missing values, and data types.
- Recommendations for renaming columns based on coding best practices.
- Code snippets for easy column renaming.

## Installation

You can install the package via pip:

```
pip install datasnap
```

## Usage

```
import pandas as pd
from datasnap.core import generate_report

df = pd.DataFrame({
    'Order ID': [1, 2],
    'Order Date': ['2024-01-01', '2024-01-02'],
    'CustomerName': ['John Doe', 'Jane Doe'],
    'State': ['NY', 'CA'],
    'City': ['New York', 'Los Angeles'],
    'Day': [1, 2],
    'Month': [1, 1],
    'Year': [2024, 2024]
})

overview, recommendations = generate_report(df)

print(overview)
print(recommendations)
```

## License 

This project is licensed under the MIT License - see the LICENSE file for details.
