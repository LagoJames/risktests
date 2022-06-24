"""The Hosmer-Lemeshow-Chi-squared test

    Created on 2022-06-08

    Author: Anton Treialt
    License: BSD(3-clause)

    NOTES
    -----

    This test measures the squared difference between forecasted and observed defaults on bucket level.

    The null hypotheisis makes two assumptions:
        -That the  forecasted default probabilities and the observed default rates are identically distributed, and;
        -that the defaults are independent.
    According to Blochwitz et al. (2006), under the assumptions the test statistic converges to a chi-square distribution with B-2 degrees of
    freedom if N (the number of observations) goes to infinity. Here B is the number of credit buckets.

    The hypotheses are:
        H0: The observed number of defaults is equal to the predicted number of defaults
        H1: The number of predicted and observed defaults are unequal.

    According to Tasche(2006), this test has several drawbacks. Firstly, for buckets with low number of facilities, there might be bad approximations.
    Second, independence between facilities (borrowers) is assumed which can be justified using a point-in-time approach. Thirdly, the model makes no
    distinction between deviations that are conservative or optimisitc even though they have different impact.Furthermore, the composed model test assumes
    independence, but does take into account the difference between conservative and optimistic deviations.

    REFERENCES
    ----------

    1.Blochwitz, S., Martin, M. R. W., & Wehn, C. S. (2006). Statistical Approaches to PD Validation.
        In B. Engelmann & R. Rauhmeier (Eds.), The Basel II Risk Parameters: Estimation, Validation, and Stress Testing
         (pp. 289–306). Springer. https://doi.org/10.1007/3-540-33087-9_13

    2.Tasche, D. (2006). Validation of internal rating systems and PD estimates (arXiv:physics/0606071).
        arXiv. http://arxiv.org/abs/physics/0606071
"""
import numpy as np
from scipy.stats import chi2
np.random.seed(10)
import os


