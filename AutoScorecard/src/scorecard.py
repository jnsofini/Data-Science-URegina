import json
import logging as log
import os
import pickle
from pathlib import Path

import pandas as pd
from optbinning import BinningProcess, Scorecard
from sklearn.linear_model import LogisticRegression


log.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=log.DEBUG)

TARGET: str = "RiskPerformance"
SPECIAL_CODES = [-9, -8, -7]
MISSING = [-99_000_000]
MAX_EIGEN = 0.7


def model_pipeline(features, categorical_features, binning_fit_params=None):
    """
    Creates a pipeline for building a Scorecard model using the provided features and categorical features.

    Args:
        features (list): List of feature names.
        categorical_features (list): List of categorical feature names.
        binning_fit_params (dict, optional): Parameters for the binning process. Defaults to None.

    Returns:
        Scorecard: A Scorecard model pipeline.

    """
    binning_process = BinningProcess(
        categorical_variables=categorical_features,
        variable_names=features,
        binning_fit_params=binning_fit_params,
        min_prebin_size=10e-5,
        special_codes=SPECIAL_CODES,
        selection_criteria={"iv":{"min": 0.1}}
    )
    scaling_method: str = "pdo_odds"
    scaling_method_data = {
        "pdo": 30,
        "odds": 20,
        "scorecard_points": 750,
    }
    return Scorecard(
        binning_process=binning_process,
        estimator=LogisticRegression(),
        scaling_method=scaling_method,
        scaling_method_params=scaling_method_data,
        intercept_based=True,
        reverse_scorecard=False,
        rounding=True,
    )



# def build(x_train, y_train, categorical_columns, reductor_pipeline, scorecard_model) -> tuple:
#     """
#     Clustering and Variable Reduction Pipeline

#     This function performs clustering and variable reduction on the input data using the "varclushi" library.
#     The input data and corresponding target labels are obtained from the specified data_path.
#     Categorical and non-categorical features are determined, and the clustering pipeline is constructed.
#     The model pipeline is then created based on the selected features, and both pipelines are fitted to the data.
#     The selected features are stored, and the scorecard model's table is generated.
#     Finally, the pipelines and model are saved as artifacts.

#     Args:
#         data_path (str): Path to the data directory containing training data.
#         binning_fit_params (dict): Parameters for binning fitting.

#     Returns:
#         tuple: A tuple containing the scorecard model, the scorecard model's table, and the clustering pipeline.
#     """

#     reductor_pipeline.fit(X=x_train, y=y_train)

#     selected_columns = (
#         reductor_pipeline["features"].feature_names_in_
#         [reductor_pipeline["features"].support_]
#     )
#     categorical_columns = list(set(selected_columns).intersection(categorical_columns))

#     scorecard_model.fit(X=x_train, y=y_train)

#     # Save artifacts
#     # save_pipeline_artifacts(pipe=reductor_pipeline, scorecard=scorecard_model)

#     return scorecard_model, reductor_pipeline
