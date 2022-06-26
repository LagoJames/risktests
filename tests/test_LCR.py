import Loss_Coverage_Ratio as LCR
import pandas as pd
import pytest


def test_LCR():
    df = pd.read_excel("synthetic_pd.xlsx")
    output = LCR.lcr(
        df=df,
        LGD_col='LGD',
        EAD_col='EAD', pred_LGD_col='PRED_LGD')
    assert round(output, 2) == 1.00
