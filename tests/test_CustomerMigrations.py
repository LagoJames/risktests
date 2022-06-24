import risktests.Customer_migrations as CM
import pytest
import pandas as pd
import os


def test_CM():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.abspath(os.path.join(BASE_DIR, 'synthetic_pd.xlsx'))
    df = pd.read_excel(test_file)
    output = CM.migration_matrix(df=df, initial_ratings_col='ratings', final_ratings_col='ratings2')
    assert round(output[0], 2) == 1.05
    assert round(output[1], 1) == 0.6
