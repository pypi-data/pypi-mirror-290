from typing import cast

import networkx as nx
import pandas as pd
from pandas._typing import Suffixes

from langchain_graphrag.types.graphs.community import (
    Community,
    CommunityDetectionResult,
    CommunityId,
    CommunityLevel,
)


class CommunitiesTableGenerator:
    def _unpack_nodes(
        self,
        level: CommunityLevel,
        communities: dict[CommunityId, Community],
        graph: nx.Graph,
    ) -> pd.DataFrame:
        records = []

        for community_id, community in communities.items():
            for node in community.nodes:
                node_data = graph.nodes[node.name]
                records.append(
                    {
                        "label": node.name,
                        "cluster": community_id,
                        "level": level,
                        **node_data,
                    }
                )

        return pd.DataFrame.from_records(records)

    def _unpack_edges(self, level: CommunityLevel, graph: nx.Graph) -> pd.DataFrame:
        records = [
            {
                "level": level,
                "source": source_id,
                "target": target_id,
                **(edge_data or {}),
            }
            for source_id, target_id, edge_data in graph.edges(data=True)
        ]
        return pd.DataFrame.from_records(records)

    def _make_all_clusters(self, graph_nodes: pd.DataFrame) -> pd.DataFrame:
        grouped = graph_nodes.groupby(
            ["cluster", "level"],
            sort=False,
        )
        output = cast(pd.DataFrame, grouped.agg({"cluster": "first"}))
        output.rename(columns={"cluster": "id"}, inplace=True)
        output.columns = ["id"]
        return output.reset_index()

    def _make_cluster_relationships(
        self,
        combined_clusters: pd.DataFrame,
    ) -> pd.DataFrame:
        grouped = combined_clusters.groupby(
            ["cluster", "level_1"],
            sort=False,
        )

        def array_agg_distinct(series: pd.Series) -> list[pd.Series]:
            return list(series.unique())

        is_list = isinstance(combined_clusters.iloc[0]["text_unit_ids_1"], list)

        def array_agg_distinct_check_list(series: pd.Series) -> list[pd.Series]:
            mod_series = series.apply(lambda x: ",".join(x)) if is_list else series
            return list(mod_series.unique())

        aggregations = {
            "id_2": array_agg_distinct,
            "text_unit_ids_1": array_agg_distinct_check_list,
        }

        output = cast(pd.DataFrame, grouped.agg(aggregations))
        output.rename(columns={"id_2": "relationship_ids"}, inplace=True)
        output.rename(columns={"text_unit_ids_1": "text_unit_ids"}, inplace=True)

        return output.reset_index()

    def run(
        self,
        detection_result: CommunityDetectionResult,
        graph: nx.Graph,
    ) -> pd.DataFrame:
        levels = list(detection_result.communities.keys())

        # TODO: Revisit - should be able to do
        # more efficiently
        graph_edges = pd.concat([self._unpack_edges(level, graph) for level in levels])

        graph_nodes = pd.concat(
            [
                self._unpack_nodes(level, communities, graph)
                for level, communities in detection_result.communities.items()
            ]
        )

        # all_clusters
        all_clusters = self._make_all_clusters(graph_nodes)

        # Make merged dataframes

        # using label from graph_nodes & source from graph_edges
        source_clusters = graph_nodes.merge(
            graph_edges,
            left_on="label",
            right_on="source",
            how="inner",
            suffixes=cast(Suffixes, ["_1", "_2"]),
            indicator=True,
        )

        # using label from graph_nodes & target from graph_edges
        target_clusters = graph_nodes.merge(
            graph_edges,
            left_on="label",
            right_on="target",
            how="inner",
            suffixes=cast(Suffixes, ["_1", "_2"]),
            indicator=True,
        )

        # concatenate both the clusters
        concatenated_clusters = pd.concat(
            [source_clusters, target_clusters], ignore_index=True
        )

        # we filter based on level_1 and level_2
        # filter based on level_1 and level_2 being equal

        combined_clusters = concatenated_clusters[
            concatenated_clusters["level_1"] == concatenated_clusters["level_2"]
        ]

        cluster_relationships = self._make_cluster_relationships(combined_clusters)

        # join all_clusters with cluster_relationships
        all_custers_relationships = all_clusters.merge(
            cluster_relationships,
            left_on="id",
            right_on="cluster",
            how="inner",
            suffixes=cast(Suffixes, ["_1", "_2"]),
            indicator=True,
        )

        # TODO: Revist this one
        # again filter based on level and level_1
        filtered_clustered_relationships = all_custers_relationships[
            all_custers_relationships["level"] == all_custers_relationships["level_1"]
        ].reset_index(drop=True)

        # we need add a title to the frame
        # Community id
        filtered_clustered_relationships["title"] = filtered_clustered_relationships[
            "id"
        ].apply(lambda x: f"Community {x}")

        # and finally we select the columns we need
        return filtered_clustered_relationships[
            [
                "id",
                "title",
                "level",
                "relationship_ids",
                "text_unit_ids",
            ]
        ]
