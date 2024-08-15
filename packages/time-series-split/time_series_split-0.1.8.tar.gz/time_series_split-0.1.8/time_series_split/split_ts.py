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
    # Check if X is a DataFrame or a Series
    if not isinstance(X, (pd.DataFrame, pd.Series)):
        raise ValueError("X must be a pandas DataFrame or Series")

    # Calculate the number of records for the test set
    n_test = int(len(X) * test_size)

    # Splitting the data into training and testing sets
    X_train = X.iloc[:-n_test]
    X_test = X.iloc[-n_test:]

    # Convert Series to numpy.ndarray
    if isinstance(X, pd.Series):
        X_train = X_train.values
        X_test = X_test.values

    if y is not None:
        # Check if y has the same length as X
        if len(y) != len(X):
            raise ValueError("X and y must have the same number of rows")

        y_train = y.iloc[:-n_test]
        y_test = y.iloc[-n_test:]

        # Convert Series to numpy.ndarray
        if isinstance(y, pd.Series):
            y_train = y_train.values
            y_test = y_test.values

        return X_train, X_test, y_train, y_test
    else:
        return X_train, X_test
