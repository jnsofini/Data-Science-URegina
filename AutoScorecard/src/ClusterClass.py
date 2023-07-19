import json
import logging as log
from pathlib import Path

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from varclushi import VarClusHi

class Cluster(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        max_eigen=1,
        maxclus=None,
    ) -> None:
        # self.data = data
        self.max_eigen = max_eigen
        self.maxclus = maxclus

    def fit(self, x, y=None):
        self.clusters = VarClusHi(df=x, maxeigval2=self.max_eigen, maxclus=self.maxclus)
        return self

    def transform(self, x):
        file = Path("data/pipeline/auto-iv-table.csv")
        if file.is_file():
            iv_table = self.read_iv_table(file)
        else:
            iv_table = None
        self.cluster_table = self.get_clusters(iv_table)
        # self.cluster_table.to_csv("data/pipeline/cluster-iv-table.csv")
        self.selected_features = self.get_best_feature_from_each_cluster(
            cluster_table=self.cluster_table, feature="Variable"
        )
        cluster_table = self._indicated_selected(
            self.cluster_table, self.selected_features
        )
        cluster_table.to_csv("data/pipeline/cluster-iv-table.csv")
        return x[self.selected_features]

    @staticmethod
    def _indicated_selected(table, selected, features="Variable"):
        return table.assign(cluster_iv_selection=table[features].isin(selected))

    # def clustering(self, data):
    #     self.clusters = VarClusHi(
    #         df=data,
    #         maxeigval2=self.max_eigen,
    #         maxclus=self.maxclus
    #         )

    def get_clusters(self, iv_table=None):
        self.clusters.varclus()
        self.iv_table = iv_table
        if self.iv_table is None:
            log.info("Retriving clusters without IVs")
            return self.clusters.rsquare

        log.info("Retriving clusters with IV for each feature")
        return pd.merge(
            self.clusters.rsquare,
            self.iv_table,
            how="left",
            left_on="Variable",
            right_on="name",
        )

    @staticmethod
    def get_best_feature_from_each_cluster(
        cluster_table: pd.DataFrame, feature: str = "Variable"
    ):
        # The best feature from each cluster is the one with the min RS Ratio
        # from that cluster. If the feature with the highest IV is different
        # than the one with the highest RS Ratio, it is included as well.
        if "iv" in cluster_table.columns:
            highest_iv = cluster_table.loc[
                cluster_table.groupby(["Cluster"])["iv"].idxmax()
            ][feature].tolist()
        else:
            highest_iv = []

        lowest_rs_ratio = cluster_table.loc[
            cluster_table.groupby(["Cluster"])["RS_Ratio"].idxmin()
        ][feature].tolist()

        return list(set(highest_iv + lowest_rs_ratio))

    @classmethod
    def read_iv_table(cls, path: Path | str, cutoff: float = 0.0):
        # Read IV table from path and filter based on cutoff
        return pd.read_csv(path).query(f"iv >= {cutoff}")

    @classmethod
    def save(cls, data: dict, path):
        with open(path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=6)
