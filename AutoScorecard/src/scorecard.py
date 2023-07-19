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

from ClusterClass import Cluster

log.basicConfig(format='%(levelname)s:%(message)s', encoding='utf-8', level=log.DEBUG)

TARGET: str = "RiskPerformance"
SPECIAL_CODES = [-9]
MISSING = [-99_000_000]
MAX_EIGEN = 0.7


def variable_reduction_pipeline(
    categorical_features: list[str],
    binning_features: list[str],
    binning_fit_params=None,
):
    binning_process = BinningProcess(
        categorical_variables=categorical_features,
        variable_names=binning_features,
        binning_fit_params=binning_fit_params,
        # This is the prebin size that should make the feature set usable
        min_prebin_size=10e-5,
        special_codes=SPECIAL_CODES,
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


def model_pipeline(pipe):
    scaling_method: str = "pdo_odds"
    # scaling_method_data = {
    #     "min": 350,
    #     "max": 850,
    # }
    scaling_method_data = {
        "pdo": 30,
        "odds": 20,
        "scorecard_points": 750,
    }
    return Scorecard(
        binning_process=pipe["binning"],
        estimator=LogisticRegression(),
        scaling_method=scaling_method,
        scaling_method_params=scaling_method_data,
        intercept_based=True,
        reverse_scorecard=False,
        rounding=True,
    )


def get_data_and_columns(data_path="data"):
    # data_path = "data"
    x_train = pd.read_parquet(path=os.path.join(data_path, "X_train.parquet"))
    y_train = (
        pd.read_parquet(path=os.path.join(data_path, "y_train.parquet"))
        .astype("int8")
        .values.reshape(-1)
    )

    categorical_columns = (
        x_train.select_dtypes(include=["object", "category", "string"]).columns.values
    ).tolist()
    features = x_train.columns.to_list()

    return x_train, y_train, features, categorical_columns


def save_pipeline_artifacts(pipe, scorecard):
    scorecard.save("data/pipeline/model.pkl")
    pipe["binning"].summary().to_csv("data/pipeline/auto-iv-table.csv")
    scorecard.table(style="detailed").round(3).to_csv(
        "data/pipeline/scorecard-table.csv"
    )
    # with open("data/pipeline/pipeline.pkl", "wb") as f:
    #     pickle.dump(obj=pipe, file=f)


def main():
    data_path = "data"
    x_train, y_train, features, categorical_columns = get_data_and_columns(
        data_path=data_path
    )

    reductor_pipeline = variable_reduction_pipeline(
        categorical_features=categorical_columns, binning_features=features
    )
    reductor_pipeline.fit(X=x_train, y=y_train)

    scorecard_model = model_pipeline(reductor_pipeline)
    scorecard_model.fit(X=x_train, y=y_train)

    # Save artifacts
    save_pipeline_artifacts(pipe=reductor_pipeline, scorecard=scorecard_model)

    return scorecard_model, scorecard_model.table(style="detailed").round(3)


if __name__ == "__main__":
    model, model_table = main()
    # model_table.to_csv("auto-scorecard-model.csv")
    print(model_table)
