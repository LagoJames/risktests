import numpy as np
import pandas as pd
from scipy.stats import norm


def Speigelhalter_Normal_test(df, ratings_col, defaults_col, PDs_col):
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
    results : array-like, 4D
        z-score, p-value and pass/fail verdict per rating and overall


    References
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems
    (revised). https://www.bis.org/publ/bcbs_wp14.htm

    Examples
    --------
    >>res = Speigelhalter_Normal_test(
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
    results = pd.DataFrame({
        'Rating': [],
        'z-score': [],
        'P-Value': [],
        'Pass/Fail':  []})
    ratings = df[ratings_col]

    for rating in set(ratings):
        temp = df[df[ratings_col] == rating]
        MSE = ((temp[defaults_col] - temp[PDs_col])**2).sum()/len(temp)
        EMSE = (temp[PDs_col]*(1 - temp[PDs_col])).sum()/len(temp)
        Var_EMSE = (temp[PDs_col]*(1-temp[PDs_col])*(1-2*temp[PDs_col])**2)
        Var_EMSE = Var_EMSE.sum()/(len(temp))**2
        z = (MSE - EMSE)/np.sqrt(Var_EMSE)
        p = norm.sf(abs(z))

        if p < 0.05:
            verdict = 'Pass'
        else:
            verdict = 'Fail'

        res = pd.DataFrame({
            'Rating': [rating],
            'z-score': [z],
            'P-Value': [p],
            'Pass/Fail': [verdict]})

        results = pd.concat([results, res])
    # Overall

    MSE = ((df[defaults_col] - df[PDs_col])**2).sum()/len(df)
    EMSE = (df[PDs_col]*(1 - df[PDs_col])).sum()/len(df)
    Var_EMSE = (df[PDs_col]*(1-df[PDs_col])*(1-2*df[PDs_col])**2)
    Var_EMSE = Var_EMSE.sum()/(len(df))**2
    z = (MSE - EMSE)/np.sqrt(Var_EMSE)
    p = norm.sf(abs(z))
    if p <= 0.05:
        verdict = 'Pass'
    else:
        verdict = 'Fail'
    overall = pd.DataFrame({
        'Rating': ['Overall'],
        'z-score': [z],
        'P-Value': [p],
        'Pass/Fail':  [verdict]})

    results = pd.concat([results, overall]).set_index('Rating')

    return results
