import risktests.Concentration_of_Rating_Grades as RC
import pytest
import pandas as pd
import os


def test_RC():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.abspath(os.path.join(BASE_DIR, 'synthetic_pd.xlsx'))
    df = pd.read_excel(test_file)

    output = RC.ratings_concentration(df=df, initial_ratings_col='ratings', final_ratings_col='ratings2')
    assert round(output[0], 6) == 8e-06
    assert round(output[1], 6) == 0.020336
    assert round(output[2], 6) == 1.0
    assert round(output[3], 6) == 373028
