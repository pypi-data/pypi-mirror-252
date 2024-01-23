from typing import Union, List

import pandas as pd
from pandas.core.api import DataFrame as DataFrame
import numpy as np
import statsmodels.api as sm
from sklearn.base import BaseEstimator, RegressorMixin

# from .base import BasePandasRegressor
from .data_loader import load_daily_factors
from .base import LogMixin, ColumnNameHandler


class BaseReturnsEstimator(BaseEstimator, RegressorMixin, LogMixin, ColumnNameHandler):
    def __init__(self):
        self.__resid = None

    def fit(self, x: pd.DataFrame, y=None) -> 'BaseEstimator':
        raise NotImplementedError
    
    def predict(self, x: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
    
    @property
    def resid(self):
        return self.__resid
    

class MAMEstimator(BaseReturnsEstimator):
    def fit(self, x: DataFrame, y=None) -> BaseEstimator:
        self.__resid = (x[self.ret_col] - x[self.mkt_rf_col] - x[self.rf_col])**2
        return self
    
    def predict(self, x: DataFrame) -> List[float]:
        return (x[self.mkt_rf_col] + x[self.rf_col]).tolist()
    

class RegReturnsEstimator(BaseReturnsEstimator):
    def __init__(self, feature_cols: List[str]):
        super().__init__()
        self.feature_cols = feature_cols
        self.reg_model = None
    
    def fit(self, x: DataFrame, y=None) -> BaseEstimator:
        self.reg_model = sm.OLS(
            x[self.ret_col], 
            sm.add_constant(x[self.feature_cols])
        ).fit()
        self.__resid = self.reg_model.resid
        return self
    
    def predict(self, x: DataFrame) -> DataFrame:
        return self.reg_model.predict(sm.add_constant(x[self.feature_cols])).tolist()
    

class CAPM(RegReturnsEstimator):
    """
    CAPM estimator - based on regression = alpha + Beta*(Mkt-Rf)
    Parameters
    ----------
    BaseEstimator : _type_
        _description_
    """
    def __init__(self, **kwargs):
        super().__init__(feature_cols=[self.mkt_rf_col], **kwargs)
        self.model = None

class FF3(RegReturnsEstimator):
    """FF3 estimator - based on regression = alpha + Beta * (Mkt-Rf) + Beta2 * SMB + Beta3 * HML"""
    def __init__(self, *args, **kwargs):
        super().__init__(feature_cols=[self.mkt_rf_col, self.smb_col, self.hml_col], **kwargs)
        self.model = None

class FF5(RegReturnsEstimator):
    """FF5 estimator - based on regression = alpha + Beta * (Mkt-Rf) + Beta2 * SMB + Beta3 * HML + Beta4 * RMW + Beta5 * CMA"""
    def __init__(self, *args, **kwargs):
        super().__init__(feature_cols=[self.mkt_rf_col, self.smb_col, self.hml_col, self.rmw_col, self.cma_col], five_factors=True, **kwargs)
        self.model = None
    
    