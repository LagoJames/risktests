import numpy as np
import pandas as pd


def Information_value(df, defaults_col, PDs_col, ratings_col):
    """
    Parameters
    ----------
    df: array-like, at least 2D
        data
    ratings_col: string
        name of column with ratings
    PDs_col: string
        name of column with probabilities-of-default values
    defaults_col: string
        name of column with default statuses


    Returns
    -------
    results : array-like, 2D
        information value for each bucket and overall


    References
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems
    (revised). https://www.bis.org/publ/bcbs_wp14.htm

    Examples
    --------
    >>res = Information_value(
        df=df,
        ratings_col='ratings',
        defaults_col='default_flag',
        PDs_col='prob_default')
    >>print(res)
    """
    if df.empty:
        raise TypeError('No data provided!')
    if defaults_col is None:
        raise TypeError('No column name for defaults provided')
    if ratings_col is None:
        raise TypeError('No column name for ratings provided')
    if PDs_col is None:
        raise TypeError('No column name for PDs provided.')

    # Checking that the correct datatype
    if not isinstance(defaults_col, str):
        raise TypeError('defaults_col not of type string')
    if not isinstance(ratings_col, str):
        raise TypeError('ratings_col not of type string')
    if not isinstance(PDs_col, str):
        raise TypeError('PDs_col not of type string')

    # Check if the correct column names have been provided
    if defaults_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(defaults_col))
    if ratings_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(ratings_col))
    if PDs_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(PDs_col))

    # Check the data for missing values
    if df[ratings_col].hasnans:
        raise ValueError('Missing values in {}'.format(ratings_col))
    if df[defaults_col].hasnans:
        raise ValueError('Missing values in {}'.format(defaults_col))
    if df[PDs_col].hasnans:
        raise ValueError('Missing values in {}'.format(PDs_col))

    ratings = df[ratings_col]
    results = pd.DataFrame({'Rating': [], 'IV': []})
    for rating in set(ratings):
        temp = df[df[ratings_col] == rating]
        tempX = temp[temp[defaults_col] == 0]
        tempY = temp[temp[defaults_col] == 1]
        num = len(tempX[defaults_col])/len(df[df[defaults_col] == 0])
        denom = len(tempY[defaults_col])/len(df[df[defaults_col] == 1])
        IV = (num - denom)*np.log(num/denom)
        res = pd.DataFrame({'Rating': [rating], 'IV': [IV]})
        results = pd.concat([results, res])
    IV = sum(results['IV'])
    res = pd.DataFrame({'Rating': ['Overall'], 'IV': [IV]})
    results = pd.concat([results, res])
    results = results.set_index('Rating')
    return results