#  THE TEST FUNCTION
class Hosmer_Lemeshow_Chi_Square:
    """
    Performs the Hosmer-Lemeshow Chi-Square test to validate credit data given the loan buckets, loan statuses and probabilitities of default.

    Assumes at least a 3D dataframe or 3D array-like dataset is passed to the arguement 'data' but requires the buckets column, loan status column and probability-of-default column names to be
    passed to the corresponding arguments.

    If verbose is set to True, the test results and interpretation will be printed, the default is False.

    alpha must be set otherwise a TypeError is raised.
    :param
    data : array_like, 3-D of higher
    buckets_col : name of column with buckets
    loan_status_col : name of column with loan statuses
    PDs_col : name of column with probabilities-of-default
    alpha: the tests level of significance. either 1%, 5% or 10%
    verbose: boolean. Prints the results if true.
    :return
    data: data passed into the function call
    bucket_levels: unique buckets in the data
    HLC_stat: Hosmer-Lemeshow test statistic
    alpha: the test's significance level
    p_value: the test's p-value
    verbose: boolean passed to function call to print results or not.
    critical_value: the critical value of the test
    dof: the test's degrees of freedom

    EXAMPLE
    -------
    >>import Hosmer_Lemeshow_Chi_Square as HLC
    >>import pandas as pd
    >>import numpy as np

    >># Sampling the buckets randomly at fixed probabilities
    >>buckets = np.random.choice(a=["Bucket one","Bucket two","Bucket three","Bucket four","Bucket five"], p = [0.15,0.25,0.05,0.05,0.5], size=1000)
    >>loan_status = np.random.choice(a=["default", "non-default"], p=[0.3,0.7], size=1000)

    >>probs = []

    >>for i in range(len(buckets)):
    >>    if buckets[i] == 'Bucket one':
    >>        probs.append(0.15)
    >>    elif buckets[i] == 'Bucket two':
    >>        probs.append(0.25)
    >>    elif buckets[i] == 'Bucket three':
    >>        probs.append(0.05)
    >>    elif buckets[i] == 'Bucket four':
    >>        probs.append(0.05)
    >>    elif buckets[i] == 'Bucket five':
    >>        probs.append(0.5)
    >>
    >>probs = np.array(probs)

    >>loan_data = pd.DataFrame({'loan_bucket': buckets,
    >>                          'loan_status': loan_status,
    >>                          'PD': probs})



    >>output = HLC.Hosmer_Lemeshow_Chi_Square(data=loan_data, buckets_col='loan_bucket', loan_statuses_col='loan_status', PDs_col='PD', alpha=0.05, verbose=True)
    >>output.HLC_stat # Shows the Hower-Lemeshow statistic
    >>output.p_value # Shows the p-value
    """


    def __init__(self,data, buckets_col, loan_statuses_col, PDs_col, alpha, verbose=False):

        # Checking for any missing data
        if data.empty:
            raise TypeError('No data provided!')
        if alpha == None:
            raise TypeError('No value provided for alpha. Please input a value for alpha.')
        if buckets_col == None:
            raise TypeError('No column name for buckets provided')
        if loan_statuses_col == None:
            raise TypeError('No column name for loan statuses provided')
        if PDs_col == None:
            raise TypeError('No column name for probabilities of default (PDs) provided')

        # Checking that the correct datatype
        if not isinstance(buckets_col, str):
            raise TypeError('buckets_col not of type string')
        if not isinstance(loan_statuses_col, str):
            raise TypeError('loan_statuses_col not of type string')
        if not isinstance(PDs_col, str):
            raise TypeError('PDs_col not of type string')
        if not isinstance(alpha, float):
            raise TypeError('alpha should be a float value')
        if not isinstance(verbose, bool):
            raise TypeError('verbose should be a boolean value')


        # Check if the correct column names have been provided
        if not buckets_col in data.columns:
            raise ValueError('{} not a column in the data provided'.format(buckets_col))
        if not loan_statuses_col in data.columns:
            raise ValueError('{} not a column in the data provided'.format(loan_statuses_col))
        if not PDs_col in data.columns:
            raise ValueError('{} not a column in the data provided'.format(PDs_col))

        # Check the data for missing values
        if data[buckets_col].hasnans:
            raise ValueError('There are missing values in the {} column'.format(buckets_col))
        if data[loan_statuses_col].hasnans:
            raise ValueError('There are missing values in the {} column'.format(loan_statuses_col))
        if data[PDs_col].hasnans:
            raise ValueError('There are missing values in the {} column'.format(PDs_col))

        buckets, loan_statuses, PDs = data[buckets_col], data[loan_statuses_col], data[PDs_col]
        self.data = np.asarray(data)
        self.bucket_levels = np.unique(buckets)
        self.alpha = alpha
        self.verbose = verbose


        def HLC_stat(self):
            """
            Calculates the Hosmer-Lemeshow Chi-square statistic
            :param self:
            :return: HLC statistic, degrees of freedom, probabilities of default in each bucket
            """

            Ni = []
            di = []
            pi = []
            HLC_stat = 0

            for i in range(len(self.bucket_levels)):
                mask = buckets == self.bucket_levels[i]
                Ni.append((mask).sum())
                di.append((loan_statuses[mask] == 'default').sum())
                pi.append(np.unique(PDs[mask]).item())

                HLC_stat = HLC_stat + (Ni[i] * pi[i] - di[i])**2/(Ni[i]*pi[i]*(1-pi[i]))

            self.PDs = pi

            df = len(self.bucket_levels) - 2
            self.df = df
            self.HLC_stat = HLC_stat
            return self.HLC_stat, self.df, self.PDs


        def HLC_cv(self, alpha):
            """
            Calculates the critical value of the Chi-square test using the degrees of freedom and alpha
            :param self:
            :param alpha:
            :return: critical value of the Chi-square test
            """
            critical_value = chi2.ppf(q=(1-self.alpha), df=self.df)
            self.critical_value = critical_value
            return self.critical_value


        def HLC_pvalue(self):
            """
            Calculate the p-value of the HLC statistic using the Chi-square cdf and the degrees of freedom
            :param self:
            :return: p-value of the HLC statistic
            """
            p_value = 1 - chi2.cdf(x=self.HLC_stat, df=self.df)
            self.p_value = p_value
            return self.p_value
        # Populating the HLC statistic object, the degrees of freedom object, the probabilities of default object, the critical values object
        # and the p-value objects

        self.HLC_stat, self.dof, self.PDs = HLC_stat(self)
        self.critical_value = HLC_cv(self, alpha=self.alpha)
        self.p_value = HLC_pvalue(self)

        if self.verbose == True:
            # print the results
            print("HLC_statistic=%.3f, df=%d, cv=%.3f, p=%.3f" % (self.HLC_stat, self.dof, self.critical_value, self.p_value))
            if self.p_value <= self.alpha:
                print("P-value <= alpha, therefore, the null hypothesis that the observed number of defaults is equal to the predicted number of defaults is rejected.")
            elif self.p_value>self.alpha:
                print(
                    "P-value > alpha, therefore, the null hypothesis that the observed number of defaults is equal to the predicted number of defaults fails to be rejected.")


