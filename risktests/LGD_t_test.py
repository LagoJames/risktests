import numpy as np
import pandas as pd
from scipy.stats import t

def lgd_t_test(df, observed_LGD_col, expected_LGD_col, verbose=False):
    """t-test for the Null hypothesis that estimated LGD is greater than true LGD


    Parameters
    ----------
    df: array-like, at least 2D
        data
    observed_LGD_col: string
        name of column with observed LGD values
    expected_LGD_col: string
        name of column with expected LGD values
    verbose: boolean
        if true, results and interpretation are printed


    Returns
    -------
    N: integer
        Number of customers
    LGD.mean: float
        Mean value of observed LGD values
    pred_LGD.mean: float
        Mean value of predicted LGD values
    t_stat: float
        test statistic
    lgd_s2: float
        denominator of test statistic
    p_value: float
        p-value of the test


    Notes
    -----------
    Observations are assumed to be independent.
    This fundtion can be used for both performing and non-performing LGDs.


    Examples
    --------
    >>res = lgd_t_test(df=df, observed_LGD_col='LGD', expected_LGD_col='PRED_LGD', verbose=True)
    >>print(res)
    """
    # Checking for any missing data
    if df.empty:
        raise TypeError('No data provided!')
    if observed_LGD_col is None:
        raise TypeError('No column name for observed LGDs provided')
    if expected_LGD_col is None:
        raise TypeError('No column name for expected LGDs provided')

    # Checking that the correct datatype
    if not isinstance(observed_LGD_col, str):
        raise TypeError('observed_LGD_col not of type string')
    if not isinstance(expected_LGD_col, str):
        raise TypeError('expected_LGD_col not of type string')

    # Check if the correct column names have been provided
    if observed_LGD_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(observed_LGD_col))
    if expected_LGD_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(expected_LGD_col))

    # Check the data for missing values
    if df[observed_LGD_col].hasnans:
        raise ValueError('Missing values in {}'.format(observed_LGD_col))
    if df[expected_LGD_col].hasnans:
        raise ValueError('Missing values in {}'.format(expected_LGD_col))

    N = len(df)
    LGD = df[observed_LGD_col]
    pred_LGD = df[expected_LGD_col]
    error = LGD - pred_LGD
    mean_error = error.mean()
    num = np.sqrt(N)*mean_error
    lgd_s2 = ((error - mean_error)**2).sum()/(N-1)
    t_stat = num/np.sqrt(lgd_s2)
    p_value = 1 - t.cdf(t_stat, df=N-1)

    if verbose is True:
        # print the results
        print("t_stat=%.3f, LGD.mean=%.3f,pred_LGD.mean=%.3f,N=%d, s2=%.3f, p=%.3f" % (t_stat, pred_LGD.mean(), LGD.mean(), N, lgd_s2, p_value))
        if p_value <= 0.05:
            print(
                "P-value <= 5%, therefore, H0 is rejected.")
        elif p_value > 0.05:
            print(
                "P-value > 5%, therefore, H0 fails to be rejected.")

    return N, LGD.mean(), pred_LGD.mean(), t_stat, lgd_s2, p_value
