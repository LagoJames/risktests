import risktests.Expected_Loss_Best_Estimate_t_test as ELBE
import pytest
import pandas as pd
import os


def test_ELBE():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.abspath(os.path.join(BASE_DIR, 'synthetic_pd.xlsx'))
    df = pd.read_excel(test_file)

    output = ELBE.elbe_t_test(df=df, LGD_col='LGD', ELBE_col='ELBE')
    assert output[0] == 373028
    assert round(output[1], 3) == 6581.532
    assert round(output[2], 3) == 6581.027
    assert round(output[3], 5) == 0.53385
    assert round(output[4], 3) == 333868.036
    assert round(output[5], 5) == 0.59344
