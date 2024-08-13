## IMPORTS

import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder
import warnings
import threading

## HELPER FUNCTIONS

def _parse_missing_data_values(data, missing_data_values):
    """
    Parse missing data values and replace them with np.nan.
    """
    if isinstance(missing_data_values, str) and "," in missing_data_values: # comma separated
        missing_data_values_list = missing_data_values.split(',')
        for i in range(len(missing_data_values_list)):
            try:
                missing_data_values_list[i] = float(missing_data_values_list[i]) # cast numbers entered as strings back to numeric
            except:
                continue
        with warnings.catch_warnings(action="ignore"):
            data = data.replace(dict.fromkeys(missing_data_values_list, np.nan)).infer_objects(copy=False)
    elif missing_data_values is not np.nan and "," not in str(missing_data_values): # single value 
        with warnings.catch_warnings(action="ignore"):
            data = data.replace(missing_data_values, np.nan).infer_objects(copy=False)
    return data

def _encode(data):
    """
    Performs ordinal encoding on categorical variables. Returns the encoded copy as well as an encoding dictionary to later reverse encodings.
    """
    enc_dict = {}
    copy = data.copy()
    for col in copy.columns.values:
        if pd.api.types.is_numeric_dtype(copy[col]):
            continue
        copy[col] = copy[col].astype(object)
        oe = OrdinalEncoder()
        encodings = {i: l for (i, l) in enumerate(oe.fit(copy[[col]]).categories_[0])}
        enc_dict[col] = encodings
        copy[col] = oe.fit_transform(copy[[col]])
    return copy, enc_dict

def _column_info(data):
    #important summaries for each column are calculated
    #parameters:
    #     data - inputtable
    #Output: important MD summaries for columns
    
    #data frame for column info/summary:
    no_rows_df=data.shape[0]
    df_temp=pd.DataFrame(data.isna().sum(),columns=['MD count'])   #number of missings in columns
    df_temp['MD percentage']= data.isna().mean()                   #percentage of missings in columns
    df_temp['not missing count']=data.shape[0]-df_temp['MD count'] #number of not missings in columns
    df_temp['unique values']= data.nunique()                       #number of unique values
    #how much of the total count of missing values is due to particular column
    influence1=data.isna().sum() #initianion (it is not optimal,can be changed to anything)
    #in next loop we are finding how much complete rows we have in data with particular variable deleted
    #so it is this number of complete rows in smaller file minus number of complete rows in the full file
    if data.shape[1]==1:
        influence1=df_temp['MD count']
    else:     
        for i in data.columns:
            influence1[i]=(data.drop(columns=i).isna().mean(axis=1)==0).sum()-(data.isna().mean(axis=1)==0).sum()
           
    df_temp['how much influencing']=influence1
    df_temp['ratio of influenced MDs']=df_temp['how much influencing']/df_temp['MD count']   #what percentage of all missings in this variable is influenced by this variable 
    df_temp['percentage rows saved']=df_temp['how much influencing']/(data.isna().mean(axis=1)>0).sum()  # what percentage of incomplete rows will be saved if this variable will be deleted
    df_temp['percentage gain of complete rows']=df_temp['how much influencing']/no_rows_df
    columns_summary=df_temp.reset_index()
    columns_summary.rename(columns={'index':'column name'}, inplace=True)
    return(columns_summary)

## USER CALLABLE FUNCTIONS

