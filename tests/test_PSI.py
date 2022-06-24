import Population_Stability_Index as PSI
import pandas as pd
import pytest


def test_PSI():
    df = pd.read_excel('synthetic_pd.xlsx')
    output = PSI.PSI(
        df=df,
        initial_ratings_col='ratings',
        final_ratings_col='ratings2')
    assert round(output, 10) == 5.4678000061
