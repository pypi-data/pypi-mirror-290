#module with all the function definitions for mp_df.dxp

print("debugging - this run from editable package")

import pandas as pd
import numpy as np
from typing import Union, List, Tuple

#imports for packages used in user-callable functions
from typing import Optional, Union, NamedTuple, List, Tuple
import warnings

#imports for packages used in helper functions.
from stumpy import stump as _stump
from stumpy import motifs as _motifs

# # set up logging for use below.
# import logging
# try:
#     from spotfire_dsml.logging_config import get_log_contents, clear_log_contents, close_log
# except ImportError as e:
#     print(f"ImportError: {e}")


# from spotfire_dsml.logging_config import get_log_contents, clear_log_contents, close_log

# #from logging_config import get_log_contents, clear_log_contents, close_log

# get_mp()
#  helper functions
def _report_missing_first_column(df):
    first_column = df.columns[0]
    total_rows = len(df)
    missing_count = df[first_column].isnull().sum()
    missing_percentage = (missing_count / total_rows) * 100
    
    print(f"Column: {first_column}")
    print(f"Total rows: {total_rows}")
    print(f"Missing values: {missing_count}")
    print(f"Percentage missing: {missing_percentage:.2f}%")
    if missing_percentage > .8:
        print("Warning - maybe too much missing data for Matrix Profile")



def _get_mp_with_stumpy(sequence: np.ndarray,
                       windowSize: Union[List[int], str]) -> np.ndarray:
    """ Use stumpy.mstump to get matrix profile."""
    result = _stump(sequence, windowSize)
    return result

def _get_mp_df(input_obj) -> pd.DataFrame:
    """ convert an object, usually an array representing a matrix profile, to a data frame"""
    mp_df = pd.DataFrame(input_obj)
    return mp_df

def _pad_to_nrows(input_df: pd.DataFrame, rows: int)-> pd.DataFrame:
    """Pad a dataframe to a number of rows, adjusting for situations where
    the number of rows in input_df is less than the desired number.
    """
    
    # Ensure rows is an integer and greater than the current number of rows
    rows = max(rows, len(input_df))
    
    # Reindex the DataFrame to the desired number of rows
    padded_df = input_df.reindex(range(rows))
    
    return padded_df

def _rename_mp_columns(input_df: pd.DataFrame) -> pd.DataFrame:
    """ Rename columns of a matrix profile in dataframe form. """
    if len(input_df.columns) == 4:
        input_df.columns = ['mp', 'index', 'left_mp', 'right_mp']
    else:
        # Handle cases where the number of columns doesn't match expectations
        raise Exception("The number of columns in input_df does not match the expected four.")
    return input_df
    

# def _mp1col(marked_df: pd.DataFrame, windowSize:Union[List[int], str]) -> pd.DataFrame:
#     """ Get a Matrix Profile from the input, a single column DataFrame which represents the original 
#     series in time sequence.
#     The output is transformed to a DataFrame which has the following columns:
#     ['mp', 'index', 'left_mp', 'right_mp', <original sequence name>]
#     The first 4 columns are padded at the end to match the longer length of the original sequence.

def _mp1col(marked_df: pd.DataFrame, windowSize: Union[List[int], str]) -> pd.DataFrame:
    """ Get a Matrix Profile from the input, a single column DataFrame which represents the original 
    series in time sequence.
    The output is transformed to a DataFrame which has the following columns:
    ['mp', 'index', 'left_mp', 'right_mp', <original sequence name>]
    The first 4 columns are padded at the end to match the longer length of the original sequence.
    """
    assert marked_df.shape[1] == 1, "wrong shape input to _mp1col"
    # Initialize the default output DataFrame
    default_data = {
        'mp': [None],
        'index': [None],
        'left_mp': [None],
        'right_mp': [None],
        marked_df.columns[0]: [None]
    }
    default_index = [0]
    default_output_df = pd.DataFrame(default_data, index=default_index)
    default_output_df['position_id'] = np.nan

    # some data checking:
    if marked_df.empty:
        print("No Data! Mark some data and retry")
        #logger.error(f"No Data! Mark some data and retry")
        return default_output_df
    else:
        print("DataFrame exists and has rows")
        #logger.info(f"DataFrame exists and has rows")
        nrows = marked_df.shape[0]
        if windowSize/2 >= nrows:
            print("not enough rows of data for this windowsize")
            _report_missing_first_column(marked_df)
            return default_output_df
    #get the matix profile:
    try:
        input_sequence = marked_df.values.flatten()
        mp4cols_array = _get_mp_with_stumpy(input_sequence, windowSize)
        mp_df = _get_mp_df(mp4cols_array)
        longshape_df = _rename_mp_columns(_pad_to_nrows(mp_df, marked_df.shape[0]))
        mp_df = pd.concat([marked_df, longshape_df], axis=1)
    except Exception as e:
        print(f"An error occurred: {e}")
        mp_df = default_output_df
        mp_df['position_id'] = np.nan
    return mp_df