def removal(data, row_threshold="all", col_threshold="all", priority="both", missing_data_values=None):
    """
    Remove columns and rows from a dataset containing missing values based on a row threshold and column threshold of missing values.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) containing missing values.
    row_threshold : str or float, optional (default="all")
        Percentage of values in a given row that need to be missing for the row to be deleted.
        Row will be deleted if the missing value percentage is at or above the threshold.
        Allowed values:
        • "all" - remove empty rows only
        • "any" - remove any rows with missing values
        • "ignore" - do not perform row removal
        • float between 0.0 and 1.0 indicating missing value percentage threshold
    col_threshold : str or float, optional (default="all")
        Percentage of values in a given column that need to be missing for the column to be deleted.
        Column will be deleted if the missing value percentage is at or above the threshold.
        Allowed values:
        • "all" - remove empty columns only
        • "any" - remove any columns with missing values
        • "ignore" - do not perform column removal
        • float between 0.0 and 1.0 indicating missing value percentage threshold
    priority : str, optional (default="both")
        Indicates what to prioritize when removing rows/columns. Defines when the percentages are evaluated.
        Allowed values:
        • "both" - which rows and which columns to remove is evaluated in one step
        • "rows_first" - two-step approach: rows are removed first based on rows_threshold and columns for removal are based on remaining data from the first step
        • "cols_first" - two-step approach: columns are removed first, rows for removal are based on remaining data from the first step
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.

    Returns
    -------
    drop_data : pandas.DataFrame
        Dataframe with missing values removed as indicated.
    """
    #We will remove rows and columns based on percentages
    
    #special situations first
    if (col_threshold=="all"):
        col_threshold=1.0
    if (row_threshold=="all"):
        row_threshold=1.0
    if (row_threshold=="ignore"): 
        row_threshold=1.1
    if (col_threshold=="ignore"): 
        col_threshold=1.1
    
    #removing values which are representing MD
    if missing_data_values is not None:
        data = _parse_missing_data_values(data, missing_data_values)
    
    if(data.shape[0]>0 and data.shape[1]>0):
        #does not make sense if data empty
    
        #situation when rows should be removed first:
        if (priority=="rows_first"):
            #row removal
            if (row_threshold=="any"):
                drop_data=data[data.isna().mean(axis=1)==0]
            else: 
                drop_data=data[data.isna().mean(axis=1)<row_threshold] 
            #column removal (it is applied after row removal, so missing percentages are calculated after row removal
            column_summary=_column_info(drop_data)
            if  (col_threshold=="any"):
                drop_variable=list(column_summary['column name'][column_summary['MD percentage']>0])
            else:    
                drop_variable=list(column_summary['column name'][column_summary['MD percentage']>=col_threshold])
            drop_data=drop_data.drop(columns=drop_variable,axis=1)
            
         #situation when columns should be removed first:
        if (priority=="cols_first"):
            #column removal
            column_summary=_column_info(data)
            if  (col_threshold=="any"):
                drop_variable=list(column_summary['column name'][column_summary['MD percentage']>0])
            else:    
                drop_variable=list(column_summary['column name'][column_summary['MD percentage']>=col_threshold])
            data=data.drop(columns=drop_variable,axis=1)
            #row removal
            if  (row_threshold=="any"):
                drop_data=data[data.isna().mean(axis=1)==0]
            else: 
                drop_data=data[data.isna().mean(axis=1)<row_threshold]
    
         #situation when rows and columns are removed together, this means rows and columns to remove are identified in one step
        if (priority=="both"):
            #variables to remove:
            column_summary=_column_info(data)
            if  (col_threshold=="any"):
                drop_variable=list(column_summary['column name'][column_summary['MD percentage']>0])
            else: 
                drop_variable=list(column_summary['column name'][column_summary['MD percentage']>=col_threshold])
            #removing rows
            if  (row_threshold=="any"):
                drop_data=data[data.isna().mean(axis=1)==0]
            else:
                drop_data=data[data.isna().mean(axis=1)<row_threshold]
            #removing columns
            drop_data=drop_data.drop(columns=drop_variable,axis=1)
    return drop_data

