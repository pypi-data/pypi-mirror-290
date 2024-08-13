
# --- LIBRARIES ---------------------------------------------------------------
import pandas as pd
import shapely
import pyogrio
from shapely.validation import make_valid
import geopandas as gpd

# spotfire_dsml libraries
from spotfire_dsml.geo_analytics import crs_utilities, shape_utilities

###############################################################################
# IO Utilities:
# Utilities for IO to/from Spotfire and to external file system

# Use geopandas, shapely for transformations and other calculations
###############################################################################

# --- GLOBAL SETTINGS ---------------------------------------------------------
# see https://geopandas.org/en/stable/docs/user_guide/io.html
# fiona soon to be replaced by pyogrio in geopandas
gpd.options.io_engine = "pyogrio"

# --- INTERNAL FUNCTIONS ------------------------------------------------------

def _convert_unit(from_unit,to_unit):
    '''
    Internal function to convert metric or imperial units.
    Recognized units are:
        'm','metre','meter','meters'
        'km','kilometer','kilometers','kilometre','kilometres'
        'mi', 'mile','miles'
        'feet','ft','feets'.

    Parameters
    ----------
    from_unit : str
        The original unit.
    to_unit : str
        The target unit.

    Raises
    ------
    RuntimeError
        If the unit is not recognized.

    Returns
    -------
    factor : float
        Multiplicative factor to convert a number expressed in from_unit to
        a number expressed in to_unit.

    '''
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()
    metre_units = ['m','mt','metre','meter','meters']
    km_units = ['km','kilometer','kilometers','kilometre','kilometres']
    mile_units = ['mi','mile','miles']
    feet_units = ['ft','feet','feets']
    allowed_units = metre_units + km_units + mile_units+ feet_units

    if from_unit not in allowed_units or to_unit not in allowed_units:
        raise RuntimeError('_convert_unit: Unit can only be meters, feet, km or miles',from_unit,to_unit)
    
    factor = -1 #default initial
    
    unit_dict = dict.fromkeys(metre_units, 'm')
    unit_dict.update(dict.fromkeys(km_units, 'km'))
    unit_dict.update(dict.fromkeys(mile_units, 'mi'))
    unit_dict.update(dict.fromkeys(feet_units, 'ft'))
    
    if unit_dict[from_unit] == unit_dict[to_unit]:
        factor = 1.0
    else:
        if from_unit in metre_units:
            if to_unit in km_units:
                factor = 0.001
            elif to_unit in mile_units:
                factor = 1.0/1609.34
            elif to_unit in feet_units:
                factor = 3.28084
                
        if from_unit in km_units:
            if to_unit in metre_units:
                factor = 1000.0
            elif to_unit in mile_units:
                factor = 1.0/1.60934
            elif to_unit in feet_units:
                factor = 3280.84
                
        if from_unit in mile_units:
            if to_unit in km_units:
                factor = 1.60934
            elif to_unit in metre_units:
                factor = 1609.34
            elif to_unit in feet_units:
                factor = 5280.0
                
        if from_unit in feet_units:
            if to_unit in km_units:
                factor = 0.0003048
            elif to_unit in metre_units:
                factor = 0.3048
            elif to_unit in mile_units:
                factor = 1.0/5280.0

    if factor == -1:
        raise RuntimeError('_convert_unit: unknown error occurred',from_unit,'to',to_unit)
        
    return factor


def _handle_missing_data_geometry(geo,extra=None):
    '''
    Handle missing data in a geometry, removing the corresponding rows
    from the optional extra_columns data frame.

    Parameters
    ----------
    geo : geopandas GeoSeries
        The input geometry column.
    extra : pandas DataFrame, optional
        Any extra columns to be aligned with the geometry. 
        The default is None.

    Returns
    -------
    geo : geopandas GeoSeries
        The geometry with removed missing data.
    extra : pandas DataFrame
        The extra columns with rows removed where the geometry was missing.

    '''

    if isinstance(extra,pd.core.frame.DataFrame):
        missing_index =geo.loc[geo.isna()].index.tolist()
        extra.drop(index=missing_index,inplace=True)
    geo.dropna(inplace=True)
    return (geo, extra)


