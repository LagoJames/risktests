import numpy as np
import pandas as pd
from scipy.stats import binom


def binomial_test(df, defaults_col, PDs_col, ratings_col):
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
    results : array-like, 6D
        Number of observations, number of defaults, average PD, Binomial
        Test score and test conclusion per rating.


    References
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems
    (revised). https://www.bis.org/publ/bcbs_wp14.htm

    Examples
    --------
    >>res = binomial_test(
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
    results = pd.DataFrame({
        'Rating': [],
        'Number of Obs': [],
        'Number of Defaults': [],
        'Average PD': [],
        'Binomial Test': [],
        'Conclusion': []})

    alpha = 0.05

    for rating in set(ratings):
        # Calculation of factors needed
        g = df[df[ratings_col] == rating]
        n_g = len(g)
        n_1g = sum(g[defaults_col])
        p_g = np.mean(g[PDs_col])
        binomial_factor = binom.cdf(n_1g, n_g, p_g)
        # Binomial test
        if (binomial_factor <= alpha) | (1 - binomial_factor <= alpha):
            conclusion = 'reject'
        else:
            conclusion = 'fail to reject'
        res = pd.DataFrame({
            'Rating': [rating],
            'Number of Obs': [n_g],
            'Number of Defaults': [n_1g],
            'Average PD': [p_g],
            'Binomial Test': [binomial_factor],
            'Conclusion': [conclusion]})
        results = pd.concat([results, res])
    results = results.set_index('Rating')
    return results
