import numpy as np
import pandas as pd
from scipy.stats import t


def elbe_t_test(df, LGD_col, ELBE_col, verbose=False):
    """t-test of Null hypothesis that ELBE is equal to realised LGD.


    Parameters
    ----------
    df: array-like, at least 2D
        data
    LGD_col: string
        name of column with LGD values
    ELBE_col: string
        name of column with ELBE values
    verbose: boolean
        if true, results and interpretation are printed


    Returns
    -------
    N: integer
        Number of customers
    LGD.mean: float
        Mean value of LGD
    ELBE.mean: float
        Mean value of ELBE
    t_stat: float
        test statistic
    s2: float
        denominator of test statistic
    p_value: float
        p-value of the test


    Notes
    -----------
    Observations are assumed to be independent.


    Examples
    --------
    >>res = elbe_t_test(df=df, LGD_col='LGD', ELBE_col='ELBE', verbose=True)
    >>print(res)
    """
    # Checking for any missing data
    if df.empty:
        raise TypeError('No data provided!')
    if LGD_col is None:
        raise TypeError('No column name for LGDs provided')
    if ELBE_col is None:
        raise TypeError('No column name for ELBEs provided')

    # Checking that the correct datatype
    if not isinstance(LGD_col, str):
        raise TypeError('LGD_col not of type string')
    if not isinstance(ELBE_col, str):
        raise TypeError('ELBE_col not of type string')

    # Check if the correct column names have been provided
    if LGD_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(LGD_col))
    if ELBE_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(ELBE_col))

    # Check the data for missing values
    if df[LGD_col].hasnans:
        raise ValueError('Missing values in the {} column'.format(LGD_col))
    if df[ELBE_col].hasnans:
        raise ValueError('Missing values in the {} column'.format(ELBE_col))

    N = len(df)
    LGD = df[LGD_col]
    ELBE = df[ELBE_col]

    error = LGD - ELBE
    mean_error = error.mean()
    num = np.sqrt(N)*mean_error
    s2 = ((error - mean_error)**2).sum()/(N-1)
    t_stat = num/np.sqrt(s2)
    p_value = 2*(1 - t.cdf(abs(t_stat), df=N-1))

    if verbose is True:
        # print the results
        print("t_stat=%.3f, ELBE.mean=%.3f,LGD.mean=%.3f,N=%d, s2=%.3f, p=%.3f" % (t_stat, ELBE.mean(), LGD.mean(), N, s2, p_value))
        if p_value <= 0.05:
            print(
                "P-value <= 5%, therefore, H0 is rejected.")
        elif p_value > 0.05:
            print(
                "P-value > 5%, therefore, H0 fails to be rejected.")
    return N, LGD.mean(), ELBE.mean(), t_stat, s2, p_value

