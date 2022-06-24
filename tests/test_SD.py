import Somers_d as SD
import pandas as pd


def test_SD():
    df = pd.read_excel('synthetic_pd.xlsx')
    output = SD.Somersd(
                df=df,
                ratings_col='ratings',
                PDs_col='prob_default',
                defaults_col='default_flag')
    assert round(output, 15) == 0.538461538461538
