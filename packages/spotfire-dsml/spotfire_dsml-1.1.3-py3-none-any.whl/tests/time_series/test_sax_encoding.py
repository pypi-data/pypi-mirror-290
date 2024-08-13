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
project_root = current_dir.parent.parent

# Add the project root to sys.path
sys.path.append(str(project_root))

from spotfire_dsml.time_series.pattern_exploration import sax_encoding

@pytest.fixture
def sample_data():
    # Define the start date, number of periods, and frequency
    start_date = "2022-01-01"
    num_periods = 365
    date_range = pd.date_range(start=start_date, periods=num_periods, freq='D')

    # Simulate a linear trend
    linear_trend = np.linspace(start=0, stop=num_periods/10, num=num_periods)

    # Simulate a seasonal component (e.g., sine wave for yearly seasonality)
    seasonality = 10 * np.sin(np.linspace(start=0, stop=2*np.pi, num=num_periods))

    # Add random noise
    np.random.seed(42)  # Seed for reproducibility
    noise = np.random.normal(loc=0, scale=2, size=num_periods)

    # Combine the components to create the time series
    data = linear_trend + seasonality + noise

    # Create a DataFrame
    measurement_col = pd.Series(data, name="Measurement")
    return measurement_col

def sax_test_1(sample_data):
    # Set the parameters for testing
    sax_string_length = 3
    sax_alphabet_size = 2
    aggregation_method = "average"
    breakpoints = "sax_default"
    normalize_input = True
    verbose = 0
    result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input, verbose)
    assert len(result) == sax_string_length
    assert np.all(pd.Series(list(result)).isin([chr(65 + c) for c in np.arange(sax_alphabet_size)] + ["_"]))
        
def sax_test_2(sample_data):
    sax_string_length = 8
    sax_alphabet_size = 25
    aggregation_method = "median"
    breakpoints = "equal_width"
    normalize_input = True
    verbose = 0
    result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input, verbose)
    assert len(result) == sax_string_length
    assert np.all(pd.Series(list(result)).isin([chr(65 + c) for c in np.arange(sax_alphabet_size)] + ["_"]))
    
def sax_test_3(sample_data):
    sax_string_length = 4
    sax_alphabet_size = 1
    aggregation_method = "min"
    breakpoints = "equal_amounts_in_each_bin"
    normalize_input = False
    verbose = 0
    result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input, verbose)
    assert len(result) == sax_string_length
    assert np.all(pd.Series(list(result)).isin([chr(65 + c) for c in np.arange(sax_alphabet_size)] + ["_"]))
    
def sax_test_4(sample_data):
    # Ensure array works for breakpoints, plus make sure nulls don't cause an error
    sax_string_length = 4
    sax_alphabet_size = 4
    aggregation_method = "min"
    breakpoints = np.array([-2, -1, 0, 1, 2])
    normalize_input = True
    verbose = 1
    result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input, verbose)
    assert len(result) == sax_string_length
    assert np.all(pd.Series(list(result)).isin([chr(65 + c) for c in np.arange(sax_alphabet_size)] + ["_"]))
    
def sax_test_5(sample_data):
    # invalid aggregation
    sax_string_length = 4
    sax_alphabet_size = 1
    aggregation_method = "mean"
    breakpoints = "equal_amounts_in_each_bin"
    normalize_input = False
    verbose = 0
    with pytest.raises(ValueError) as exception_info:
        result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input, verbose)
    assert "Invalid aggregation_method. Supported methods:" in str(exception_info.value)
    
def sax_test_6(sample_data):
    # breakpoints invalid (need to convert str to array for list option)
    sax_string_length = 4
    sax_alphabet_size = 1
    aggregation_method = "min"
    breakpoints = "[1, 2, 3]"
    normalize_input = False
    verbose = 0
    with pytest.raises(ValueError) as exception_info:
        result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input, verbose)
    assert "Invalid method for determining breakpoints" in str(exception_info.value)
    
def sax_test_7(sample_data):
    # sax alphabet too big, make sure breakpoint array doesn't cause error
    sax_string_length = 4
    sax_alphabet_size = 58
    aggregation_method = "min"
    breakpoints = [1, 2, 3]
    normalize_input = False
    verbose = 0
    with pytest.raises(ValueError) as exception_info:
        result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input, verbose)
    assert "sax_alphabet_size ({}) over maximum of 52".format(sax_alphabet_size) in str(exception_info.value)
    
def sax_test_8(sample_data):
    # Make sure all kinds of lists work for breakpoints
    sax_string_length = 6
    sax_alphabet_size = 4
    aggregation_method = "average"
    normalize_input = True
    for breakpoints in [[-np.inf, -1, 0, 1, np.inf], pd.Series([-np.inf, -1, 0, 1, np.inf]), (-np.inf, -1, 0, 1, np.inf)]:
        result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, aggregation_method, breakpoints, normalize_input)
        assert len(result) == sax_string_length
        assert np.all(pd.Series(list(result)).isin([chr(65 + c) for c in np.arange(sax_alphabet_size)] + ["_"]))
        
def sax_test_9(sample_data):
    # Get correct error message when length of breakpoints is misaligned with SAX alphabet size
    sax_string_length = 6
    sax_alphabet_size = 4
    breakpoints = [-1, 0, 2]
    with pytest.raises(ValueError) as exception_info:
        result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, breakpoints=breakpoints)
    assert "Invalid list of breakpoints" in str(exception_info.value)
    
def sax_test_10(sample_data):
    # Make sure warning comes up for no normalization with "sax_default" breakpoints
    sax_string_length = 6
    sax_alphabet_size = 4
    normalize_input = False
    breakpoints = "sax_default"
    with pytest.warns(UserWarning, match="default method for determining breakpoints assumes data has been normalized"):
        result = sax_encoding(sample_data, sax_string_length, sax_alphabet_size, breakpoints=breakpoints, normalize_input=normalize_input)
        
def sax_test_11():
    # If std is 0, SAX string should be all _ 
    sax_string_length = 5
    sax_alphabet_size = 3
    normalize_input = True
    breakpoints = "sax_default"
    result = sax_encoding(np.ones(20), sax_string_length, sax_alphabet_size)
    assert "_" * sax_string_length == result