import risktests.Jeffreys_test as JT
import pytest
import pandas as pd
import os

def test_JT():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.abspath(os.path.join(BASE_DIR, 'synthetic_pd.xlsx'))
    df = pd.read_excel(test_file)

    output = JT.jeffreys_test(df=df,ratings_col='ratings', PDs_col='prob_default', defaults_col='predicted_flag')
    x = [0.00000, 0.00000, 0.00000, 0.00000, 0.45443, 0.99992, 0.99992, 0.99994, 0.99994, 0.99995, 0.99994, 0.99995, 0.99992, 0.99990, 0.72264]
    assert round(output['P-Value'][0],5) == x[0]
    assert round(output['P-Value'][1],5) == x[1]
    assert round(output['P-Value'][2],5) == x[2]
    assert round(output['P-Value'][3],5) == x[3]
    assert round(output['P-Value'][4],5) == x[4]
    assert round(output['P-Value'][5],5) == x[5]
    assert round(output['P-Value'][6],5) == x[6]
    assert round(output['P-Value'][7],5) == x[7]
    assert round(output['P-Value'][8],5) == x[8]
    assert round(output['P-Value'][9],5) == x[9]
    assert round(output['P-Value'][10],5) == x[10]
    assert round(output['P-Value'][11],5) == x[11]
    assert round(output['P-Value'][12],5) == x[12]
    assert round(output['P-Value'][13],5) == x[13]