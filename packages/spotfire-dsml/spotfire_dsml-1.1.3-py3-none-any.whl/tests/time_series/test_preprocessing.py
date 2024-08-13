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

import spotfire_dsml.time_series.preprocessing as tsp

@pytest.fixture
def ts_data():
    n_cols = 5
    np.random.seed(10)
    data_dict = {"date": pd.date_range("1/1/2022", "1/5/2022")}
    for i in np.arange(1, n_cols+1):
        data_dict["feature_{}".format(i)] = np.random.normal(size=5)
    data = pd.DataFrame(data_dict)
    data.iloc[1, 1] = np.nan
    data.iloc[2, 2] = np.nan
    return data

def test_exception_on_numeric_imputation_method(ts_data):
    method = "prevoius"
    with pytest.raises(Exception) as exception_info:
        tsp.missing_value_imputation(ts_data, "Date", numeric_method=method)
    assert exception_info.match(
            "numeric_method not recognized, please try again."
        )

def test_missing_value_imputation(ts_data):
    method = "linear"
    result = tsp.missing_value_imputation(ts_data, "date", numeric_method=method)

    # Test case1: This checks if the given data is of the pandas Dataframe type
    assert isinstance(result, pd.DataFrame), "result should be of type pandas Dataframe"

    # Test case2: This checks if null value is imputed correctly
    assert result.iloc[1, 1] == np.mean([ts_data.iloc[0, 1], ts_data.iloc[2, 1]])
    assert result.iloc[2, 2] == np.mean([ts_data.iloc[1, 2], ts_data.iloc[3, 2]])

def test_exception_on_resampling_rule(ts_data):
    rule = "8hh"
    method = "prevoius"
    with pytest.raises(ValueError) as exception_info:
        tsp.resampling(ts_data, "date", rule=rule, fill_method=method)
    assert exception_info.match(
            "Invalid frequency: 8hh"
        )

def test_exception_on_resampling_fill_method(ts_data):
    n_samples = 12
    method = "prevoius"
    rule = "4H"
    with pytest.raises(Exception) as exception_info:
        tsp.resampling(ts_data, "date", rule=rule, fill_method=method)
    assert exception_info.match(
            "fill_method not recognized, please try again."
        )

def test_resampling(ts_data):
    method = "linear"
    result = tsp.missing_value_imputation(ts_data, "Date", numeric_method=method)

    # Test case1: This checks if the given data is of the pandas Dataframe type
    assert isinstance(result, pd.DataFrame), "result should be of type pandas Dataframe"

    # Test case2: This checks if null value is imputed correctly
    assert result.iloc[1, 1] == np.mean([ts_data.iloc[0, 1], ts_data.iloc[2, 1]])
    assert result.iloc[2, 2] == np.mean([ts_data.iloc[1, 2], ts_data.iloc[3, 2]])

def test_resampling_prev(ts_data):
    method = "previous"
    result = tsp.resampling(ts_data, "date", rule="4H", fill_method=method)
    result["day"] = result["date"].dt.date
    final_result = result.drop_duplicates(subset=result.columns.difference(["date"]))
    assert len(ts_data) == len(final_result)

def test_exception_on_min_max(ts_data):
    with pytest.raises(Exception) as exception_info:
        tsp.min_max_normalization(ts_data, 1, 0)
    assert exception_info.match(
        "new_max must be greater than new_min. Please adjust and try again."
    )
    
def test_constant_cols_on_min_max(ts_data):
    d = ts_data.copy()
    d["constant"] = 0
    result = tsp.min_max_normalization(d, 0, 1)
    assert sum(result["constant"]) == 0

def test_exception_on_min_max(ts_data):
    d = ts_data.copy()
    d.loc[0, "date"] = np.nan
    result = tsp.index_normalization(d, "date", "1-1-2001", "1-1-2002", "%d-%m-%Y")
    assert len(d) == len(result)
    assert len(d[d["date"].isna()]) == len(result[result["date"].isna()])

@pytest.fixture
def generate_test_data():
    # Create a date range from Jan 1, 2022 to Jan 10, 2022
    date_range = pd.date_range(start='1/1/2022', end='1/10/2022')

    # Generate random data for 3 features
    feature_1 = np.random.normal(0, 1, len(date_range))
    feature_2 = np.random.normal(0, 2, len(date_range))
    feature_3 = np.random.normal(0, 3, len(date_range))

    # Create a DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'feature_1': feature_1,
        'feature_2': feature_2,
        'feature_3': feature_3
    })

    return df

def test_lag(generate_test_data):
    result = tsp.lag(generate_test_data, "date", 2)
    assert isinstance(result, pd.DataFrame), "result should be of type pandas DataFrame"
    assert result["feature_1_lag_2"].isna().sum() == 2, "First two values should be NaN"
    assert result["feature_1_lag_2"].iloc[2] == generate_test_data["feature_1"].iloc[0], "Lag operation did not work correctly"

def test_lead(generate_test_data):
    result = tsp.lead(generate_test_data, "date", 2)
    assert isinstance(result, pd.DataFrame), "result should be of type pandas DataFrame"
    assert result["feature_1_lead_2"].isna().sum() == 2, "Last two values should be NaN"
    assert result["feature_1_lead_2"].iloc[0] == generate_test_data["feature_1"].iloc[2], "Lead operation did not work correctly"

