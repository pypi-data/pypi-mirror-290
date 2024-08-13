# test file for pattern_exploration:

#note full path.
from spotfire_dsml.time_series.pattern_exploration import get_motifs
from spotfire_dsml.time_series.pattern_exploration import get_mp, display_motifs

import numpy as np
import pandas as pd
import pytest
import sys
import os
from pathlib import Path


# Get the current working directory
current_dir = Path(os.getcwd())

# Assuming the current directory is tests/time_series or a subdirectory of the project
# Adjust the number of parent calls as needed based on your actual directory structure
project_root = current_dir.parent
print(project_root)

# Add the project root to sys.path
sys.path.append(str(project_root))

def test_get_mp(test_data):
    result = get_mp(test_data, 5000)
    assert result is not None

def test_get_motifs(test_mp_data):
    result = get_motifs(test_mp_data)
    assert result is not None

# def test_display_motifs_with_fixtures(index_df_fixture, input_data_fixture, windowSize, request):
#     index_df = request.getfixturevalue(index_df_fixture)
#     input_data = request.getfixturevalue(input_data_fixture)
#     result = display_motifs(index_df, input_data, windowSize)

#def test_display_motifs_with_fixtures(test_display_motifs_data, test_data, windowSize):
#using default windowSize:
def test_display_motifs_with_fixtures(test_display_motifs_data, test_data):
#    result = display_motifs(test_display_motifs_data, test_data, windowSize)
    result = display_motifs(test_display_motifs_data, test_data)
    # Add assertions to check the result if needed
    