def _handle_missing_data_coords(coords_df, coord_names):
    '''
    Internal function to handle missing data from a data frame.
    In the current implementation, missing data are removed in the whole
    data frame, but only for the specified columns (which are expected to 
    correspond to the spatial coordinates)

    Parameters
    ----------
    coords_df : pandas DataFrame
        The input data frame.
    coord_names: list[str]
        The names of the columns containing coordinates.
        Null values of any other column will be ignored.

    Returns
    -------
    pandas DataFrame
        The data frame with missing rows removed.

    '''
    return coords_df.dropna(subset=coord_names,inplace=False, how='any')
    

def _check_id(id_vector, length, prefix='ID'):
    '''
    Internal function to check whether an id column was provided and
    whether it has unique values. If no id column was provided, generate
    a new one with the desired prefix.

    Parameters
    ----------
    id_vector : array-like
        The input id column.
    length : int
        The desired length of the id column.
    prefix : str, optional
        The desired prefix of the id column, if it needs generating. 
        The default is 'ID'. A "_" separator will be added to the prefix.

    Raises
    ------
    RuntimeError
        If the provided id column does not have all unique values.

    Returns
    -------
    list
        The generated id vector (if the input id was None) or the input id cast
        into a Python list.

    '''
    if not isinstance(id_vector,pd.Series) and not isinstance(id_vector,list):
        prefix = prefix+'_'
        id_gen_vector = [prefix + str(x) for x in range(length)]
        return id_gen_vector
    else:
        if len(id_vector) != length:
            raise RuntimeError('The id provided does not have the desired length')            
        if len(id_vector) > len(set(id_vector)):
            raise RuntimeError('The id provided does not contain all unique values')
        try:
            return id_vector.tolist()
        except:
            return id_vector


def _input_coordinates(col_names,a,b=None):
    '''
    Internal function to set up a dataframe containing the input coordinates.
    The coordinates can come as two separate columns of data (a and b) or as a single tuple (a).
    The column names for the output data frame must be provided (normally, either lat,lon or x,y).
    Missing data are only removed if present in a and b (if provided).

    Parameters
    ----------
    col_names : list[str]
        The column names for the output dataframe.
    a : tuple or array-like
        The coordinates (if a tuple) or the first coordinate (if an array).
    b : array-like, optional
        The second coordinate (if a is a vector) or empty if a is a tuple. The default is None.

    Raises
    ------
    RuntimeError
        If something goes wrong creating the output dataframe.

    Returns
    -------
    df : dataframe
        A dataframe with two columns, representing the spatial coordinates, 
        the names of which are stored in col_names.

    '''
    try:
        if b is None:
            df = pd.DataFrame(a,columns=col_names)
        else:
            df = pd.DataFrame({col_names[0]:a,col_names[1]:b})
    except Exception as e: # Catch exceptions in pandas
        raise RuntimeError('An exception occurred in {function}: {error}'.\
                        format(function='pandas.DataFrame',error=e))
            
    df = _handle_missing_data_coords(df, col_names)
    return df



def _geo_series_from_wkb(geo,crs):
    '''
    Internal function to transform a WKB (Well Known Binary) geometry 
    read from Spotfire into a geo series.

    Parameters
    ----------
    geo : array-like or Series
        The geometry column in WKB format.
    crs : pyproj CRS
        The CRS of the input geometry.

    Returns
    -------
    geo_series : geopandas GeoSeries
        The transformed geometry column.
    '''
    geo_series = gpd.GeoSeries.from_wkb(geo, crs=crs)
    # Remove any possible inconsistencies in the geometry
    geo_series = geo_series.apply(lambda row: make_valid(row))
    return geo_series


def _geo_series_to_wkb(geo):
    '''
    Internal function to transform a geo series into a WKB (Well Known Binary) 
    geometry, to be returned to Spotfire.    

    Parameters
    ----------
    geo : geopandas GeoSeries
        The input geo series to transform.

    Returns
    -------
    wkb_geo : pandas Series
        The transformed binary column.

    '''
    wkb_geo = gpd.GeoSeries.to_wkb(geo)
    return wkb_geo



    
