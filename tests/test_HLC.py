import risktests.Hosmer_Lemeshow_Chi_Square as HLC
import pytest
import pandas as pd
import numpy as np


def test_Hosmer_Lemeshow_Chi_Square():
    # Sampling the buckets randomly at fixed probabilities
    buckets = np.random.choice(a=["Bucket one", "Bucket two", "Bucket three", "Bucket four", "Bucket five"],
                               p=[0.15, 0.25, 0.05, 0.05, 0.5], size=1000)
    loan_status = np.random.choice(a=["default", "non-default"], p=[0.3, 0.7], size=1000)

    probs = []

    for i in range(len(buckets)):
        if buckets[i] == 'Bucket one':
            probs.append(0.15)
        elif buckets[i] == 'Bucket two':
            probs.append(0.25)
        elif buckets[i] == 'Bucket three':
            probs.append(0.05)
        elif buckets[i] == 'Bucket four':
            probs.append(0.05)
        elif buckets[i] == 'Bucket five':
            probs.append(0.5)

    probs = np.array(probs)

    loan_data = pd.DataFrame({'loan_bucket': buckets,
                              'loan_status': loan_status,
                              'PD': probs})
    output = HLC.Hosmer_Lemeshow_Chi_Square(data=loan_data, buckets_col='loan_bucket', loan_statuses_col='loan_status', PDs_col='PD', alpha=0.05, verbose=True)

    assert round(output.p_value, 3) == 0.000
    assert round(output.HLC_stat, 3) == 316.176
    assert round(output.critical_value, 3) == 7.815
    assert output.dof == 3




