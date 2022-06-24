import pandas as pd
import numpy as np
from scipy.stats import rankdata


def Coefficient_of_concordance(df, defaults_col, PDs_col, ratings_col):
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
    coef : float
        calculated Coefficient of Concordance

    Notes
    -----
    Takes a value between 0 and 1. The measured concordance is between
    the average default probability per bucket and the number of defaults
    per bucket.

    References
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems
    (revised). https://www.bis.org/publ/bcbs_wp14.htm
    [2] Samorodov, B. V., Azarenkova, G. M., Golovko, O. G., Miroshnik,
    O. Y., & Babenko, M. V. (2019). CREDIT RISK MANAGEMENT IN THE BANK’S
    FINANCIAL STABILITY SYSTEM. Financial and Credit Activity Problems of
    Theory and Practice, 4(31), 301–310.
     https://doi.org/10.18371/fcaptp.v4i31.190920

    Examples
    --------
    >>res = Coefficient_of_concordance(
        df=df,
        defaults_col = 'default_flag',
        PDs_col='prob_default',
        ratings_col = 'ratings')
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
    X = []
    Y = []
    for rating in set(ratings):
        temp = df[df[ratings_col] == rating]
        X.append(temp[defaults_col].sum())
        Y.append(temp[PDs_col].mean())
    ranked_X = len(X) - rankdata(X, method='max') + 1
    ranked_Y = len(Y) - rankdata(Y, method='max') + 1
    expt_ratings = pd.DataFrame([(a, b) for a, b in zip(ranked_X, ranked_Y)])
    if expt_ratings.ndim != 2:
        raise 'ratings matrix must be 2-dimensional'
    m = expt_ratings.shape[1]  # Number of raters
    n = expt_ratings.shape[0]  # Number of items rated
    denom = (1/12)*m**2*(n**3-n)
    ratings_sum = np.sum(expt_ratings, axis=1)
    a = 0.5*m*(n+1)
    num = ((ratings_sum - a)**2).sum()
    return num/denom