def _add_spotfire_metadata(df,geo_column_name='geometry'):
    '''
    Internal function to add Spotfire metadata to the data frame, so that 
    geometry, bounds and centroid can be automatically geo-coded by Spotfire.
    Bounds and centroid are expected to be named XMin, XMax, YMin, YMax,
    XCentroid and YCentroid.
    
    Parameters
    ----------
    df : pandas DataFrame.
        The data frame to garnish with the metadata.
        Must not be a geopandas GeoDataFrame.
    geo_column_name : str, optional
        The name of the column containing the geometry. 
        The default is 'geometry'.

    Returns
    -------
    df : pandas DataFrame
        The data frame with added Spotfire metadata.

    '''
    
    df[geo_column_name].spotfire_column_metadata = {"MapChart.ColumnTypeId": ["Geometry"], 
                                                    "ContentType": ["application/x-wkb"]}
    
    if 'XMax' in df.columns:
        df['XMax'].spotfire_column_metadata = {"MapChart.ColumnTypeId": ["XMax"]}
    if 'YMax' in df.columns:
        df['YMax'].spotfire_column_metadata = {"MapChart.ColumnTypeId": ["YMax"]}
    if 'XMin' in df.columns:
        df['XMin'].spotfire_column_metadata = {"MapChart.ColumnTypeId": ["XMin"]}
    if 'YMin' in df.columns:
        df['YMin'].spotfire_column_metadata = {"MapChart.ColumnTypeId": ["YMin"]}
    if 'XCenter' in df.columns:
        df['XCenter'].spotfire_column_metadata = {"MapChart.ColumnTypeId": ["XCenter"]}
    if 'YCenter' in df.columns:
        df['YCenter'].spotfire_column_metadata = {"MapChart.ColumnTypeId": ["YCenter"]}
    
    return df





# --- EXTERNAL FUNCTIONS ------------------------------------------------------

### GENERIC  ###

def prepare_geo_dataframe_for_spotfire(geo_df, centroid_style = 'representative'):
    '''
    Wrapper around create_shapefile_output to simplify preparing a
    geo data frame to be output back to Spotfire from a Spotfire
    Data Function.

    Parameters
    ----------
    geo_df : geopandas GeoDataFrame
        The data frame to prepare for output.
    centroid_style: str, optional.
        The way the centroid is calculated.
        See create_shapefile_output.
        The default is 'representative'.

    Raises
    ------
    RuntimeError
        If the input geo_df is not a geo data frame or if the CRS is not
        already defined within the data frame.

    Returns
    -------
    pandas DataFrame
        A data frame with calculated bounds and centroid, WKB geometry
        and Spotfire metadata for geo-coding. All the extra columns present
        in the input data frame are preserved.

    '''
    
    if not isinstance(geo_df,gpd.geodataframe.GeoDataFrame):
        raise RuntimeError('prepare_geo_dataframe_for_spotfire: You must input a geopandas GeoDataFrame.')
    
    # Extract the CRS from the input data frame
    crs = geo_df.crs
    if crs is None:
        raise RuntimeError('prepare_geo_dataframe_for_spotfire: The CRS must be defined in the data frame.')
        
    geo_column_name = geo_df.geometry.name
    
    columns = geo_df.columns.tolist()
    if len(columns)>1:
        extra_columns = geo_df.drop(columns=geo_column_name)
    else:
        extra_columns = None
    

    return create_shapefile_output(geo_df, True, crs, extra_columns, 
                                geo_column_name,
                                centroid_style = centroid_style)
        

