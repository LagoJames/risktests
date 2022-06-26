import Traffic_lights_approach as TL
import pandas as pd
import pytest


def test_TL():
    df = pd.read_excel("synthetic_pd.xlsx")
    output = TL.traffic_lights(
        df=df,
        ratings_col='ratings',
        defaults_col='default_flag')
    a = ["Green", "Green", "Green", "Green", "Green",
         "Green", "Green", "Green", "Green", "Green",
         "Red", "Green", "Green", "Green"]
    assert output['Traffic Light'][1.0] == a[0]
    assert output['Traffic Light'][2.0] == a[1]
    assert output['Traffic Light'][3.0] == a[2]
    assert output['Traffic Light'][4.0] == a[3]
    assert output['Traffic Light'][5.0] == a[4]
    assert output['Traffic Light'][6.0] == a[5]
    assert output['Traffic Light'][7.0] == a[6]
    assert output['Traffic Light'][8.0] == a[7]
    assert output['Traffic Light'][9.0] == a[8]
    assert output['Traffic Light'][10.0] == a[9]
    assert output['Traffic Light'][11.0] == a[10]
    assert output['Traffic Light'][12.0] == a[11]
    assert output['Traffic Light'][13.0] == a[12]
    assert output['Traffic Light'][14.0] == a[13]
