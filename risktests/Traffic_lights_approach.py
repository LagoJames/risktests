import pandas as pd
import numpy as np


def traffic_lights(df, ratings_col, defaults_col):
    """traffic lights approach to PD validation
    Parameters
    ----------
    df: array-like, at least 2D
        data
    ratings_col: string
        name of column with ratings
    defaults_col: string
        name of column with default statuses

    Returns
    -------
    results : array-like, 2D
        traffic light for each bucket

    References
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems
    (revised). https://www.bis.org/publ/bcbs_wp14.htm
    [2] Tasche, D. (2003). A traffic lights approach to PD validation
    (arXiv:cond-mat/0305038). arXiv.

    Examples
    --------
    >>res = traffic_lights(
        df=df,
        ratings_col='ratings',
        defaults_col='default_flag')
    >>print(res)
    """
    if df.empty:
        raise TypeError('No data provided!')
    if defaults_col is None:
        raise TypeError('No column name for defaults provided')
    if ratings_col is None:
        raise TypeError('No column name for ratings provided')

    # Checking that the correct datatype
    if not isinstance(defaults_col, str):
        raise TypeError('defaults_col not of type string')
    if not isinstance(ratings_col, str):
        raise TypeError('ratings_col not of type string')

    # Check if the correct column names have been provided
    if defaults_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(defaults_col))
    if ratings_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(ratings_col))

    # Check the data for missing values
    if df[ratings_col].hasnans:
        raise ValueError('Missing values in {}'.format(ratings_col))
    if df[defaults_col].hasnans:
        raise ValueError('Missing values in {}'.format(defaults_col))

    ratings = df.ratings
    X = []
    results = pd.DataFrame({'Rating': [], 'Traffic Light': []})

    for rating in set(ratings):
        temp = df[df[ratings_col] == rating]
        X.append(temp[defaults_col].sum())
        res = pd.DataFrame({'Rating': [rating], 'Traffic Light': [rating]})
        results = pd.concat([results, res])

    c_low = np.quantile(X, 0.95)
    c_high = np.quantile(X, 0.95)
    Y = []
    for i in set(X):
        if i < c_low:
            Y.append('Green')
        elif i > c_low and i < c_high:
            Y.append('Yellow')
        else:
            Y.append('Red')
    results['Traffic Light'] = Y
    results = results.set_index('Rating')
    return results