def add_bounds_and_centroid(geo_df, centroid_style = 'representative'):
    '''
    Wrapper around create_shapefile_output to simplify adding bounds and
    centroid to a geo data frame.

    Parameters
    ----------
    geo_df : geopandas GeoDataFrame
        The data frame to prepare for output.
    centroid_style: str, optional.
        The way the centroid is calculated.
        See create_shapefile_output.
        The default is 'representative'.
    Raises
    ------
    RuntimeError
        If the input geo_df is not a geo data frame or if the CRS is not
        already defined within the data frame.

    Returns
    -------
    gropandas GeoDataFrame
        A geo data frame with calculated bounds and centroid.
        All the extra columns present in the input data frame are preserved.
    '''
    
    if not isinstance(geo_df,gpd.geodataframe.GeoDataFrame):
        raise RuntimeError('prepare_geo_dataframe_for_spotfire: You must input a geopandas GeoDataFrame.')
    
    # Extract the CRS from the input data frame
    crs = geo_df.crs
    if crs is None:
        raise RuntimeError('prepare_geo_dataframe_for_spotfire: The CRS must be defined in the data frame.')
        
    geo_column_name = geo_df.geometry.name
    
    columns = geo_df.columns.tolist()
    if len(columns)>1:
        extra_columns = geo_df.drop(columns=geo_column_name)
    else:
        extra_columns = None
    
    return create_shapefile_output(geo_df, False, crs, extra_columns, 
                                geo_column_name,
                                centroid_style = centroid_style)


def create_shapefile_output(geo_df, to_spotfire, crs='EPSG:4326',
                            extra_columns=None, 
                            geo_column_name='geometry', 
                            centroid_style = 'representative'):
    '''
    Prepare a shapefile further calculations and/or export, or else for 
    output back to Spotfire. 
    Calculate bounds and centroid.
    If this is output back to Spotfire from a Spotfire Data Function: 
    also translate geometry to WKB and set Spotfire metadata for geo-location. 
    This must be the LAST manipulation before outputting the data frame to Spotfire.
    For output to Spotfire, the returned data frame is a pandas DataFrame.
    Otherwise it will be a geopandas GeoDataFrame.
    
    Parameters
    ----------
    geo_df : geopandas GeoDataFrame
        The data frame to prepare for output.
    crs : int, str, pyproj CRS
        The CRS of the geometry, optional.
        This value is ignored if the input data frame has a defined CRS.
        The default is EPSG:4326.
    to_spotfire: bool
        If True, the data frame is prepared for output to Spotfire.
        Otherwise, the bounds and centroid are calculated.
    extra_columns : data frame, optional
        Any columnd beyond the geometry that need to be output. 
        If this data frame already contains bounds and centroid, these
        are ignored and superseded by the newly calculated ones.
        The default is None.
    geo_column_name : str, optional
        The name of the geometry column. The default is 'geometry'.
    centroid_style: str, optional
        if 'representative'  return a representative point that is guaranteed to lie
        within the perimeter;
        if 'original' calculate centroid using the current CRS, regardless of whether it is 
        geographic or projected;
        if 'projected' calculate centroid using a projected CRS, set to EPSG:6933.
        The default is 'representative'.

    Raises
    ------
    RuntimeError
        If the input geo_df is not a geo data frame.

    Returns
    -------
    output_df : pandas DataFrame, geopandas GeoDataFrame
        The output data frame. The return type depends on the value of the
        to_spotfire parameter.
    '''
    
    if not isinstance(geo_df,gpd.geodataframe.GeoDataFrame):
        raise RuntimeError('create_shapefile_output: You must send a geopandas geo dataframe.')
        
    # Extract the CRS from the input data frame, if present. 
    # If not, default to the input parameter
    current_crs = geo_df.crs
    if current_crs is not None:
        crs = current_crs
        
    crs = crs_utilities.get_crs(crs)
            
    # Calculate bounding coordinates and centers 
    shape_bounds=  shape_utilities._calculate_bounds(geo_df)
    shape_centroid= shape_utilities._calculate_centroid(crs, geo_df, 
                                                        centroid_style = centroid_style)
            
    bounds_and_centroid_columns = shape_bounds.columns.tolist() + shape_centroid.columns.tolist()
    
    if to_spotfire:
        # Translate geometry to WKB
        wkb_geometry = _geo_series_to_wkb(geo_df[geo_column_name])
        
        # Downgrade to simple pandas data frame
        output_df = pd.DataFrame({geo_column_name:wkb_geometry})
        
    else:
        # Drop any existing bounds and centroid
        output_df = geo_df.drop(bounds_and_centroid_columns, axis=1, errors='ignore')
    
    # Use newly calculated bounds and centroid
    output_df = pd.concat([output_df, shape_bounds, shape_centroid],axis=1)
    
    # Check there are columns and remove bounds and centroids from there too
    if isinstance(extra_columns,pd.core.frame.DataFrame):
        extra_columns = extra_columns.drop(bounds_and_centroid_columns, axis=1, errors='ignore')
        output_df=pd.concat([output_df,extra_columns],axis=1)

    if to_spotfire:
        # Add Spotfire metadata for geo-location
        output_df =_add_spotfire_metadata(output_df, geo_column_name)        
        
    return output_df


