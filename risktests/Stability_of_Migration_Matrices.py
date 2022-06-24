import numpy as np
import pandas as pd
from scipy.stats import norm

df = pd.read_excel('synthetic_pd.xlsx')


def migration_matrix_stability(df, initial_ratings_col, final_ratings_col):
    """z-tests to verify stability of transition matrices

    Parameters
    ----------
    df: array-like, at least 2D
        data
    initial_ratings_col: string
        name of column with initial ratings values
    final_ratings_col: string
        name of column with final ratings values

    Returns
    -------
    z_df: array-like
        z statistic for each ratings pair
    phi_df: array-like
        p-values for each ratings pair


    Notes
    -----------
    The Null hypothesis is that p_ij >= p_ij-1 or p_ij-1 >= p_ij
    depending on whether the (ij) entry is below or above main diagonal


    Examples
    --------
    >>res = migration_matrix_stability(df=df, initial_ratings_col='ratings', final_ratings_col='ratings2')
    >>print(res)
    """
    a = df[initial_ratings_col]
    b = df[final_ratings_col]
    N_ij = pd.crosstab(a, b)
    p_ij = pd.crosstab(a, b, normalize='index')
    K = len(set(a))
    z_df = p_ij.copy()
    for i in range(1, K+1):
        for j in range(1, K+1):
            if i == j:

                z_ij = np.nan

            if i > j:
                Ni = N_ij.sum(axis=1).values[i-1]

                num = p_ij.iloc[i-1, j-1+1] - p_ij.iloc[i-1, j-1]
                den_a = p_ij.iloc[i-1, j-1]*(1-p_ij.iloc[i-1, j-1])/Ni
                den_b = p_ij.iloc[i-1, j-1+1]*(1-p_ij.iloc[i-1, j-1+1])/Ni
                den_c = 2*p_ij.iloc[i-1, j-1]*p_ij.iloc[i-1, j-1+1]/Ni

                z_ij = num/np.sqrt(den_a + den_b + den_c)

            elif i < j:
                Ni = N_ij.sum(axis=1).values[i-1]

                num = p_ij.iloc[i-1, j-1-1] - p_ij.iloc[i-1, j-1]
                den_a = p_ij.iloc[i-1, j-1]*(1-p_ij.iloc[i-1, j-1])/Ni
                den_b = p_ij.iloc[i-1, j-1-1]*(1-p_ij.iloc[i-1, j-1-1])/Ni
                den_c = 2*p_ij.iloc[i-1, j-1]*p_ij.iloc[i-1, j-1-1]/Ni

                z_ij = num/np.sqrt(den_a + den_b + den_c)

            else:

                z_ij = np.nan

            z_df.iloc[i-1, j-1] = z_ij
    phi_df = z_df.apply(lambda x: x.apply(lambda y: norm.cdf(y)))
    return z_df, phi_df
