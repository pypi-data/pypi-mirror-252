import re

import numpy as np
import pandas as pd
import networkx as nx

from matplotlib import pyplot as plt

from .config import RENDERING_DPI, MAPPING_MATCHER
from .types_constants import Sheet, Kind, Node


class HazardMap:
    def __init__(self, mapping_table_file: str):
        self.parse_workbook_filename(mapping_table_file)

        self.graph = nx.Graph()

    def parse_workbook_filename(self, mapping_table_file: str):
        self.MAPPING_TABLE_FILE = mapping_table_file

        workbook_filename_parts = mapping_table_file.split('.')
        if workbook_filename_parts[-1] == 'xlsx': 
            self.WORKBOOK_NAME = '.'.join(workbook_filename_parts[:-1])
        else:
            raise Exception('Please pass an xlsx file')

    def extract_sheet_mappings(self, sheets: list[Sheet]):
        for sheet in sheets:
            df = pd.read_excel(self.MAPPING_TABLE_FILE, sheet.name, index_col=0)
            if sheet.transpose: df = df.T

            df.apply(self._extract_individual_mappings, axis=1)

    def _extract_individual_mappings(self, row: pd.Series):
        map_from = Node.from_str(row.name)

        row = row.dropna()
        mapped = row[row.str.match(MAPPING_MATCHER)].index.str.strip().to_list()
        mapped_typed = [Node.from_str(node_str) for node_str in mapped]
        
        for map_to in mapped_typed: self.graph.add_edge(map_from, map_to)

    def write_to_file(self):
        with pd.ExcelWriter(f'{self.WORKBOOK_NAME}-hazard_log_format.xlsx') as writer:
            for hazard in self.filter_node_set_for_kind(
                self.graph.nodes, 
                Kind.HAZARD,
            ):
                cause_control_mappings = []
                for cause in self.filter_node_set_for_kind(
                    self.graph[hazard], 
                    Kind.CAUSE,
                ):
                    for control in self.filter_node_set_for_kind(
                        self.graph[cause], 
                        Kind.CONTROL,
                    ):
                        cause_control_mappings.append((cause.to_str(), control.to_str()))
                df = (
                    pd.DataFrame(
                        data=cause_control_mappings, 
                        columns=['cause', 'control'],
                    )
                    .set_index('cause', append=True)
                    .reorder_levels([1, 0])
                    .to_excel(writer, sheet_name=hazard.to_str())
                )

    def filter_node_set_for_kind(self, node_set: set, kind: Kind) -> list[Node]:
        return sorted([node for node in node_set if node.kind == kind])

    def draw_graph(self) -> (plt.Figure, plt.Axes):
        self.fig, self.ax = plt.subplots(
            frameon=False,
            figsize=(9, 7),
            dpi=RENDERING_DPI,
        )
        self.ax.axis('off')
    
        nx.draw_networkx(
            self.graph,
            pos=nx.kamada_kawai_layout(self.graph),
            node_color=[
                KIND_COLOURS.get(node.kind, '#53676c') 
                for node in self.graph.nodes
            ],
            labels={node: node.to_str() for node in self.graph.nodes},
            node_size=self._define_node_sizes((100, 250)),
            font_size=3,
            alpha=0.9,
            edge_color=(0.5, 0.5, 0.5, 0.9),
            width=0.5,
            ax=self.ax,
        )

        return self.fig, self.ax

    def _define_node_sizes(
        self, 
        size_limits: tuple[float, float],
    ) -> list[float]:
        degrees = self.graph.degree()
        large_connect = np.percentile(
            [n_connections for node, n_connections in degrees],
            97,
        )
        add_size_per_connect = (size_limits[1] - size_limits[0]) / large_connect

        return [
            min([
                size_limits[0] + add_size_per_connect * n_connections,
                size_limits[1],
            ])
            for node, n_connections in degrees
        ]

    def save_graph(self): 
        if not hasattr(self, 'fig'):
            self.draw_graph()

        filename = (
            f'{self.WORKBOOK_NAME}'
            '-graph_rendering'
            f'-{str(hash(self.graph))[-4:]}'
            '.png'
        )

        print(f'Saving a rendering of the graph as "{filename}"...')
        plt.savefig(filename, transparent=True, dpi=RENDERING_DPI)
