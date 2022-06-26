import InformationValue as IV
import pandas as pd
import pytest


def test_IV():
    # import dataset
    df = pd.read_excel('synthetic_pd.xlsx')
    # calculate values
    output = IV.Information_value(
        df=df,
        ratings_col='ratings',
        defaults_col='default_flag',
        PDs_col='prob_default')
    # Manually import excel computed values
    x = [0.997138, 0.273416, 0.072754, 0.012484, 0.005889, 0.03132, 0.047055,
         0.091188, 0.084132, 0.110719, 0.134859, 0.184387, 0.148909, 0.139378,
         2.333628]
    # check that output is the same as corresponding excel value
    assert round(output['IV'][0], 6) == x[0]
    assert round(output['IV'][1], 6) == x[1]
    assert round(output['IV'][2], 6) == x[2]
    assert round(output['IV'][3], 6) == x[3]
    assert round(output['IV'][4], 6) == x[4]
    assert round(output['IV'][5], 6) == x[5]
    assert round(output['IV'][6], 6) == x[6]
    assert round(output['IV'][7], 6) == x[7]
    assert round(output['IV'][8], 6) == x[8]
    assert round(output['IV'][9], 6) == x[9]
    assert round(output['IV'][10], 6) == x[10]
    assert round(output['IV'][11], 6) == x[11]
    assert round(output['IV'][12], 6) == x[12]
    assert round(output['IV'][13], 6) == x[13]