def test_rolling(generate_test_data):
    result = tsp.rolling(generate_test_data, "date", 2, 'mean')
    assert isinstance(result, pd.DataFrame), "result should be of type pandas DataFrame"
    assert result["feature_1_rolling_2"].isna().sum() == 1, "First value should be NaN"
    assert np.isclose(result["feature_1_rolling_2"].iloc[1], generate_test_data["feature_1"].iloc[:2].mean()), "Rolling operation did not work correctly"

def test_lag_with_fill_value(generate_test_data):
    result = tsp.lag(generate_test_data, "date", 2, fill_value=0)
    assert result["feature_1_lag_2"].isna().sum() == 0, "There should be no NaN values"
    assert result["feature_1_lag_2"].iloc[0] == 0, "First value should be 0"

def test_lead_with_fill_value(generate_test_data):
    result = tsp.lead(generate_test_data, "date", 2, fill_value=0)
    assert result["feature_1_lead_2"].isna().sum() == 0, "There should be no NaN values"
    assert result["feature_1_lead_2"].iloc[-1] == 0, "Last value should be 0"

def test_rolling_with_fill_value(generate_test_data):
    result = tsp.rolling(generate_test_data, "date", 2, 'mean', fill_value=0)
    assert result["feature_1_rolling_2"].isna().sum() == 0, "There should be no NaN values"
    assert result["feature_1_rolling_2"].iloc[0] == 0, "First value should be 0"

def test_lag_with_dropna(generate_test_data):
    result = tsp.lag(generate_test_data, "date", 2, dropna=True)
    assert result["feature_1_lag_2"].isna().sum() == 0, "There should be no NaN values"
    assert len(result) == len(generate_test_data) - 2, "Resulting DataFrame should have 2 less rows"

def test_lead_with_dropna(generate_test_data):
    result = tsp.lead(generate_test_data, "date", 2, dropna=True)
    assert result["feature_1_lead_2"].isna().sum() == 0, "There should be no NaN values"
    assert len(result) == len(generate_test_data) - 2, "Resulting DataFrame should have 2 less rows"

def test_rolling_with_dropna(generate_test_data):
    result = tsp.rolling(generate_test_data, "date", 2, 'mean', dropna=True)
    assert result["feature_1_rolling_2"].isna().sum() == 0, "There should be no NaN values"
    assert len(result) == len(generate_test_data) - 1, "Resulting DataFrame should have 1 less row"

def test_lag_with_multiple_periods(generate_test_data):
    result = tsp.lag(generate_test_data, "date", [1, 2])
    assert "feature_1_lag_1" in result.columns, "Column 'feature_1_lag_1' should exist"
    assert "feature_1_lag_2" in result.columns, "Column 'feature_1_lag_2' should exist"

def test_lead_with_multiple_periods(generate_test_data):
    result = tsp.lead(generate_test_data, "date", [1, 2])
    assert "feature_1_lead_1" in result.columns, "Column 'feature_1_lead_1' should exist"
    assert "feature_1_lead_2" in result.columns, "Column 'feature_1_lead_2' should exist"

def test_rolling_with_center(generate_test_data):
    result = tsp.rolling(generate_test_data, "date", 2, 'mean', center=True)
    assert isinstance(result, pd.DataFrame), "result should be of type pandas DataFrame"
    assert result["feature_1_rolling_2"].isna().sum() == 1, "Only the first value should be NaN"
    assert np.isclose(result["feature_1_rolling_2"].iloc[1], generate_test_data["feature_1"].iloc[:2].mean()), "Rolling operation did not work correctly"

def test_rolling_with_min_periods(generate_test_data):
    result = tsp.rolling(generate_test_data, "date", 2, 'mean', min_periods=1)
    assert isinstance(result, pd.DataFrame), "result should be of type pandas DataFrame"
    assert result["feature_1_rolling_2"].isna().sum() == 0, "There should be no NaN values"
    assert np.isclose(result["feature_1_rolling_2"].iloc[0], generate_test_data["feature_1"].iloc[0]), "First value should be equal to the first value of the original series"

def test_rolling_with_closed(generate_test_data):
    result = tsp.rolling(generate_test_data, "date", 2, 'mean', closed='right')
    assert isinstance(result, pd.DataFrame), "result should be of type pandas DataFrame"
    assert result["feature_1_rolling_2"].isna().sum() == 1, "First value should be NaN"
    assert np.isclose(result["feature_1_rolling_2"].iloc[1], generate_test_data["feature_1"].iloc[:2].mean()), "Rolling operation did not work correctly"

def test_rolling_with_win_type(generate_test_data):
    result = tsp.rolling(generate_test_data, "date", 2, 'mean', win_type='boxcar')
    assert isinstance(result, pd.DataFrame), "result should be of type pandas DataFrame"
    assert result["feature_1_rolling_2"].isna().sum() == 1, "First value should be NaN"
    assert np.isclose(result["feature_1_rolling_2"].iloc[1], generate_test_data["feature_1"].iloc[:2].mean()), "Rolling operation did not work correctly"

def test_lag_dropna_none():
    # Create a sample DataFrame
    sample_data = {
        "Date": pd.date_range("2022-01-01", periods=5),
        "Value": [10, 20, np.nan, 40, 50]
    }
    df = pd.DataFrame(sample_data)

    # Call lag with dropna=None (mistakenly)
    result = tsp.lag(df, "Date", 2, dropna=None)

    # Assert that dropna is treated as False
    assert result.shape[0] == 5, "Number of rows should remain unchanged"
    assert result["Value_lag_2"].isnull().sum().sum() == 3, "Missing values should not be dropped in lagged columns"