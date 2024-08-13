from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from category_encoders import BinaryEncoder


from sklearn.utils import estimator_html_repr

import os
from joblib import dump
import itertools
from pathlib import Path


try:
    from AutoPrep.pipeline_control import PipelineControl
except ImportError:
    from pipeline_control import PipelineControl
# from pipeline_configuration import PipelinesConfiguration



from sklearn import set_config
set_config(transform_output="pandas")



class AutoPrep():
    def __init__(
        self,
        datetime_columns: list = None,
        nominal_columns: list = None,
        ordinal_columns: list = None,
        exclude_columns: list = None,
        pattern_recognition_columns: list = None,
        drop_columns_no_variance: bool = True,
        ):

        self.datetime_columns = datetime_columns
        self.nominal_columns = nominal_columns
        self.ordinal_columns = ordinal_columns
        self.exclude_columns = exclude_columns

        self.pattern_recognition_columns = pattern_recognition_columns
        
        self.drop_columns_no_variance = drop_columns_no_variance


        self._pipeline_structure = None
        self._fitted_pipeline = None

        self._df = None
        self._df_preprocessed = None

    @property
    def df(self):
        return self._df
    @df.setter
    def df(self, new_df):
        if isinstance(new_df,pd.DataFrame) is False:
            raise ValueError("New value of pipeline has to be an object of type Dataframe!")
        self._df = new_df

    @property
    def pipeline_structure(self):
        return self._pipeline_structure   
    @pipeline_structure.setter
    def pipeline_structure(self, new_pipeline):
        if isinstance(new_pipeline, Pipeline) is False:
            raise ValueError("New value of pipeline has to be an object of type Pipeline!")
        self._pipeline_structure = new_pipeline


    @property
    def fitted_pipeline(self):
        return self._fitted_pipeline



    def preprocess(
            self, 
            df: pd.DataFrame
    ) -> pd.DataFrame:
        self._df = df.copy()

        self._df_preprocessed = self.remove_excluded_columns(df = self._df)
        
        self._fitted_pipeline = self.fit_pipeline_structure(df = self._df_preprocessed)

        self._df_preprocessed =  self._fitted_pipeline.transform(self._df_preprocessed)

        self._df_preprocessed = self.remove_no_variance_columns(
            df=self._df_preprocessed,
            remove_no_variance=self.drop_columns_no_variance,
            name="Preprocessed"
        )

        return self._df_preprocessed

        



    def fit_pipeline_structure(self, df):
        self._pipeline_structure = PipelineControl(
            datetime_columns = self.datetime_columns,
            nominal_columns = self.nominal_columns,
            ordinal_columns = self.ordinal_columns,
            pattern_recognition_columns = self.pattern_recognition_columns
        )

        self._pipeline_structure = self._pipeline_structure.pipeline_configuration()

        try:
            return self._pipeline_structure.fit(df)
        except TypeError as e:
            message = (
                "Please check if your data contains datetime columns.\n"
                "If it does, ensure they are specified using the 'datetime_columns' parameter.\n"
                "when initializing the AutoPrepAD object.\n"
            )

            raise DatetimeException(f"{e}\n\n\n{message}")
        
        except Exception as e:
            print(self.df.isna().sum(), "\n", e, "\n")
            raise







        
    def remove_excluded_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes specified columns from the dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataframe.

        Returns
        -------
        pd.DataFrame
            The dataframe with specified columns removed.
        """
        df_modified = df.copy()
        if self.exclude_columns is not None:
            for col in self.exclude_columns:
                try:
                    df_modified.drop([col], axis=1, inplace=True)
                except Exception as e:
                    print(e)
        return df_modified


    def remove_no_variance_columns(
            self, df, remove_no_variance=False, name="Preprocessed"
        ) -> (pd.DataFrame, pd.DataFrame):
            

            df_cols_no_variance = df.loc[:, df.std() == 0.0].columns
            print("No Variance in follow Train Columns: ", df_cols_no_variance)

            df_cols_only_nans = df.columns[df.isna().any()]
            print("Only NaNs in follow Train Columns: ", df_cols_only_nans)

            print(f"Shape {name} before drop: {df.shape}")


            if remove_no_variance == True:
                df_dropped = df.drop(df_cols_no_variance, axis=1)

                print(f"Shape {name} after drop: {df_dropped.shape}\n")
                print(f"Check NaN {name}: {df_dropped.columns[df_dropped.isna().any()].tolist()}")
                print(f"Check inf {name}: {df_dropped.columns[np.isinf(df_dropped).any()].tolist()}")
                return df_dropped
            else:
                return df


    def visualize_pipeline_structure_html(self, filename="./visualization/PipelineDQ"):
        """
        Save the pipeline structure as an HTML file.

        This method creates the necessary directories (if they do not already exist) 
        and saves a visual representation of the pipeline structure to an HTML file.

        Parameters
        ----------
        filename : str, optional
            The path and filename for the HTML file. The default is "./visualization/PipelineDQ".

        Returns
        -------
        None
            This function does not return any value. It only saves the HTML file.

        """
        Path("./visualization").mkdir(parents=True, exist_ok=True)
        Path("./visualization/Pipeline").mkdir(parents=True, exist_ok=True)
        with open(file=f"{filename}.html", mode="w", encoding="utf-8") as f:
            f.write(estimator_html_repr(self.pipeline_structure))
            f.close()


class DatetimeException(Exception):
    """
    Exception raised for errors in the datetime handling in the pipeline.

    Attributes
    ----------
    message : str
        Explanation of the error.
    """
    pass






