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
    results = pd.DataFrame({'Rating': [], 'Information Value': []})

    for rating in set(ratings):
        temp = df[df[ratings_col] == rating]
        tempX = temp[temp[defaults_col] == 0][PDs_col]
        tempY = temp[temp[defaults_col] == 1][PDs_col]
        L = min(min(tempX), min(tempY))
        H = max(max(tempX), max(tempY))
        bins = np.arange(L, H, 1/10*(H-L))
        res = pd.cut(tempX, bins=bins)
        res2 = pd.cut(tempY, bins=bins)
        n0 = res.value_counts().values
        n1 = res2.value_counts().values
        n = len(tempX)
        m = len(tempY)
        i_val = 0
        for j in range(len(n0)):
            if n0[j] == 0:
                n0[j] = 0.0001
            if n1[j] == 1:
                n1[j] = 0.0001
            i_val += ((n1[j]/n) - (n0[j]/m))*np.log((n1[j]*m)/(n0[j]*n))
        res = pd.DataFrame({'Rating': [rating], 'Information Value': [i_val]})
        results = pd.concat([results, res])
    # Overall
    dfX = df[df[defaults_col] == 0][PDs_col]
    dfY = df[df[defaults_col] == 1][PDs_col]
    L = min(min(dfX), min(dfY))
    H = max(max(dfX), max(dfY))
    bins = np.arange(L, H, 1/10*(H-L))
    res = pd.cut(dfX, bins=bins)
    res2 = pd.cut(dfY, bins=bins)
    n0 = res.value_counts().values
    n1 = res2.value_counts().values
    n = len(dfX)
    m = len(dfY)
    i_val = 0
    for j in range(len(n0)):
        if n0[j] == 0:
            n0[j] = 0.0001
        if n1[j] == 1:
            n1[j] = 0.0001
        i_val += ((n1[j]/n) - (n0[j]/m))*np.log((n1[j]*m)/(n0[j]*n))

    overall = pd.DataFrame({'Rating': ['Overall'],
                            'Information Value': [i_val]})
    results = pd.concat([results, overall]).set_index('Rating')
    return results
