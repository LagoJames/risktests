import Speigelhalter_Normal_test as ST
import pandas as pd
import pytest


def test_ST():
    df = pd.read_excel('synthetic_pd.xlsx')
    output = ST.Speigelhalter_Normal_test(
        df=df,
        ratings_col='ratings',
        defaults_col='default_flag',
        PDs_col='prob_default')
    a = [78.6931, 168.0981, 155.45, 159.8649, 21.5747, -110.7245, -96.2287, 
         -102.1287, -79.4184, -70.8243, -55.7118, -42.5918, -18.4127, -4.6069,
         -18.7334]
    assert round(output['z-score'][1], 4) == a[1]   
    assert round(output['z-score'][2], 4) == a[2]
    assert round(output['z-score'][3], 4) == a[3]
    assert round(output['z-score'][4], 4) == a[4]
    assert round(output['z-score'][5], 4) == a[5]
    assert round(output['z-score'][6], 4) == a[6]
    assert round(output['z-score'][7], 4) == a[7]
    assert round(output['z-score'][8], 4) == a[8]
    assert round(output['z-score'][9], 4) == a[9]
    assert round(output['z-score'][10], 4) == a[10]
    assert round(output['z-score'][11], 4) == a[11]
    assert round(output['z-score'][12], 4) == a[12]
    assert round(output['z-score'][13], 4) == a[13]
    assert round(output['z-score'][14], 4) == a[14]
