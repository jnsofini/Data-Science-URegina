import json
import logging as log
import os
import pickle
from pathlib import Path

import pandas as pd
from optbinning import BinningProcess, Scorecard
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import RFECV, VarianceThreshold
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from varclushi import VarClusHi

from .ClusterClass import Cluster

log.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=log.DEBUG)

TARGET: str = "RiskPerformance"
SPECIAL_CODES = [-9, -8, -7]
MISSING = [-99_000_000]
MAX_EIGEN = 0.7


def variable_reduction_pipeline(
    categorical_features: list[str],
    binning_features: list[str],
    binning_fit_params=None,
) -> Pipeline:
    """Create a scikit-learn pipeline for feature reduction using clustering.

    Args:
        categorical_features (list[str]): List of names of categorical features.
        binning_features (list[str]): List of names of features to apply binning.
        binning_fit_params (dict, optional): Fit parameters for binning process. Defaults to None.

    Returns:
        Pipeline: A scikit-learn pipeline for feature reduction.

    """
    binning_process = BinningProcess(
        categorical_variables=categorical_features,
        variable_names=binning_features,
        binning_fit_params=binning_fit_params,
        min_prebin_size=10e-5,  # The prebin size to make the feature set usable
        special_codes=SPECIAL_CODES,
        selection_criteria={"iv": {"min": 0.1}}
    )

    variance_reductor = VarianceThreshold().set_output(transform="pandas")
    clustering_process = Cluster(max_eigen=MAX_EIGEN)
    feature_selection = RFECV(
        LogisticRegression(max_iter=1000),
        cv=5,
        scoring="roc_auc",
        n_jobs=-1,
    )

    return Pipeline(
        [
            ('variance', variance_reductor),
            ('binning', binning_process),
            ('cluster', clustering_process),
            ('features', feature_selection),
        ]
    )


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


def get_data_and_columns(data_path="data"):
    """
    Load data and return the features and categorical columns.

    Args:
        data_path (str): Path to the data directory.

    Returns:
        x_train (pd.DataFrame): Training data features.
        y_train (numpy.ndarray): Training data target labels.
        features (list): List of all features.
        categorical_columns (list): List of categorical column names.
    """
    x_train = pd.read_parquet(os.path.join(data_path, "X_train.parquet"))
    y_train = pd.read_parquet(os.path.join(data_path, "y_train.parquet")).astype("int8").values.reshape(-1)

    categorical_columns = x_train.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    features = x_train.columns.tolist()

    return x_train, y_train, features, categorical_columns


def save_pipeline_artifacts(pipe, scorecard):
    """
    Save the pipeline artifacts such as the model, IV table, and scorecard table.

    Args:
        pipe (dict): Dictionary containing pipeline components.
        scorecard (scorecardpy.ScoreCard): Scorecard model.
    """
    Path("data/pipeline").mkdir(parents=True, exist_ok=True)
    scorecard.save("data/pipeline/model.pkl")
    pipe["binning"].summary().to_csv("data/pipeline/auto-iv-table.csv")
    scorecard.table(style="detailed").round(3).to_csv("data/pipeline/scorecard-table.csv")
    # with open("data/pipeline/pipeline.pkl", "wb") as f:
    #     pickle.dump(obj=pipe, file=f)


def main(data_path: str, binning_fit_params: dict) -> tuple:
    """
    Clustering and Variable Reduction Pipeline

    This function performs clustering and variable reduction on the input data using the "varclushi" library.
    The input data and corresponding target labels are obtained from the specified data_path.
    Categorical and non-categorical features are determined, and the clustering pipeline is constructed.
    The model pipeline is then created based on the selected features, and both pipelines are fitted to the data.
    The selected features are stored, and the scorecard model's table is generated.
    Finally, the pipelines and model are saved as artifacts.

    Args:
        data_path (str): Path to the data directory containing training data.
        binning_fit_params (dict): Parameters for binning fitting.

    Returns:
        tuple: A tuple containing the scorecard model, the scorecard model's table, and the clustering pipeline.
    """

    x_train, y_train, features, categorical_columns = get_data_and_columns(
        data_path=data_path
    )

    # Clustering and variable reduction pipeline
    reductor_pipeline = variable_reduction_pipeline(
        categorical_features=categorical_columns,
        binning_features=features,
        binning_fit_params=binning_fit_params
    )
    reductor_pipeline.fit(X=x_train, y=y_train)

    selected_columns = (
        reductor_pipeline["features"].feature_names_in_
        [reductor_pipeline["features"].support_]
    )
    categorical_columns = list(set(selected_columns).intersection(categorical_columns))

    # Model pipeline
    scorecard_model = model_pipeline(
        features=selected_columns,
        categorical_features=categorical_columns,
        binning_fit_params=binning_fit_params
    )
    scorecard_model.fit(X=x_train, y=y_train)

    # Save artifacts
    save_pipeline_artifacts(pipe=reductor_pipeline, scorecard=scorecard_model)

    return scorecard_model, scorecard_model.table(), reductor_pipeline


if __name__ == "__main__":
    model, model_table, dim_reduction = main(data_path="data", binning_fit_params=binning_fit_params)
    # model_table.to_csv("auto-scorecard-model.csv")
    print(model_table)
