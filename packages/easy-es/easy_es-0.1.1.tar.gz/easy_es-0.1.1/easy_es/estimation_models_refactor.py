from typing import Union, List

import pandas as pd
from pandas.core.api import DataFrame as DataFrame
import numpy as np
import statsmodels.api as sm
from sklearn.base import BaseEstimator, RegressorMixin

# from .base import BasePandasRegressor
from .data_loader import load_daily_factors
from .base import LogMixin, ColumnNameHandler


class BaseEstimator(BaseEstimator, RegressorMixin, LogMixin, ColumnNameHandler):
    def __init__(self, feature_cols: List[str]):
        self.feature_cols = feature_cols

    def fit(self, x: pd.DataFrame, y=None) -> 'BaseEstimator':
        return self
    
    def predict(self, x: pd.DataFrame) -> List[float]:
        raise NotImplementedError
    
    @property
    def resid(self) -> np.ndarray:
        raise NotImplementedError
    

class RegReturnEstimator(BaseEstimator):
    def __init__(self, feature_cols: List[str]):
        self.estimator = None
        self.feature_cols = feature_cols if isinstance(feature_cols, List) else [feature_cols]
    
    def fit(self, x: DataFrame, y=None) -> BaseEstimator:
        self.estimator = sm.OLS(
            x[self.ret_col], 
            sm.add_constant(x[self.feature_cols])
        ).fit()
        return self
    
    def predict(self, x: DataFrame) -> List[float]:
        return self.estimator.predict(sm.add_constant(x[self.feature_cols])).tolist()
    
    @property
    def resid(self) -> np.ndarray:
        if self.estimator:
            return self.estimator.resid
        return
    

class MAMReturnEstimator(BaseEstimator):
    def __init__(self):
        self.__resid = None
    
    @property
    def resid(self) -> float:
        return self.__resid

    def fit(self, x: pd.DataFrame, y=None) -> 'MAMReturnEstimator':
        self.__resid = (x[self.ret_col] - x[self.mkt_rf_col] - x[self.rf_col])**2
        return self
    
    def predict(self, x: pd.DataFrame) -> List[float]:
        return (x[self.mkt_rf_col] + x[self.rf_col]).tolist()
    



        




# class BasePandasRegressor(BaseEstimator, RegressorMixin, LogMixin, ColumnNameHandler):
#     def fit(self, x: pd.DataFrame, y=None):
#         return self
#     def predict(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
#         raise NotImplementedError
#     def fit_predict(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
#         return self.fit(x, y).predict(x, y)


# class BaseEstimator(BaseEstimator, RegressorMixin, LogMixin, ColumnNameHandler):
#     def __init__(self, feature_cols: Union[str, List[str]], estimation_days: int = 255, 
#                  gap_days: int = 50, window_before: int = 10, window_after: int = 10, 
#                  min_estimation_days: int = 100, five_factors: bool=False):
#         self.feature_cols = feature_cols if isinstance(feature_cols, list) else [feature_cols]
#         self.estimation_days = estimation_days
#         self.gap_days = gap_days
#         self.window_before = window_before
#         self.window_after = window_after
#         self.min_estimation_days = min_estimation_days
#         self.five_factors = five_factors
#         self.estimator = None
#         self.__factors_df = self.__load_factors()

#     def __load_factors(self) -> pd.DataFrame:
#         factors_df = load_daily_factors(self.five_factors)
#         factors_df.loc[:, self.feature_cols] = factors_df[self.feature_cols]/100
#         return factors_df
    
#     @property
#     def factors_df(self) -> pd.DataFrame:
#         return self.__factors_df
    
#     @property
#     def estimation_resid(self) -> float:
#         return self.estimator.resid if self.estimator is not None else None
    
#     def _fit_estimator(self, feature_df: pd.DataFrame):
#         self.estimator = sm.OLS(
#             feature_df[self.ret_col], 
#             sm.add_constant(feature_df[self.feature_cols])
#         ).fit()
    
#     def fit(self, x: pd.DataFrame, y=None):
#         feature_df = pd.merge(x, self.factors_df, on=self.date_col)
        
#         if any(c not in feature_df for c in self.feature_cols):
#             raise ValueError(f"Input data does not contain all required columns: {', '.join(self.feature_cols)}")
        
#         estimation_period = np.arange(
#             -(self.window_before+self.gap_days+self.estimation_days), 
#             -(self.window_before+self.gap_days), 
#             1)
#         train_df = feature_df[feature_df[self.offset_col].isin(estimation_period)].copy()
#         if train_df.shape[0] < self.min_estimation_days:
#             return self

#         self._fit_estimator(train_df)
#         return self

#     def predict_returns(self, event_df: pd.DataFrame) -> pd.Series:
#         raise NotImplementedError

