# tests
import pytest
import networkx as nx
from challenge import read_data, build_graph

from data_for_tests import TEST_DATA, TEST_GRAPH


def test_read_data():
    # sample file path is in repo

    file_path = "test_data.csv"

    data = read_data(file_path)

    assert data == TEST_DATA


def test_read_data_bad_path():
    file_path = "this_file_does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        read_data(file_path)


def test_read_data_no_path():
    with pytest.raises(TypeError):
        read_data()


def test_empty_build_graph():

    empty_graph = nx.DiGraph()

    assert nx.is_isomorphic(build_graph([]), empty_graph)


def test_build_graph():

    assert nx.is_isomorphic(build_graph(TEST_DATA), TEST_GRAPH)