def simple_imputation(data, methods, missing_data_values=None, fixed_value=None):
    """
    Perform a variety of simple imputation methods on a dataset containing missing values.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) containing missing values to be imputed.
    methods : str or pandas.DataFrame, required
        A string (for a single method) or dataframe (for multiple methods) indicating what imputation method(s) should be applied. 
        Available methods:
        • 'mean' (numeric columns only)
        • 'median' (numeric columns only)
        • 'min' (numeric columns only)
        • 'max' (numeric columns only)
        • 'most_frequent'
        • 'constant'
        Dataframe should be formatted as two columns: "Column" containing column names and "Method" containing one of the above methods.
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.
    fixed_value : optional (default=None)
        The fixed value to be imputed with if selected method(s) contains 'constant'.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe containing imputed values.
    """

    # SimpleImputer requires a dataframe, convert array-like inputs
    if isinstance(data, (pd.Series, list, np.ndarray)):
        data = pd.DataFrame(data)

    # make copy of data
    working_copy = data.copy()

    if missing_data_values is not None:
        working_copy = _parse_missing_data_values(working_copy, missing_data_values)

    numeric_methods = ['min', 'max', 'mean', 'median']

    if isinstance(methods, str):
        # check data types
        if methods in numeric_methods and 'O' in working_copy.dtypes.values:
            raise ValueError("At least one column is non-numeric and a numeric imputation method was chosen. Please cast to numeric type, remove column, or change method choice.")
        # min and max
        if methods == 'min':
            min_values = {}
            for col in working_copy.columns.values:
                min_values[col] = working_copy[col].min()
            return working_copy.fillna(value=min_values)
        elif methods == 'max':
            max_values = {}
            for col in working_copy.columns.values:
                max_values[col] = working_copy[col].max()
            return working_copy.fillna(value=max_values)
        
        # fixed value
        elif methods == 'constant':
            if fixed_value is None:
                raise ValueError("Chosen method is 'constant' but no input value for 'fixed_value' was given.")
            return working_copy.fillna(fixed_value)

        # mean, median, most_frequent
        else:
            imputer = SimpleImputer(strategy=methods)
        result = imputer.fit_transform(working_copy)
        output = pd.DataFrame(result)
        rename_cols = dict(zip(output.columns.values, working_copy.columns.values))
        return output.rename(columns=rename_cols)
    
    elif isinstance(methods, pd.DataFrame): # for multiple methods
        for col in working_copy.columns.values:
            method = methods[methods['Column']==col]['Method'].values[0]
            # check data types
            if method in numeric_methods and working_copy[col].dtype == 'O':
                raise ValueError(f"Column {col} is non-numeric where a numeric imputation method was chosen. Please cast to numeric type, remove column, or change method choice.")
            if method == 'min':
                working_copy[col] = working_copy[col].fillna(working_copy[col].min())
            elif method == 'max':
                working_copy[col] = working_copy[col].fillna(working_copy[col].max())
            elif method == 'constant':
                if fixed_value is None:
                    raise ValueError("Chosen method is 'constant' but no input value for 'fixed_value' was given.")
                working_copy[col] = working_copy[col].fillna(fixed_value)
            elif method == 'mean':
                working_copy[col] = working_copy[col].fillna(working_copy[col].mean())
            elif method == 'median':
                working_copy[col] = working_copy[col].fillna(working_copy[col].median())
            elif method == 'most_frequent':
                working_copy[col] = working_copy[col].fillna(working_copy[col].mode()[0])
        return working_copy

    else:
        raise ValueError("Invalid input for methods. Must be a string or a table.")
    
def rand_samp_imputation(data, missing_data_values=None):
    """
    Perform random sample imputation on a dataset containing missing values.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) containing missing values to be imputed.
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe containing imputed values.
    """
    working_copy = data.copy()

    if missing_data_values is not None:
        working_copy = _parse_missing_data_values(working_copy, missing_data_values)

    for col in working_copy.columns.values:
        has_na_idx = np.where(working_copy[col].isna())[0]
        no_na_idx = np.where(working_copy[col].notna())[0]
        no_na = working_copy[col].iloc[no_na_idx]

        rand_samp = no_na.sample(len(has_na_idx), replace=True) # sampling with replacement, especially necessary if number missing is more than number not missing
        rand_samp.index = has_na_idx
        working_copy.loc[working_copy[col].isna(), col] = rand_samp

    return working_copy