#     def predict(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
#         if self.model is None:
#             return None
#         event_period = np.arange(-self.window_before, self.window_after + 1, 1)
#         event_df = x[
#             x[self.offset_col].isin(event_period)
#         ].copy()
#         # Predict normal returns and calculate other variables
#         event_df.sort_values(self.offset_col, inplace=True)
#         event_df.loc[:, self.pred_ret_col] = self.predict_returns(event_df)
#         event_df.loc[:, self.ar_col] = event_df[self.ret_col] - event_df[self.pred_ret_col]
#         event_df.loc[:, self.car_col] = event_df[self.ar_col].cumsum()
#         event_df.loc[:, self.sar_col] = event_df[self.ar_col] / self.estimation_resid.std()
#         event_df.loc[:, self.scar_col] = event_df[self.car_col] / (
#             self.estimation_resid.std() * np.sqrt(event_df.reset_index(drop=True).index+1))
#         event_df.loc[:, self.e_std_col] = self.estimation_resid.std()
#         return event_df
    

# class BaseRegressionEstimator(BaseEstimator):
#     def fit(self, x: pd.DataFrame, y=None):
#         feature_df = pd.merge(x, self.factors_df, on=self.date_col)
        
#         if any(c not in feature_df for c in self.feature_cols):
#             raise ValueError(f"Input data does not contain all required columns: {', '.join(self.feature_cols)}")
        
#         estimation_period = np.arange(
#             -(self.window_before+self.gap_days+self.estimation_days), 
#             -(self.window_before+self.gap_days), 
#             1)
#         train_df = feature_df[feature_df[self.offset_col].isin(estimation_period)].copy()
#         if train_df.shape[0] < self.min_estimation_days:
#             return self
#         self.model = sm.OLS(
#             train_df[self.ret_col], 
#             sm.add_constant(train_df[self.feature_cols])
#         ).fit()
#         self.estimation_resid = self.model.resid
#         return self
    
#     def predict_returns(self, event_df: pd.DataFrame) -> List[float]:
#         x = pd.merge(event_df, self.factors_df, on=self.date_col)
#         return self.model.predict(sm.add_constant(x[self.feature_cols])).tolist()


# class MAM(BaseEstimator):
#     """
#     Market-Adjusted estimator - calculated as difference between StockRet - MarketRet

#     Parameters
#     ----------
#     BaseEstimator : _type_
#         _description_
#     """
#     def __init__(self, **kwargs):
#         super().__init__(feature_cols=[self.mkt_rf_col, self.rf_col], **kwargs)
#         self.model = None
    
#     def _fit_estimator(self, feature_df: DataFrame):
#         return 
    
#     @property
#     def estimation_resid(self) -> float:
#         return self.estimator.resid if self.estimator is not None else None

#     def fit(self, x: pd.DataFrame, y=None) -> 'MAM':
#         feature_df = pd.merge(x, self.factors_df, on=self.date_col)
#         if any(c not in feature_df for c in self.feature_cols):
#             raise ValueError(f"Input data does not contain all required columns: {', '.join(self.feature_cols)}")
        
#         estimation_period = np.arange(
#             -(self.window_before+self.gap_days+self.estimation_days), 
#             -(self.window_before+self.gap_days), 
#             1)
#         train_df = feature_df[feature_df[self.offset_col].isin(estimation_period)].copy()
#         self.estimation_resid = (train_df[self.ret_col] - train_df[self.mkt_rf_col] - train_df[self.rf_col])**2
#         return self
    
#     def predict_returns(self, event_df: pd.DataFrame) -> List[float]:
#         x = pd.merge(event_df, self.factors_df, on=self.date_col, how='left')
#         return (x[self.mkt_rf_col] + x[self.rf_col]).tolist()


# class CAPM(BaseRegressionEstimator):
#     """
#     CAPM estimator - based on regression = alpha + Beta*(Mkt-Rf)
#     Parameters
#     ----------
#     BaseEstimator : _type_
#         _description_
#     """
#     def __init__(self, **kwargs):
#         super().__init__(feature_cols=[self.mkt_rf_col], **kwargs)
#         self.model = None

# class FF3(BaseRegressionEstimator):
#     """FF3 estimator - based on regression = alpha + Beta * (Mkt-Rf) + Beta2 * SMB + Beta3 * HML"""
#     def __init__(self, *args, **kwargs):
#         super().__init__(feature_cols=[self.mkt_rf_col, self.smb_col, self.hml_col], **kwargs)
#         self.model = None

# class FF5(BaseRegressionEstimator):
#     """FF5 estimator - based on regression = alpha + Beta * (Mkt-Rf) + Beta2 * SMB + Beta3 * HML + Beta4 * RMW + Beta5 * CMA"""
#     def __init__(self, *args, **kwargs):
#         super().__init__(feature_cols=[self.mkt_rf_col, self.smb_col, self.hml_col, self.rmw_col, self.cma_col], five_factors=True, **kwargs)
#         self.model = None