############################  
### MAIN DATA FUNCTIONS  ###
############################

def export_to_file(path_folder,file_name, driver, data,
                crs = 'EPSG:4326',
                geo_column_name='geometry',
                bounds_and_centroid='remove'):
    '''
    Export a data frame containing a geometry to a shapefile or geoJson file.
    Spotfire re-calculates bounds and centroids on file import. So by
    default, any calculated bounds and centroids are not exported. To
    reverse this behaviour, set bounds_and_centroid to "keep".

    Parameters
    ----------
    path_folder : str
        The folder path to export data to.
    file_name : str
        The file name to export data to. Any specified file type is
        ignored.
    driver : str
        The driver to use for writing. 
        Currently supported: shapefile or geojson.
    data : pandas DataFrame
        The data to be exported.
    crs: int, str, pyproj CRS, optional
        The CRS of the data to write. The default is 'EPSG:4326'.
    geo_column_name : str, optional
        Name of the geometry column. The default is 'geometry'.
    bounds_and_centroid : str, optional
        Option to remove bounds and centroid columns when exporting. 
        These will be re-created by Spotfire when re-importing the dataset.
        Any value except from 'remove' will result in these columns being kept.
        The default is 'remove'.

    Raises
    ------
    RuntimeError
        If the folder does not exist or if the driver is not supported.

    Returns
    -------
    None.

    '''
    import os

    # Validate crs
    crs = crs_utilities.get_crs(crs)

    # Do not create a folder, it must exist already.
    if os.path.exists(path_folder)==False:
        raise RuntimeError('The folder ',path_folder,' does not exist.')
        
    # Check the driver specified in input
    drivers_dict = dict({'shapefile':'ESRI Shapefile','geojson':'GeoJSON'})
    ftypes_dict  = dict({'shapefile':'shp','geojson':'geojson'})
    
    driver = driver.lower()
    if driver not in drivers_dict.keys():
        raise RuntimeError('The driver must be one of: '+', '.join(drivers_dict.keys()))
        
    # Remove file type if present
    file_name = file_name.split('.')[0]
    # then assign it according to the driver
    file_type = ftypes_dict[driver]
    file_name +='.'+file_type

    # Now turn it into the standard driver name
    driver = drivers_dict[driver]

    # Build complete path
    path = os.path.join(path_folder,file_name)

    # Handle geometry column: turn it into WKT if it was WKB
    geometry = data[geo_column_name]
    if not isinstance(list(geometry)[0],shapely.geometry.base.BaseGeometry):
        geometry = _geo_series_from_wkb(geometry,crs=crs)
        geometry.name = geo_column_name

    # Handle bounds and centroids
    bounds_and_centroid_columns = ['XMin','XMax','YMin','YMax','XCenter','YCenter']
    if bounds_and_centroid=='remove':
        keep_columns = list(set(data.columns.tolist()) - set(bounds_and_centroid_columns))
    else:
        keep_columns = data.columns
                
    # Create a geo dataframe with geometry and any other columns to keep
    geo_df = gpd.GeoDataFrame(data[keep_columns])
    geo_df.set_geometry(geometry, inplace=True)

    # Finally, write to file 
    geo_df.to_file(path,mode='w')  



###################################################################
# MAIN ------------------------------------------------------------
if __name__ == '__main__':
    print('Executed io_utilities')