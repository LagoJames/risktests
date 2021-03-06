import pandas as pd


def migration_matrix_statistics(df, initial_ratings_col, final_ratings_col):
    """Calculates statistics that summarise the upgrades and downgrades of ratings

    Parameters
    ----------
    df: array-like, at least 2D
        data
    initial_ratings_col: string
        name of column with observed LGD values
    final_ratings_col: string
        name of column with expected LGD values


    Returns
    -------
    upper_mwb: float
        upper matrix weighted bandwidth
    lower_mwb: float
        lower matrix weighted bandwidth


    Examples
    --------
    >>res = migration_matrix_statistics(
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
    N_ij = pd.crosstab(a, b)
    p_ij = pd.crosstab(a, b, normalize='index')
    K = len(set(a))
    mnormu = mnorml = upper_mwb = lower_mwb = 0
    for i in range(1, K):
        c = p_ij.iloc[i-1, i:].sum()
        b = N_ij.sum(axis=1).values[i-1]
        a = max(i-K, i-1)
        mnormu += a*b*c
    for i in range(2, K+1):
        c = p_ij.iloc[i-1, 0:i-1].sum()
        b = N_ij.sum(axis=1).values[i-1]
        a = max(i-K, i-1)
        mnorml += a*b*c
    for i in range(1, K-1+1):
        for j in range(i+1, K+1):
            upper_mwb += abs(i-j)*N_ij.sum(axis=1).values[i-1]*p_ij.iloc[i-1, j-1]
    upper_mwb = (1/mnormu)*upper_mwb
    for i in range(2, K+1):
        for j in range(1, i-1+1):
            lower_mwb += abs(i-j)*N_ij.sum(axis=1).values[i-1]*p_ij.iloc[i-1, j-1]
    lower_mwb = (1/mnorml)*lower_mwb
    return upper_mwb, lower_mwb
