import os
import pytest
import pandas as pd

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_csv_file_path(filename):
    project_root = get_project_root()
    return os.path.join(project_root, 'tests', 'time_series', 'pattern_exploration_data', filename)

@pytest.fixture(scope="module")
def test_data():
    csv_file_path = get_csv_file_path('test_data.csv')
    return pd.read_csv(csv_file_path)

@pytest.fixture(scope="module")
def test_mp_data():
    csv_file_path = get_csv_file_path('test_mp_data.csv')
    return pd.read_csv(csv_file_path)

@pytest.fixture(scope="module")
def test_display_motifs_data():
    csv_file_path = get_csv_file_path('test_index_data.csv')
    return pd.read_csv(csv_file_path)
