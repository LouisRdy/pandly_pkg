# Pandly

Pandly is a Python package that contains handy functions. 
Built on top of Pandas and Plotly, its main goal is to make data analysis and data manipulation even easier.


## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Pandly like below. 
Rerun this command to check for and install  updates .
```bash
pip install git+https://github.com/LouisRdy/pandly_pkg.git
```

## Usage
Features:
* functions.missing_value_counts --> display missings values count and percentage for all your df columns
* functions.vcounts --> display value counts in a proper table and a nice plotly graph
* functions.groupby_2 --> display proportion of a column based on another one

#### Demo of some of the features:
```python
import pandas as pd
import pandly as pdy

data = {
    "Gender" : ["Male", "Male", "Women", "Women", "Male"],
    "Nationality": ["France", "Kabylia", "France", "Kabylia", "Kabylia"]
}

df = pd.DataFrame(data)

pdy.groupby_2(
    data=df,
    column_1="Gender",
    column_2="Nationality",
    round_to=4
)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
