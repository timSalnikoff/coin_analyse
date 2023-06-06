import numpy as np
from scipy import stats


class RegResult:
    def __init__(self, slope, intercept, is_valid):
        self.slope = slope
        self.intercept = intercept
        self.is_valid = is_valid


class SeriesRegression:
    def __init__(self, p_value=0.05, accepted_r=0.5):

        self.influence = np.array([])
        self.influenced = np.array([])

        self.p_value = p_value
        self.accepted_r = accepted_r

    def add_influence(self, val):
        self.influence = np.append(val,
                                   self.influence)

    def add_influenced(self, val):
        self.influenced = np.append(val,
                                    self.influenced)

    def corr(self):
        try:
            slope, intercept, r, p, se = stats.linregress(
                x=self.influence,
                y=self.influenced)

            is_valid = abs(r) > self.accepted_r and p <= self.p_value

            return RegResult(slope, intercept, is_valid)

        except Exception as e:
            return None
