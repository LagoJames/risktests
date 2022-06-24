import pandas as pd
import Binomial_test as BT
import pytest


def test_Bin():
    df = pd.read_excel('synthetic_pd.xlsx')
    output = BT.binomial_test(
                    df=df,
                    ratings_col='ratings',
                    defaults_col='default_flag',
                    PDs_col='prob_default')
    assert round(output['Binomial Test'][1], 1) == 1.0
    assert round(output['Binomial Test'][2], 1) == 1.0
    assert round(output['Binomial Test'][3], 1) == 1.0
    assert round(output['Binomial Test'][4], 1) == 1.0
    assert round(output['Binomial Test'][5], 1) == 1.0
    assert round(output['Binomial Test'][6], 1) == 1.0
    assert round(output['Binomial Test'][7], 1) == 1.0
    assert round(output['Binomial Test'][8], 1) == 1.0
    assert round(output['Binomial Test'][9], 1) == 1.0
    assert round(output['Binomial Test'][10], 1) == 1.0
    assert round(output['Binomial Test'][11], 1) == 1.0
    assert round(output['Binomial Test'][12], 1) == 1.0
    assert round(output['Binomial Test'][13], 1) == 1.0
    assert round(output['Binomial Test'][14], 1) == 1.0
