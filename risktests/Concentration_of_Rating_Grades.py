import numpy as np
import pandas as pd
from scipy.stats import norm


def ratings_concentration(df, initial_ratings_col, final_ratings_col):
    """test for the meaningful dispersion of the rating grades

        Parameters
        ----------
        df: array-like, at least 2D
            data
        initial_ratings_col: string
            name of column with initial ratings
        final_ratings_col: string
            name of column with final ratings


        Returns
        -------
        H_init: float
            Initial Herfindahl index
        H_curr: float
            Final Herfindahl index
        p_value: float
            p-value of the test
        N: integer
            Number of customers or facilities


        Notes
        -----------
        Observations are assumed to be independent.
        This function can be used for both performing and non-performing LGDs.


        Examples
        --------
        >>res = ratings_concentration(df=df, initial_ratings_col='ratings', final_ratings_col='ratings2')
        >>print(res)
        """

    if df.empty:
        raise TypeError('No data provided!')
    if initial_ratings_col is None:
        raise TypeError('No column name for initial ratings provided')
    if final_ratings_col is None:
        raise TypeError('No column name for final ratings provided')

    # Checking that the correct datatype
    if not isinstance(initial_ratings_col, str):
        raise TypeError('defaults_col not of type string')
    if not isinstance(final_ratings_col, str):
        raise TypeError('ratings_col not of type string')

    # Check if the correct column names have been provided
    if initial_ratings_col not in df.columns:
        raise ValueError('{} not in the df'.format(initial_ratings_col))
    if final_ratings_col not in df.columns:
        raise ValueError('{} not in the df'.format(final_ratings_col))

    # Check the data for missing values
    if df[initial_ratings_col].hasnans:
        raise ValueError('Missing values in{}'.format(initial_ratings_col))
    if df[final_ratings_col].hasnans:
        raise ValueError('Missing values in{}'.format(final_ratings_col))

    a = df[initial_ratings_col]
    b = df[final_ratings_col]
    N_init = pd.crosstab(a, a)
    N_curr = pd.crosstab(b, b)
    K = len(set(a))

    R_init = list(N_init.sum(axis=1)/N_init.sum(axis=1).sum())
    R_curr = list(N_curr.sum()/N_curr.sum().sum())

    CV_init = CV_curr = 0
    for i in range(1, K+1):
        CV_init += (R_init[i-1]-1/K)**2
    CV_init = np.sqrt(K*CV_init)
    HI_init = 1 + np.log((CV_init**2+1)/K)/np.log(K)

    for i in range(1, K+1):
        CV_curr += (R_curr[i-1]-1/K)**2
    CV_curr = np.sqrt(K*CV_curr)
    HI_curr = 1 + np.log((CV_curr**2+1)/K)/np.log(K)

    p_value = 1 - norm.cdf(np.sqrt(K-1)*(CV_curr-CV_init)/np.sqrt(CV_curr**2*(0.5 + CV_curr**2)))
    return HI_curr, HI_init, p_value, sum(list(N_curr.sum(axis=1)))