def knn_imputation(data, n_neighbors=5, missing_data_values=None):
    """
    Perform KNN imputation on a dataset containing missing values.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) containing missing values to be imputed.
    n_neighbors : int, optional (default=5)
        Number of nearest neighbors to include in KNN imputation.
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe containing imputed values.

    Notes
    -----
    • KNN imputation is only valid on numeric variables.
    • KNN imputation can be computationally expensive, which can cause a long runtime for large datasets.
    """
    # KNNImputer requires a dataframe, convert array-like inputs
    if isinstance(data, (pd.Series, list, np.ndarray)):
        data = pd.DataFrame(data)

    # necessary workaround for Spotfire optional inputs
    if n_neighbors is None:
        n_neighbors = 5

    # make copy of data
    working_copy = data.copy()

    if missing_data_values is not None:
        working_copy = _parse_missing_data_values(working_copy, missing_data_values)

    # only keep numeric columns    
    working_copy = working_copy.select_dtypes(include='number')

    imputer = KNNImputer(n_neighbors=n_neighbors)
    result = imputer.fit_transform(working_copy)
    output = pd.DataFrame(result)
    rename_cols = dict(zip(output.columns.values, working_copy.columns.values))
    output = output.rename(columns=rename_cols)

    return output

def mice_imputation(data, missing_data_values=None, n_nearest_features=None, encode=False):
    """
    Perform MICE imputation on a dataset containing missing values.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) containing missing values to be imputed.
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.
    n_nearest_features : int, optional (default=None)
        Number of other features to use to estimate missing values.
        When set to None, all other features will be used.
        Parameter is useful to speed up processing time when total number of features is large.
    encode : bool, optional (default=False)
        Set as True to indicate if non-numeric variables should be encoded prior to imputing, then reverse encoded in the output.
        Set as False to indicate if non-numeric variables should be dropped prior to imputing.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe containing imputed values.

    Notes
    -----
    • The default model used is RandomForestRegressor(). If fitting and transforming via RandomForestRegressor takes longer than 10 seconds, BayesianRidge() is used instead.
    • If fitting and transforming via BayesianRidge takes longer than 10 seconds, LinearRegression() is used instead.
    """
    # IterativeImputer requires a dataframe, convert array-like inputs
    if isinstance(data, (pd.Series, list, np.ndarray)):
        data = pd.DataFrame(data)

    # make copy of data
    working_copy = data.copy()

    if missing_data_values is not None:
        working_copy = _parse_missing_data_values(working_copy, missing_data_values)

    # if encode true, do encoding
    encoded = False
    if encode is True and 'O' in working_copy.dtypes.values:
        working_copy, oe_dict = _encode(working_copy)
        encoded = True

    # only keep numeric columns    
    working_copy = working_copy.select_dtypes(include='number')

    def _timeout():
        pass
    t1 = threading.Timer(10, _timeout)
    t1.start()
    t1.join()
    if t1.is_alive():
        imputer = IterativeImputer(estimator=RandomForestRegressor(), n_nearest_features=n_nearest_features)
        result = imputer.fit_transform(working_copy)
    else:
        warnings.warn("RandomForestRegressor taking longer than 10 seconds, BayesianRidge to be used instead.")
        t2 = threading.Timer(10, _timeout)
        t2.start()
        t2.join()
        if t2.is_alive():
            imputer = IterativeImputer(estimator=BayesianRidge(), n_nearest_features=n_nearest_features)
            result = imputer.fit_transform(working_copy)
        else:
            warnings.warn("BayesianRidge taking longer than 10 seconds, LinearRegression to be used instead.")
            imputer = IterativeImputer(estimator=LinearRegression(), n_nearest_features=n_nearest_features)
            result = imputer.fit_transform(working_copy)

    output = pd.DataFrame(result)
    rename_cols = dict(zip(output.columns.values, working_copy.columns.values))
    output = output.rename(columns=rename_cols)

    if encoded is True:
        for col in oe_dict.keys():
            output[col] = output[col].apply(lambda x: round(x))
            output[col] = output[col].map(oe_dict[col])

    return output

