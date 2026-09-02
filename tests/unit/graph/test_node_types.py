"""
Test: Graph Node Type Definitions
"""

import pytest
from graph.schemas.node_types import NodeType, NODE_FEATURE_DIMS


class TestNodeTypes:
    """Tests for graph node type enumerations."""

    def test_all_expected_node_types_exist(self):
        expected = {"user", "device", "email", "file", "url", "pc"}
        actual = {nt.value for nt in NodeType}
        assert actual == expected

    def test_feature_dims_defined_for_all_types(self):
        for nt in NodeType:
            assert nt in NODE_FEATURE_DIMS
            assert NODE_FEATURE_DIMS[nt] > 0