####
def get_mp(
        marked_df: pd.DataFrame, 
        windowSize: Union[List[int], str], 
        method: str = 'stump', 
        percentage: float = None, 
        iterations: int = None, 
        previous_scrump_fn = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    """ 
    Takes the single column of marked_df and does matrix profile operation.

    Parameters
    ----------
    marked_df :  pandas.DataFrame 
    	has a single column representing the time series (sorted)
    windowSize :  integer 
    	The size of the window to use for the matrix profile calculation

    Returns
    -------
    output_df : pd.DataFrame
    	concatenate data frame containing (original data,  mp = calculated matrix profile, padded )   
    outputbkup: identical
    overlay2_df 
    

    Examples
    --------
    >>> get_mp(example_df, 5000)
    >>>        Surf Press         mp  index left_mp right_mp  
    >>> 0        0.000147  22.628004  45285      -1    45285  
    >>> 1        0.000147  22.701862  45286      -1    45286  
    >>> 2        0.000147  22.765625  45291      -1    45291  
    >>> 3        0.000165  22.804359  45293      -1    45293  
    >>> 4        0.000165  22.838848  45295      -1    45295  
    >>> ...           ...        ...    ...     ...      ...  
    >>> 52118    0.831608        NaN    NaN     NaN      NaN  
    >>> 52119    0.831608        NaN    NaN     NaN      NaN  
    >>> 52120    0.841335        NaN    NaN     NaN      NaN  
    >>> 52121    0.841335        NaN    NaN     NaN      NaN  
    >>> 52122    0.843062        NaN    NaN     NaN      NaN  
    >>> [52123 rows x 5 columns]

    """
    import pandas as pd
    import numpy as np

    mp_df = _mp1col(marked_df, windowSize)
    return mp_df, mp_df, mp_df


############################################################################################
# get_motifs
#  helper functions

def _populate_color_column_with_concat(index_df: pd.DataFrame, 
                                      output_df: pd.DataFrame,
                                      windowSize: int)-> pd.DataFrame:
    
    """ 
    Add or modify the color column in output_df according to the index_df. 
    
    Parameters
    ----------
    index_df :  pd.DataFrame 
    	Specifying the motifs to display found via the matrix profile.
    	Can be empty.
    	These motifs will added to the 'color' column of output_df.
    output_df :  pd.DataFrame 
    	Ceated by get_mp() with the original sequence and the mp columns
    windowSize :  int 
    	the window size that was used in the source matrix profile

    Returns
    -------
    output_df :  pd.DataFrame 
    	Modified with a color column to identify the motifs in context.

    Example
    --------
    # first get the inputs:
    mpxcols = original_mp_df.to_numpy()
    top_motifs_indexes =  \
         stumpy.motifs(sequence.flatten(), mpxcols[:, 0], max_motifs=5 ,  max_distance=max_distance) 
    index_df = pd.DataFrame(top_motifs_indexes)
    # then call the function:
    _populate_color_column_with_concat(index_df,
                                      output_df,
                                      windowSize)
    
    """
    if 'color' not in output_df.columns:
        output_df['color'] = ''
    output_df['color'] = output_df['color'].astype(str)
    for _, row in index_df.iterrows():
        id_str = f"{row['Motif']}_{row['Motif_Example']}"
        start_loc = int(row['Start_Location'])
        end_loc = min(start_loc + windowSize, output_df.shape[0] - 1)
        for loc in range(start_loc, end_loc + 1):
            color_out = output_df.at[loc, 'color']
            if color_out is None or color_out == "":
                output_df.at[loc, 'color'] = id_str
            else:
                output_df.at[loc, 'color'] += f",{id_str}"
        
    return output_df


class SearchResult(NamedTuple):
    output_df: Optional[pd.DataFrame]
    index_df: Optional[pd.DataFrame]
    overlay2_df: Optional[pd.DataFrame]


def _get_original_mp_df(mp_df):
    columns_subset = ['mp', 'index', 'left_mp', 'right_mp']
    original_mp_df = mp_df.dropna(how='all', subset=columns_subset)
    selected_columns_df = original_mp_df.loc[:, original_mp_df.columns.isin(columns_subset)]
    return selected_columns_df

def _search_for_motifs(mp_df, max_distance, windowSize):
    original_mp_df = _get_original_mp_df(mp_df)
    original_mp_height = original_mp_df.iloc[:, 0]
    original_sequence = mp_df.iloc[:,0]
    
    #get the top 5 warnings while you are getting the motifs
    # Capture warnings while calling stumpy.motifs
    with warnings.catch_warnings(record=True) as captured_warnings:
        warnings.simplefilter("always")  # Capture all warnings
        top_motifs_distances, top_motifs_indexes =  \
            _motifs(original_sequence, original_mp_height, max_motifs=5,  max_distance=max_distance) 

    # log any warnings
    if len(captured_warnings) == 0:
        print("get_motifs - no warnings generated by stumpy.motifs")
    for warning in captured_warnings:
        print(f"Warning captured from get_motif: {warning.message}")

    #test for no motifs found:
    if top_motifs_indexes.shape==(1,0):
        print("no motifs found")
        index_df=pd.DataFrame({'msg':'No Motifs Found'},index=[1]) #fmt for sf
    else:
        index_df = pd.DataFrame(top_motifs_indexes)


    # Prepare data for DataFrame creation: source row, source column, and values
    rows, cols = np.indices(top_motifs_indexes.shape)
    values = top_motifs_indexes.flatten()
    # Flatten the row and column indices to match the values array
    rows_flat = rows.flatten()
    cols_flat = cols.flatten()
    distances_flat = top_motifs_distances.flatten()
    index_df = pd.DataFrame({
        'Motif': rows_flat,
        'Motif_Example': cols_flat,
        'Start_Location': values,
        'Distance' : distances_flat
    })

###########################################################################


    #really only have to output new color column: for now just replace mp_df with new colors
    output_df = _populate_color_column_with_concat(index_df, mp_df, windowSize)
    
    #drop column position_id to prevent duplicates before rename
    if 'position_id' in output_df.columns:
        output_df.drop(columns=['position_id'], inplace=True)
    output_df.rename(columns={'color': 'position_id'}, inplace=True)

    # "" should be NaN for use in SF:
    output_df.loc[output_df['position_id'] == "", 'position_id'] = np.nan
    #output_df['position_id'] = np.nan

    # empty table here, fill in with call to show_motifs:
    #start with none because none marked: will be filled later by display_motifs
    overlay2_df = pd.DataFrame({'position': range(0, windowSize),'value':[0]*windowSize})
    overlay2_df['position_id']=np.nan
    return output_df, index_df, overlay2_df

def mp_height(mp_df):
    return mp_df.iloc[:,1]

def get_motifs(mp_df: pd.DataFrame, max_distance: float=50.0) -> SearchResult:
    """ 
    Search for 1-d motifs in the matrix profile using stumpy.motifs.

    stumpy_motifs issues warnings, these are printed here.

    Parameters
    ----------
    mp_df  :  pd.DataFrame 
    	The matrix profile in dataframe format.
    max_distance  :  float 
    	is the parameter used by stumpy.motifs 
    	to limit motifs to those sufficiently similar to each other

    Returns
    -------
    SearchResult :  namedTuple

    Example
    -------
    >>> get_motifs(mp_df)

    """
       
    output_df = mp_df.copy()

 
    index_data = {'Motif':np.nan, 'Motif_Example':np.nan,'Start_Location':np.nan,
                  'Distance':np.nan,'Correlation': np.nan}
    index_df =pd.DataFrame([index_data], dtype='float64')

    original_mp_df = _get_original_mp_df(mp_df)
    original_mp_height = original_mp_df.iloc[:, 0]
    original_sequence = mp_df.iloc[:,0]

    non_nan_rows_in_subset = original_mp_df.shape[0]
    windowSize = mp_df.shape[0] - non_nan_rows_in_subset + 1 

    overlay2_df = pd.DataFrame({'position': range(0, windowSize),'value':[0]*windowSize})

    named_tuple_default = SearchResult(
        output_df = output_df,
        index_df = index_df,
        overlay2_df = overlay2_df
        )

    #check input:
    if mp_df.shape == (1,2): # previous data function failed - use defaults
        print("Start over with get_mp, failed previously")
        return named_tuple_default
    else:
        clean_mp_df = mp_df.drop(['color','minimumpercolor','position_id'],errors='ignore',axis=1)
        try:
            output_df, index_df, overlay2_df = \
                _search_for_motifs(mp_df, max_distance,windowSize)
        except Exception as e:
            print("An error occurred in stumpy.motifs due to bad data or parameters")
            import traceback
            traceback.print_exc()
            named_tuple_default.overlay2_df['position_id'] = np.nan
            return named_tuple_default

        if output_df['position_id'].isna().all():
            output_df['position_id'] = 0
        return output_df, index_df, overlay2_df



    
# display_motifs
#  helper functions

def _get_sequence(df: pd.DataFrame) -> np.array:
    """get the column as an array """
    return df.values

class DisplayResult(NamedTuple):
    overlay2_df: pd.DataFrame 
    position_id: pd.DataFrame

def display_motifs(index_df: pd.DataFrame, input_data: pd.DataFrame, windowSize:int=50) -> DisplayResult:
    """ 
    Format the overlay2_df table for displaying the motifs overlaid on each other

    Parameters
    ----------
    index_df : pd.DataFrame
    	Which motifs to display (output of get_motifs, marked rows only)
    input_data :  pd.DataFrame
    	The original dataframe
    
    Returns
    -------
    position_id : pd.Series
    	column with length of sequence_original, for large display ie new column of output_df
    overlay2_df : pd.DataFrame 
    	Showing only the selected motifs 
    """
    sequence = _get_sequence(input_data)
    # get color column to return to add to output_df
    color_length = sequence.shape[0] 
    position_id = pd.Series(np.nan, index=range(color_length))

    positions = index_df['Start_Location']
    if len(positions) > 0:
        for i in range(len(positions)):
            end = min(windowSize+positions[i],len(position_id))
            #color[range(positions[i],end)] = str(i)
            position_id[range(positions[i],end)] = positions[i]
            print(i, positions[i])
        print(position_id)
    max_len = color_length - windowSize
    sequence_values_from_mp_df = [] #exclude nans at end
    for start_loc in positions:
           end = start_loc + windowSize
           sequence_values_from_mp_df.extend(sequence.flatten()[range(start_loc, end)])


# Update the DataFrame creation with the new values
    overlay2_df = pd.DataFrame({
        'position_id': positions.repeat(windowSize),
        'position in window': list(range(windowSize)) * len(positions),
        'value': sequence_values_from_mp_df
    })

    overlay2_df.reset_index(drop=True, inplace=True)

    return DisplayResult(overlay2_df, position_id)


def sax_encoding(ts, sax_string_length, sax_alphabet_size, aggregation_method="average", breakpoints="sax_default",
                 normalize_input=True, verbose=0):
    """
    Creates a SAX string representation of a time series. 
    
    Parameters
    ----------
    ts : array-like
        The time series for which to get SAX string.
    
    sax_string_length : int
        The number of bins to split the time series.
    
    sax_alphabet_size : int
        Specify the number of intervals into which to divide the z-normal distribution. Max 52.
        
    aggregation_method : str, optional (default="average")
        The aggregation method to use in SAX encoding. Options are: "average", "max", "min", or "median".
        
    breakpoints : str or array-like, optional (default="sax_default")
        Sets the method for determining breakpoints between bins.
        Options are:
        - "sax_default": use the z-normal distribution to determine breakpoints
        - "equal_width": equal width bins
        - "equal_amounts_in_each_bin": bins with equal number of data points
        - array-like: a list of breakpoints to use; length must be 1 greater than sax_alphabet_size

    normalize_input : bool, optional (default=True)
        Specify whether the input time series should be normalized.
        
    verbose : int, optional (default=0)
        If 0, do not create any standard output when calling the function. If 1, then print out information
        about SAX calculation.

    Returns
    -------
        string: a SAX string representation of the time series
        
    Examples
    --------
    >>> sample_data = pd.Series([1,2,3,4,5])
    >>> sax_encoding(sample_data, sax_string_length=2, sax_alphabet_size=2)
    >>> 'AB'
    >>> 
    >>> sample_data = pd.Series([1,2,3,4,4,3,2,1])
    >>> sax_encoding(sample_data, sax_string_length=3, sax_alphabet_size=3)
    >>> 'ACA'
    >>> 
    >>> sample_data = np.arange(50)
    >>> sax_encoding(sample_data, sax_string_length=10, sax_alphabet_size=5, breakpoints="equal_width", normalize_input=False)
    >>> 'AABBCCDDEE'
    
    Notes
    -----
    â€¢ The SAX (Symbolic Aggregate approXimation) method is used to transform a time series into a string representation.
    â€¢ Leaving breakpoints as "sax_default" assumes normality of the data, so either leave "normalize_input" as True or ensure that your data is normalized prior to calling this function. 
    â€¢ The "sax_default" option uses z-scores from a standard normal distribution to determine breakpoints, ensuring the data segments correspond to equal probabilities.
    â€¢ The number of breakpoints used is one less than the alphabet size, as the breakpoints divide the data into regions corresponding to each symbol.
    â€¢ When verbose is set to 1, the function will print details about each step, aiding in debugging and understanding the transformation process.
    """
    # Ensure SAX alphabet size is acceptable
    if sax_alphabet_size > 52:
        raise ValueError(f"sax_alphabet_size ({sax_alphabet_size}) over maximum of 52. Please lower and try again.") 
    
    # Set function for aggregation
    agg_func_dict = {"average": _np.mean, "max": _np.max, "min": _np.min, "median": _np.median}
    try:
        agg_func = agg_func_dict[aggregation_method]
    except:
        raise ValueError(f"Invalid aggregation_method. Supported methods: {list(agg_func_dict.keys())}")
        
    # Normalize the time series
    if normalize_input:
        ts = (ts - _np.mean(ts)) / _np.std(ts)
    
    # Piecewise Aggregate Approximation (PAA)
    if len(ts) % sax_string_length == 0:
        section_length = len(ts) // sax_string_length
    else:
        section_length = len(ts) / sax_string_length

    paa = [agg_func(ts[int(i * section_length):int((i + 1) * section_length)]) for i in _np.arange(sax_string_length)]
    
    # Find breakpoints that will map the PAA to symbols
    if isinstance(breakpoints, (_np.ndarray, pd.Series, list, tuple)):
        if len(breakpoints) != (sax_alphabet_size + 1):
            raise ValueError("Invalid list of breakpoints. Length of breakpoints must be one greater than sax_alphabet_size.")
        breakpoints = _np.array(breakpoints)
    elif breakpoints == "sax_default":
        if not normalize_input:
            _warnings.warn("default method for determining breakpoints assumes data has been normalized. Please ensure your data is already normalized or set normalize_input to True.")
        breakpoints = _norm.ppf(_np.linspace(0, 1, sax_alphabet_size + 1))
    elif breakpoints == "equal_width":
        breakpoints = sax_alphabet_size
    elif breakpoints == "equal_amounts_in_each_bin":
        breakpoints = _np.quantile(paa, _np.linspace(0, 1, sax_alphabet_size + 1))
        breakpoints[0] -= 0.000001 # Ensure min is included in first bin
    else:
        raise ValueError("Invalid method for determining breakpoints. Options are: 'sax_default', 'equal_width', 'equal_amounts_in_each_bin', or a list of breakpoints.")
    alphabet = [chr(65 + i) if i < 26 else chr(97 + i % 26) for i in _np.arange(sax_alphabet_size)]
    
    # Create SAX string
    sax, sax_bins = pd.cut(paa, bins=breakpoints, labels=alphabet, retbins=True)
    if sax.isna().any(): sax = sax.add_categories('_').fillna('_')
    sax_bins = pd.DataFrame({"lower": sax_bins[:-1], "upper": sax_bins[1:]}, index=alphabet)
    sax_string = "".join(sax)
    if verbose > 0:
        print("SAX string: " + sax_string + "\n")
        print("SAX bins: ")
        print(sax_bins)
        print("\nPAA: " + str(paa))
    return sax_string
