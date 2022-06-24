import matplotlib.pyplot as plt
from sklearn.metrics import auc


def lcr(df, LGD_col, EAD_col, pred_LGD_col):
    """
    Parameters
    ----------
    df: array-like, at least 2D
        data
    LGD_col: string
        name of column with Loss Given Default (LGD)
    EAD_col: string
        name of column with Exposure at Default (EAD)
    pred_LGD_col: string
        name of column with predicted LGDs

    Returns
    -------
    lcr : float
        Calculated value of LCR and a plot

    References
    ----------
    [1] BIS. (2005). Studies on the Validation of Internal Rating Systems

    (revised). https://www.bis.org/publ/bcbs_wp14.htm

    Examples
    --------
    >>res = Speigelhalter_Normal_test(
    df=df,
    EAD_col='ratings',
    LGD_col='default_flag',
    pred_LGD_col='prob_default')
    >>print(res)
    """
    if df.empty:
        raise TypeError('No data provided!')
    if LGD_col is None:
        raise TypeError('No column name for defaults provided')
    if EAD_col is None:
        raise TypeError('No column name for ratings provided')
    if pred_LGD_col is None:
        raise TypeError('No column name for PDs provided.')

    # Checking that the correct datatype
    if not isinstance(LGD_col, str):
        raise TypeError('LGD_col not of type string')
    if not isinstance(EAD_col, str):
        raise TypeError('EAD_col not of type string')
    if not isinstance(pred_LGD_col, str):
        raise TypeError('pred_LGD_col not of type string')

    # Check if the correct column names have been provided
    if LGD_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(LGD_col))
    if EAD_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(EAD_col))
    if pred_LGD_col not in df.columns:
        raise ValueError('{} not a column in the df'.format(pred_LGD_col))

    # Check the data for missing values
    if df[EAD_col].hasnans:
        raise ValueError('Missing values in {}'.format(EAD_col))
    if df[LGD_col].hasnans:
        raise ValueError('Missing values in {}'.format(LGD_col))
    if df[pred_LGD_col].hasnans:
        raise ValueError('Missing values in {}'.format(pred_LGD_col))
    df['loss'] = df[EAD_col] * df[LGD_col]
    # Model loss capture curve

    df2 = df.sort_values(by=pred_LGD_col, ascending=False)
    df2['cumulative_loss'] = df2.cumsum()['loss']
    df2['cumulative_loss_capture_percentage'] = df2.cumsum()['loss']/df2.loss.sum()
    auc_curve1 = auc([i for i in range(len(df2))], df2.cumulative_loss_capture_percentage)
    random_auc1 = 0.5 * len(df2) * 1
    # Ideal loss capture curve
    df3 = df.sort_values(by=LGD_col, ascending=False)
    df3['cumulative_loss'] = df3.cumsum()['loss']
    df3['cumulative_loss_capture_percentage'] = df3.cumsum()['loss']/df3.loss.sum()
    auc_curve2 = auc([i for i in range(len(df3))], df3.cumulative_loss_capture_percentage)
    random_auc2 = 0.5 * len(df3) * 1
    loss_capture_ratio = (auc_curve1 - random_auc1)/(auc_curve2 - random_auc2)
    # loss capture curve
    plt.title('Loss Capture Curve')
    plt.plot([i for i in range(len(df2))], df2.cumulative_loss_capture_percentage, 'b', label='Model Output')
    plt.plot([i for i in range(len(df3))], df3.cumulative_loss_capture_percentage, 'g', label='Ideal Output')
    plt.legend(loc = 'lower right')
    plt.plot([0, len(df2)], [0, 1],'r--')
    plt.xlim([0, len(df2)])
    plt.ylim([0, 1])
    plt.ylabel('Actual Loss Curve(%)')
    plt.xlabel('Ordered Population(Worst to Best)')
    plt.show()
    return 'loss capture ratio is equal to ' + str(abs(round(loss_capture_ratio, 2)))