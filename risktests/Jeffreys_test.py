import pandas as pd
from scipy.stats import beta


def jeffreys_test(df, ratings_col, PDs_col, defaults_col, alpha=0.05):
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
    alpha: float
        level of significance
    verbose: boolean
        if true, results and interpretation are printed


    Returns
    -------
    results: 7D array-like object
        dataframe with p-value for each rating and other statistics


    Notes
    -----------
    Observations are assumed to be independent.
    This fundtion can be used for both performing and non-performing LGDs.


    Examples
    --------
    >>df = pd.read_excel('sample_data.xlsx')
    >>outpput = jeffreys_test(df=df, ratings_col='ratings', PDs_col='PD', defaults_col='loan_status', alpha=0.05)
    >>print(output)


    """

    if df.empty:
        raise TypeError('No data provided!')
    if alpha is None:
        raise TypeError('No value provided for alpha.')
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
    if not isinstance(alpha, float):
        raise TypeError('alpha should be a float value')

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

    results = pd.DataFrame({'Rating': [], 'PD': [], 'N': [], 'D': [], 'a': [], 'b': [], 'Default Rate': [], 'P-Value': [], 'Pass/Fail':  []})
    ratings = df[ratings_col]

    for rating in set(ratings):
        temp = df[df[ratings_col] == rating]
        mean_probability = temp[PDs_col].mean()
        d = temp[defaults_col].sum()
        n = len(temp)
        a = d + 0.5
        b = n - d + 0.5
        p_value = beta.ppf(alpha, a, b)

        if p_value <= mean_probability:
            verdict = 'Pass'
        else:
            verdict = 'Fail'

        res = pd.DataFrame({'Rating': [rating],
                            'PD': [mean_probability],
                            'N': [n],
                            'D': [d],
                            'a': [a],
                            'b': [b],
                            'Default Rate': [d/n],
                            'P-Value': [p_value],
                            'Pass/Fail': [verdict]})

        results = results.append(res)
    # Overall
    d = df[defaults_col].sum()
    n = len(df)
    a = d + 0.5
    b = n - d + 0.5
    p = beta.ppf(alpha, a, b)
    m = df[PDs_col].mean()
    if p <= m:
        verdict = 'Pass'
    else:
        verdict = 'Fail'
    overall = pd.DataFrame({'Rating': ['Overall'], 'PD': [m], 'N': [n], 'D': [d], 'a': [a], 'b': [b], 'Default Rate': [d/n], 'P-Value': [p], 'Pass/Fail': [verdict]})

    results = results.append(overall).set_index('Rating')

    return results
    
