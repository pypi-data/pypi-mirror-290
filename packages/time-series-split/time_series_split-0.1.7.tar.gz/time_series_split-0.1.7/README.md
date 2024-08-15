
# Time Series Split Package

A Python package for splitting time series data into training and testing sets, preserving the temporal order.

## Installation

You can install this package using pip:

```bash
pip install time_series_split
```

## Usage

The `split_ts` function splits time series data into training and testing sets. It handles both `pandas.DataFrame` and `pandas.Series` inputs and ensures that the split maintains the temporal order.

### Function: `split_ts`

```python
import pandas as pd

def split_ts(X, y=None, test_size=0.2):
    """
    Splits time series data into training and testing sets.

    Parameters:
    X (pd.DataFrame or pd.Series): Features of the time series.
    y (pd.Series or pd.DataFrame, optional): Target column corresponding to the features. (default: None)
    test_size (float): Proportion of the dataset to use as test set. (default: 0.2)

    Returns:
    If `y` is provided:
    X_train, X_test, y_train, y_test (np.ndarray or pd.DataFrame, np.ndarray or pd.DataFrame, np.ndarray or pd.Series, np.ndarray or pd.Series): Training and testing sets.

    If `y` is not provided:
    X_train, X_test (np.ndarray or pd.DataFrame, np.ndarray or pd.DataFrame): Training and testing sets.
    """
```

### Parameters

- **`X`**: Features of the time series. Can be a `pandas.DataFrame` or `pandas.Series`.
- **`y`**: (Optional) Target column corresponding to the features. Can be a `pandas.Series` or `pandas.DataFrame`.
- **`test_size`**: Proportion of the dataset to use as the test set (default is 0.2).

### Returns

- If `y` is provided, returns four objects:
  - `X_train`: Training features.
  - `X_test`: Testing features.
  - `y_train`: Training targets.
  - `y_test`: Testing targets.
  
  All returned as `numpy.ndarray` or `pandas.DataFrame`/`pandas.Series`.

- If `y` is not provided, returns two objects:
  - `X_train`: Training features.
  - `X_test`: Testing features.
  
  Both returned as `numpy.ndarray` or `pandas.DataFrame`.

### Example

Here's how you can use the `split_ts` function:

```python
import pandas as pd
from time_series_split import split_ts

# Sample DataFrame
data = {'date': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009],
        'value': [5, 6, 8, 7, 10, 12, 13, 14, 15, 16]}
df = pd.DataFrame(data)

# Splitting data with target
X_train, X_test, y_train, y_test = split_ts(df['date'], df['value'], test_size=0.3)

# Splitting data
train, test = split_ts(df, test_size=0.3)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact [danttis](mailto:juniordante01@gmail.com).