def multi_impute(data, methods, missing_data_values=None, fixed_value=None, n_neighbors=5, n_nearest_features=None, encode=False):
    """
    Perform a variety of imputation methods on a dataset containing missing values.

    Parameters
    ----------
    data : pandas.DataFrame or array-like (pd.Series, np.ndarray, list), required
        The column(s) containing missing values to be imputed.
    methods : pandas.DataFrame, required
        Dataframe (for multiple methods) indicating what imputation method(s) should be applied. 
        Available methods:
        • 'mean' (numeric columns only)
        • 'median' (numeric columns only)
        • 'min' (numeric columns only)
        • 'max' (numeric columns only)
        • 'most_frequent'
        • 'constant'
        • 'random_samp'
        • 'knn'
        • 'mice'
        Dataframe should be formatted as two columns: "Column" containing column names and "Method" containing one of the above methods.
    missing_data_values : optional (default=None)
        Additional values to recognize as missing values. 
        For multiple values, input should be formatted as a comma separated string with all missing data values.
    fixed_value : optional (default=None)
        The fixed value to be imputed with if selected method(s) contains 'constant'.
    n_neighbors : int, optional (default=5)
        Number of nearest neighbors to include in KNN imputation.
    n_nearest_features : int, optional (default=None)
        Number of other features to use to estimate missing values.
        When set to None, all other features will be used.
        Parameter is useful to speed up processing time when total number of features is large.
    encode : bool, optional (default=False)
        Set as True to indicate if non-numeric variables should be encoded prior to imputing, then reverse encoded in the output.
        Set as False to indicate if non-numeric variables should be dropped prior to imputing.

    Returns
    -------
    output_df : pandas.DataFrame
        Dataframe containing imputed values. Original order of columns is retained.
    """
    # Methods requires a dataframe, convert array-like inputs
    if isinstance(data, (pd.Series, list, np.ndarray)):
        data = pd.DataFrame(data)

    # make copy of data
    working_copy = data.copy()

    if missing_data_values is not None:
        working_copy = _parse_missing_data_values(working_copy, missing_data_values)

    simple_methods = ['mean', 'median', 'min', 'max', 'most_frequent']
    impute_with_simple = methods[methods['Method'].isin(simple_methods)]['Column'].values
    impute_with_constant = methods[methods['Method'] == 'constant']['Column'].values
    impute_with_rand_samp = methods[methods['Method'] == 'rand_samp']['Column'].values
    impute_with_knn = methods[methods['Method'] == 'knn']['Column'].values
    impute_with_mice = methods[methods['Method'] == 'mice']['Column'].values

    for col in impute_with_simple:
        method = methods[methods['Column']==col]['Method'].values[0]
        # check data types
        if method in simple_methods[:-1] and working_copy[col].dtype == 'O':
            raise ValueError(f"Column {col} is non-numeric where a numeric imputation method was chosen. Please cast to numeric type, remove column, or change method choice.")
        
        if method == 'min':
            working_copy[col] = working_copy[col].fillna(working_copy[col].min())
        elif method == 'max':
            working_copy[col] = working_copy[col].fillna(working_copy[col].max())
        elif method == 'mean':
            working_copy[col] = working_copy[col].fillna(working_copy[col].mean())
        elif method == 'median':
            working_copy[col] = working_copy[col].fillna(working_copy[col].median())
        elif method == 'most_frequent':
            working_copy[col] = working_copy[col].fillna(working_copy[col].mode()[0])

    if len(impute_with_constant) > 0:
        if fixed_value is None:
            raise ValueError("Chosen method is 'constant' but no input value for 'fixed_value' was given.")
        working_copy[impute_with_constant] = working_copy[impute_with_constant].fillna(fixed_value)
    if len(impute_with_rand_samp) > 0:
        rand_samp_result = rand_samp_imputation(working_copy, missing_data_values=missing_data_values)
        working_copy[impute_with_rand_samp] = rand_samp_result[impute_with_rand_samp]
    if len(impute_with_knn) > 0:
        knn_result = knn_imputation(working_copy, n_neighbors=n_neighbors, missing_data_values=missing_data_values)
        working_copy[impute_with_knn] = knn_result[impute_with_knn]
    if len(impute_with_mice) > 0:
        mice_result = mice_imputation(working_copy, missing_data_values=missing_data_values, n_nearest_features=n_nearest_features, encode=encode)
        working_copy[impute_with_mice] = mice_result[impute_with_mice]
    
    return working_copy

