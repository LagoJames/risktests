import numpy as np
import pandas as pd


def PSI(df, initial_ratings_col, final_ratings_col):
    """Population stability index for the ratings bases
    PARAMETERS
    ----------
    df: array-like, at least 2D
        data
    ratings_col: string
        name of column with ratings
    final_ratings_col: string
        name of column with ratings


    RETURN
    ------
    psi : float
        calculated PSI value
    NOTES
    -----
    According to Chiriță & Nica (2020), the Population Stability Index (PSI)
    measures the difference between the model development sample and the
    current (final) sample.

    REFERENCES
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems
    (revised). https://www.bis.org/publ/bcbs_wp14.htm

    [2] Chiriță, N., & Nica, I. (2020). An approach to measuring credit risk
     in a banking institution from Romania.

    EXAMPLE
    -------
    >>res = PSI(
        df=df,
        initial_ratings_col='ratings',
        final_ratings_col='ratings2')
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
    a_totals = pd.crosstab(a, a).sum()
    b_totals = pd.crosstab(b, b).sum()
    pi = (a_totals/a_totals.sum())*100
    qi = (b_totals/b_totals.sum())*100
    return ((pi-qi)*np.log(pi/qi)).sum()
