from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

if TYPE_CHECKING:
    from typing_extensions import TypeIs

import medmodels as mm
from medmodels.medrecord.schema import Schema
from medmodels.medrecord.types import (
    EdgeTuple,
    Group,
    GroupInfo,
    NodeIndex,
    NodeTuple,
    PandasEdgeDataFrameInput,
    PandasNodeDataFrameInput,
    PolarsEdgeDataFrameInput,
    PolarsNodeDataFrameInput,
    is_edge_tuple,
    is_edge_tuple_list,
    is_node_tuple,
    is_node_tuple_list,
    is_pandas_edge_dataframe_input,
    is_pandas_edge_dataframe_input_list,
    is_pandas_node_dataframe_input,
    is_pandas_node_dataframe_input_list,
    is_polars_edge_dataframe_input,
    is_polars_edge_dataframe_input_list,
    is_polars_node_dataframe_input,
    is_polars_node_dataframe_input_list,
)

NodeInput = Union[
    NodeTuple,
    List[NodeTuple],
    PandasNodeDataFrameInput,
    List[PandasNodeDataFrameInput],
    PolarsNodeDataFrameInput,
    List[PolarsNodeDataFrameInput],
]
NodeInputWithGroup = Tuple[NodeInput, Group]


def is_node_input(value: object) -> TypeIs[NodeInput]:
    return (
        is_node_tuple(value)
        or is_node_tuple_list(value)
        or is_pandas_node_dataframe_input(value)
        or is_pandas_node_dataframe_input_list(value)
        or is_polars_node_dataframe_input(value)
        or is_polars_node_dataframe_input_list(value)
    )


EdgeInput = Union[
    EdgeTuple,
    List[EdgeTuple],
    PandasEdgeDataFrameInput,
    List[PandasEdgeDataFrameInput],
    PolarsEdgeDataFrameInput,
    List[PolarsEdgeDataFrameInput],
]
EdgeInputWithGroup = Tuple[EdgeInput, Group]


class MedRecordBuilder:
    """A builder class for constructing MedRecord instances.

    Allows for adding nodes, edges, and groups incrementally, and optionally
    specifying a schema.
    """

    _nodes: List[Union[NodeInput, NodeInputWithGroup]]
    _edges: List[Union[EdgeInput, EdgeInputWithGroup]]
    _groups: Dict[Group, GroupInfo]
    _schema: Optional[Schema]

    def __init__(self) -> None:
        """Initializes a new MedRecordBuilder instance."""
        self._nodes = []
        self._edges = []
        self._groups = {}
        self._schema = None

    def add_nodes(
        self,
        nodes: NodeInput,
        *,
        group: Optional[Group] = None,
    ) -> MedRecordBuilder:
        """Adds nodes to the builder.

        Args:
            nodes (NodeInput): Nodes to add.
            group (Optional[Group], optional): Group to associate with the nodes.

        Returns:
            MedRecordBuilder: The current instance of the builder.
        """
        if group is not None:
            self._nodes.append((nodes, group))
        else:
            self._nodes.append(nodes)

        return self

    def add_edges(
        self,
        edges: EdgeInput,
        *,
        group: Optional[Group] = None,
    ) -> MedRecordBuilder:
        """Adds edges to the builder.

        Args:
            edges (EdgeInput): Edges to add.
            group (Optional[Group], optional): Group to associate with the edges.

        Returns:
            MedRecordBuilder: The current instance of the builder.
        """
        if group is not None:
            self._edges.append((edges, group))
        else:
            self._edges.append(edges)

        return self

    def add_group(
        self, group: Group, *, nodes: List[NodeIndex] = []
    ) -> MedRecordBuilder:
        """Adds a group to the builder with an optional list of nodes.

        Args:
            group (Group): The name of the group to add.
            nodes (List[NodeIndex], optional): Node indices to add to the group.

        Returns:
            MedRecordBuilder: The current instance of the builder.
        """
        self._groups[group] = {"nodes": nodes, "edges": []}
        return self

    def with_schema(self, schema: Schema) -> MedRecordBuilder:
        """Specifies a schema for the MedRecord.

        Args:
            schema (Schema): The schema to apply.

        Returns:
            MedRecordBuilder: The current instance of the builder.
        """
        self._schema = schema
        return self

    def build(self) -> mm.MedRecord:
        """Constructs a MedRecord instance from the builder's configuration.

        Returns:
            MedRecord: The constructed MedRecord instance.
        """
        medrecord = mm.MedRecord()

        for node in self._nodes:
            if is_node_tuple(node):
                medrecord.add_node(*node)
                continue

            if (
                is_node_tuple_list(node)
                or is_pandas_node_dataframe_input(node)
                or is_pandas_node_dataframe_input_list(node)
                or is_polars_node_dataframe_input(node)
                or is_polars_node_dataframe_input_list(node)
            ):
                medrecord.add_nodes(node)
                continue

            group = node[1]

            if not medrecord.contains_group(group):
                medrecord.add_group(group)

            node = node[0]

            if is_node_tuple(node):
                medrecord.add_node(*node)
                medrecord.add_node_to_group(group, node[0])
                continue

            if is_node_tuple_list(node):
                medrecord.add_nodes(node)
                medrecord.add_node_to_group(group, [node[0] for node in node])
                continue

            if is_pandas_node_dataframe_input(node):
                medrecord.add_nodes(node)
                medrecord.add_node_to_group(group, node[0][node[1]].tolist())
                continue

            if is_polars_node_dataframe_input(node):
                medrecord.add_nodes(node)
                medrecord.add_node_to_group(group, node[0][node[1]].to_list())
                continue

            if is_pandas_node_dataframe_input_list(node):
                medrecord.add_nodes(node)
                medrecord.add_node_to_group(
                    group,
                    [nodes for node in node for nodes in node[0][node[1]].tolist()],
                )
                continue

            if is_polars_node_dataframe_input_list(node):
                medrecord.add_nodes(node)
                medrecord.add_node_to_group(
                    group,
                    [nodes for node in node for nodes in node[0][node[1]].to_list()],
                )

        for edge in self._edges:
            if is_edge_tuple(edge):
                medrecord.add_edge(*edge)
                continue

            if (
                is_edge_tuple_list(edge)
                or is_pandas_edge_dataframe_input(edge)
                or is_pandas_edge_dataframe_input_list(edge)
                or is_polars_edge_dataframe_input(edge)
                or is_polars_edge_dataframe_input_list(edge)
            ):
                medrecord.add_edges(edge)
                continue

            group = edge[1]

            if not medrecord.contains_group(group):
                medrecord.add_group(group)

            edge = edge[0]

            if is_edge_tuple(edge):
                edge_index = medrecord.add_edge(*edge)
                medrecord.add_edge_to_group(group, edge_index)
                continue

            if (
                is_edge_tuple_list(edge)
                or is_pandas_edge_dataframe_input(edge)
                or is_pandas_edge_dataframe_input_list(edge)
                or is_polars_edge_dataframe_input(edge)
                or is_polars_edge_dataframe_input_list(edge)
            ):
                edge_indices = medrecord.add_edges(edge)
                medrecord.add_edge_to_group(group, edge_indices)

        for group in self._groups:
            if medrecord.contains_group(group):
                medrecord.add_node_to_group(group, self._groups[group]["nodes"])
                medrecord.add_edge_to_group(group, self._groups[group]["edges"])
            else:
                medrecord.add_group(
                    group, self._groups[group]["nodes"], self._groups[group]["edges"]
                )

        if self._schema is not None:
            medrecord.schema = self._schema

        return medrecord
