from itertools import combinations


def Somersd(df, ratings_col, PDs_col, defaults_col):
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
    W : float
        calculated value of Somer's D


    References
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems
    (revised). https://www.bis.org/publ/bcbs_wp14.htm


    Examples
    --------
    >>res = Somersd(
    df=df,
    ratings_col='ratings',
    PDs_col='prob_default',
    defaults_col='default_flag')
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
    C = sum([1 if v1 == v2 else 0 for v1, v2 in zip(
        ['a<b' if a < b else 'a>b' for a, b in combinations(X, 2)],
        ['a<b' if a < b else 'a>b' for a, b in combinations(Y, 2)])])
    D = sum([0 if v1 == v2 else 1 for v1, v2 in zip(
        ['a<b' if a < b else 'a>b' for a, b in combinations(X, 2)],
        ['a<b' if a < b else 'a>b' for a, b in combinations(Y, 2)])])

    W = (C - D)/max(len(list(combinations(X, 2))),
                    len(list(combinations(Y, 2))))
    return W
