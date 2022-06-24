import Coefficient_of_concordance as CC 
import pandas as pd
import pandas


def test_CC():
    df = pd.read_excel('synthetic_pd.xlsx')
    output = CC.Coefficient_of_concordance(
        df=df,
        defaults_col='default_flag',
        PDs_col='prob_default',
        ratings_col='ratings')
    assert round(output, 8) == 0.83956044