
# --- LIBRARIES ---------------------------------------------------------------
import pandas as pd
import math
import pyproj 
import shapely
from shapely.affinity import affine_transform 
import geopandas as gpd

# spotfire_dsml libraries
from spotfire_dsml.geo_analytics import io_utilities, shape_utilities

###############################################################################
# CRS (Coordinate Reference System) Utilities 
# CRS definitions, validation and information extraction
# CRS changes for coordinates or geometries

# Use pyproj for underlying CRS operations
# Use geopandas, shapely for transformations and other calculations
###############################################################################

# --- INTERNAL FUNCTIONS ------------------------------------------------------
    
# Coordinate Reference Systems ######
    
def _is_crs_object(crs):
    '''
    Internal function to test whether the input CRS is an object of type
    pyproj CRS.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The input CRS.

    Returns
    -------
    bool
        True if this is a pyproj CRS object, False otherwise.

    '''
    return isinstance(crs,pyproj.crs.crs.CRS)


def _find_utm(lat,lon):
    '''
    Internal function to calculate UTM (Universal Transverse Mercator) zone 
    given a set of spatial coordinates in the form of latitude and longitude.

    Parameters
    ----------
    lat : float
        The latitude value.
    lon : float
        The longitude value.

    Returns
    -------
    int EPSG code
        Code for the UTM grid.

    '''
    utm_zone = str((math.floor((lon + 180) / 6 ) % 60) + 1)
    utm_zone = utm_zone.zfill(2)
    epsg_code =  '326' + utm_zone if lat >= 0 else '327' + utm_zone
    return int(epsg_code)


def _get_robinson_proj():
    '''
    Internal function to return the projection string for the Robinson 
    coordinate system.

    Returns
    -------
    proj : str
        The projection string.

    '''
    proj='+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    return proj


def _get_winkel_tripel_proj():
    '''
    Internal function to return the projection string for the Winkel Tripel 
    coordinate system.

    Returns
    -------
    proj : str
        The projection string.

    '''    
    proj='+proj=wintri'
    return proj

    
def _is_lat_lon(crs):
    '''
    Internal function to check that the CRS is the standard geographic
    latitude/longitude.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The input CRS to test.

    Returns
    -------
    bool
        True if this is the standard geographic CRS, with
        EPSG code 4326, False otherwise.

    '''    
    crs1 = get_crs(crs)
    return get_crs_code(crs1)==4326

# Projections #####

def _sitting_on_dateline(df,xmin_name='XMin',xmax_name='XMax',eps=1.E-5):
    '''
    Internal function to evaluate if a geometry is close to
    the dateline discontinuity (-180 or 180 degrees). 
    Closeness estimate depend on the value of eps. The smaller the eps, the
    stricter the comparison.

    Parameters
    ----------
    df : pandas DataFrame
        Input data frame containing min and max longitudes for each geometry.
    xmin_name : str, optional
        Name of the input column containing the minimum longitude. 
        The default is 'XMin'.
    xmax_name : str, optional
        Name of the input column containing the maximum longitude. 
        The default is 'XMax'.
    eps : float, optional
        An arbitrary small number to compare closeness. 
        The default is 1.E-4.

    Returns
    -------
    int
        A value of 0 if the geometry is not close to the discontinuity; 
        1 if it is close to 180; -1 if it is close to -180.

    '''

    if abs(df[xmin_name]+180)<eps  :
        return -1
    elif abs(df[xmax_name]-180)<eps   :
        return 1
    else:
        return 0  
    

def _translate_x(gg, dateline_sign, eps=1.E-5):
    '''
    Internal function. Use shapely's affine_transform to translate the 
    longitude coordinate by a factor. The factor is an small number where the 
    sign depends on the input sign value. 
    Points sitting close to -180 will be translated in one direction and
    points sitting close to 180 will be translated in the opposite direction,
    so they are not exactly on the dateline. 
    All other points will be untouched.
    
    Parameters
    ----------
    gg : geopandas GeoSeries
        The input geometry to translate.
    dateline_sign : int
        An int with possible values -1,0,1.
        If +1, the x dimension will be translated by -eps
        If -1, the x dimension will be translated by eps
        If 0, the x dimension will not be translated.
    eps : float, optional
        A very small number to translate by. 
        The default is 1.E-5.

    Returns
    -------
    geopandas GeoSeries
        The translated geometry.

    '''
    if dateline_sign   >0: factor = -eps
    elif dateline_sign <0: factor =  eps
    else: return gg
    return affine_transform(gg, [1,0,0,1,factor,0])
    

def _project_geometry(target_crs,geo_df,geometry_column_name='geometry', 
                    adjust_dateline=1.E-5, fix_dateline=True):
    '''
    Internal function to project a geometry. 
    If the geometry sits on top of the dateline, move it very slightly in the 
    appropriate direction, to avoid crossing the dateline when projecting. 
    This behaviour can be modified by setting fix_dateline to False.

    Parameters
    ----------
    target_crs : int, str, pyproj CRS
        The CRS to project to.
    geo_df : geopandas GeoDataFrame
        A geo data frame with at least a geometry column.
    geometry_column_name : str, optional
        Name of the geometry column. The default is 'geometry'.
    adjust_dateline : float, optional
        Small number to move longitude by if polygon is sitting on top of the
        dateline. The default is 1.E-5.
    fix_dateline: bool, optional
        True if we want to adjust geometries on the dateline, False otherwise.
        The default is True.

    Raises
    ------
    RuntimeError
        If the geo_df is not a geopandas dataframe.

    Returns
    -------
    geo_df1 : geopandas GeoDataFrame
        The dataframe containing the projected geometry.

    '''

    if not isinstance(geo_df,gpd.geodataframe.GeoDataFrame):
        raise RuntimeError('_project_geometry: You must send a geopandas dataframe.')

    geo_df.set_geometry(geometry_column_name, inplace=True)
    geo_df=pd.concat([geo_df,shape_utilities._calculate_bounds(geo_df)],axis=1)
    
    source_crs = get_crs(geo_df.crs)
    # If the original CRS is WGS 84, it is possible that we have longitudes set on the dateline.
    # If so, adjust them by adjust_dateline
    if source_crs.name == 'WGS 84' and fix_dateline:
        geo_df['__on_dateline']=geo_df.apply(_sitting_on_dateline, eps=adjust_dateline, axis=1)
        geo_df[geometry_column_name] = geo_df.apply(lambda x: 
                                                    _translate_x(x[geometry_column_name], 
                                                                x['__on_dateline'],
                                                                eps=adjust_dateline), axis=1)
        geo_df.drop(columns='__on_dateline',inplace=True)

    geo_df1 = geo_df.to_crs(target_crs,inplace=False)
    geo_df1.set_geometry(geometry_column_name, inplace=True)
    
    return geo_df1
    


# --- EXTERNAL FUNCTIONS ------------------------------------------------------

### GENERIC  ###

def get_crs(crs):
    '''
    Create and return a pyproj.CRS object from an input CRS integer or string.
    Always best to call this first, to verify the input CRS is valid.
    Specially named projections:
    Winkel Tripel (1921): https://en.wikipedia.org/wiki/Winkel_tripel_projection
    Robinson (1963): https://en.wikipedia.org/wiki/Robinson_projection
    Web Mercator (adopted by Google Maps 2005): https://en.wikipedia.org/wiki/Web_Mercator_projection
    GPS or WGS84: the WGS 84 latitude/longitude coordinate system.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The input CRS to transform into a CRS object if necessary.

    Returns
    -------
    pyproj CRS
        A CRS object.

    '''
    # If already a CRS object, do nothing
    if _is_crs_object(crs): return crs
    
    if isinstance(crs,str) and crs.lower()=='robinson':
        crs= _get_robinson_proj()
    elif isinstance(crs,str) and crs.lower()=='winkel tripel':
        crs = _get_winkel_tripel_proj()
    elif isinstance(crs,str) and crs.lower()=='web mercator':
        crs = 3857
    elif isinstance(crs,str) and crs.lower()=='gps':
        crs = 4326
    elif isinstance(crs,str) and crs.lower()=='wgs84':
        crs = 4326

    return pyproj.CRS.from_user_input(crs)


def get_crs_code(crs):
    '''
    Return the EPSG code assigned to the CRS, or None if a match is not found.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The input CRS.

    Returns
    -------
    int or None
        The EPSG code of the input CRS.

    '''
    crs = get_crs(crs)
    return crs.to_epsg(min_confidence=70)  


def serialize_crs(crs):
    '''
    Return a descriptive and formatted string with information about the CRS.
    The information returned is:
    - Name, Datum, Ellipsoid, Prime Meridian, Scope, Coordinate System,
    - Axis info, Area of use, Units.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The input CRS.

    Returns
    -------
    info : str
        Information on the CRS.

    '''
    crs = get_crs(crs)
    crs_info = [None]*9
    crs_info[0] = 'NAME: '+str(crs.name)
    crs_info[1] = 'Datum: '+str(crs.datum)
    crs_info[2] = 'Ellipsoid: ' + str(crs.ellipsoid)
    crs_info[3] = 'Prime Meridian: ' + str(crs.prime_meridian)
    crs_info[4] = 'Scope: ' + str(crs.scope)
    crs_info[5] = 'Coordinate System: ' + str(crs.coordinate_system)
    tmp=crs.axis_info
    tmp=[str(x) for x in tmp]
    tmp = '\n'.join(tmp)
    crs_info[6] = 'Axis info: \n' + tmp
    crs_info[7] = 'Area of use: \n' + str(crs.area_of_use)   
    crs_info[8] = 'Units: ' + str(crs_coordinate_units(crs))
    info = '\n\n'.join(crs_info)
    return info


def crs_is_projected(crs):
    '''
    Check whether the input CRS is projected, i.e. a coordinate system
    that has been flattened into cartesian coordinates using a map projection.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The input CRS.

    Returns
    -------
    bool
        True if CRS is projected, False otherwise.

    '''
    crs2 = get_crs(crs)
    return crs2.is_projected


def crs_coordinate_units(crs):
    '''
    Return the coordinate units of the CRS, if available.
    Expects the coordinates to be in the same unit, therefore only
    grabs the first value of the vector containing the units.
    If units not found or there is not a single unit, return None.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The input CRS.

    Returns
    -------
    crs_unit : str, None
        The coordinate units for the CRS (single value).

    '''
    crs = get_crs(crs)
    try:
        crs_dict=crs.coordinate_system.to_json_dict()
        crs_axes=crs_dict['axis']
        crs_units = [x['unit'] for x in crs_axes]
        crs_units=list(set(crs_units))
        if len(crs_units)==1:
            crs_unit=crs_units[0]
        else:
            crs_unit=None
    except:
        crs_unit=None
    
    return crs_unit


def calculate_utm(a, b=None):
    '''
    Calculate the EPSG code for the UTM (Universal Transverse Mercator)
    based on the location of each latitude, longitude coordinate.
    It is assumed the coordinates are in EPSG:4326 - WGS 84 latitude/longitude 
    coordinate system.

    Parameters
    ----------
    a : tuple or array-like
        The coordinates (if a tuple) or the first coordinate (if an array).
    b : array_like, optional
        The second coordinate (if a is a vector) or empty if a is a tuple. 
        The default is None.

    Returns
    -------
    utm : int
        The EPSG code of the UTM zone for every coordinate pair.

    '''
    coords_df = io_utilities._input_coordinates(['lat','lon'],a,b)
    utm = coords_df[['lat','lon']].apply(lambda x: _find_utm(*x), axis=1)
    return utm


def calculate_median_utm(a, b=None):
    '''
    Calculate the median UTM based on the UTM for each pair of input 
    latitude, longitude coordinates.
    It is assumed the coordinates are in EPSG:4326 - WGS 84 latitude/longitude 
    coordinate system.

    Parameters
    ----------
    a : tuple or array-like
        The coordinates (if a tuple) or the first coordinate (if an array).
    b : array-like, optional
        The second coordinate (if a is a vector) or empty if a is a tuple. 
        The default is None.

    Returns
    -------
    median_utm : int
        The median UTM EPSG code for the input set of coordinates.

    '''
    utm=calculate_utm(a,b)
    median_utm = utm.median()
    return int(median_utm)


############################  
### MAIN DATA FUNCTIONS  ###
############################

def change_crs_coordinates(source_crs, target_crs, a, b=None, extra_columns=None):
    '''
    Change CRS for a set of coordinates input as numeric columns. 
    The input coordinates can be expressed as:
    - A single vector containing tuples of two values, e.g. a=[(46.7, 120.3), (50.2, 100.0)], or 
    - Two separate vectors, e.g. a=[46.7,50.2] and b=[120.3,100.0].
    Expected order: latitude, longitude (if expressed in geographic 
    coordinates) or x, y (if expressed in projected coordinates).
    The projected coordinates will be returned as a data frame with two numeric
    columns, corresponding to the projections.
    Any input rows with missing coordinates will be removed.

    Parameters
    ----------
    source_crs : int, str, pyproj CRS
        The current CRS.
    target_crs : int, str, pyproj CRS
        The target CRS to project to.
    a : tuple or array-like
        The coordinates (if a tuple) or the first coordinate (if an array).
    b : array-like, optional
        The second coordinate (if a is a vector) or empty if a is a tuple. 
        The default is None.
    extra_columns : pandas DataFrame, optional
        A data frame of the same length as the input coordinates, containing
        extra columns that needs preserving in output. 
        The default is None.
        
    Returns
    -------
    new_coords_df : pandas DataFrame
        A data frame containing the projected coordinates as two columns.
        If the target CRS is projected, the names of these columns will be 
        x and y.
        If the target CRS is geographic, the names of these columns will be 
        lat and lon. 

    '''
    
    source_crs = get_crs(source_crs)
    target_crs = get_crs(target_crs)
            
    # Create point geometries
    # Missing data handled inside this function
    geo_points_df = shape_utilities.create_points_from_coordinates(source_crs, a,b)

    target_is_projected = crs_is_projected(target_crs)
    
    # Change CRS 
    geo_points_df.to_crs(crs=target_crs,inplace=True)
    
    # Go back to coordinates
    new_coords_df = geo_points_df['geometry'].get_coordinates()
    if target_is_projected:
        col_names=['x','y']
        new_coords_df.columns=col_names
    else:
        col_names=['lon','lat']
        new_coords_df.columns=col_names
        # Return to original order of lat and lon
        new_coords_df=new_coords_df[['lat','lon']]
            
    # Add any required extra columns. 
    # Left merge by the index as we may have removed rows with missing coordinates
    if isinstance(extra_columns,pd.core.frame.DataFrame):
        new_coords_df=pd.merge(new_coords_df,extra_columns, 
            left_index=True, right_index=True,how='left')
    return new_coords_df
        

def change_crs_geometry(geometry, target_crs, source_crs = 'EPSG:4326', extra_columns=None, 
                        geo_column_name='geometry',to_spotfire=True, 
                        adjust_dateline=1.E-5, fix_dateline=True,
                        centroid_style = 'representative'):
    '''
    Change CRS for a geometry column. By default the geometry is turned into 
    WKB (binary) for output back to Spotfire. This can be avoided by setting the
    to_spotfire parameter to False.
    Geometries crossing the dateline are not specifically handled. 
    From Geopandas documentation:
    "Objects crossing the dateline (or other projection boundary) 
    will have undesirable behavior."
    However, geometries with geographic boundaries that sit on longitude 
    -180 or 180 will be moved along the longitude by a small number 
    (default: 1E-5) so that the projection does not stretch the geometry 
    across the world. This behaviour can be removed by setting fix_dateline 
    to False.

    Parameters
    ----------
    geometry : geopandas GeoDataFrame or GeoSeries
        The input geometry to project.
    target_crs : int, str, pyproj CRS
        The projection CRS.
    source_crs : int, str, pyproj CRS, optional
        The current CRS. If the input geometry is a geo data frame with a defined CRS,
        it must be the same as this. 
        The default is 'EPSG:4326'.
    extra_columns : pandas DataFrame, optional
        A data frame of the same length as the input geometry, containing
        extra columns that needs preserving in output. 
        The default is None.
    geo_column_name : str, optional
        The name of the geometry column. 
        The default is 'geometry'.
    to_spotfire : bool, optional
        If True, the resulting data frame is prepared for being output into
        Spotfire. 
        The default is True.
    adjust_dateline : float, optional
        If fix_dateline is True, this is the amount used for checking proximity 
        to the (-180,180) discontinuity for geographic coordinates. 
        Ignored if fix_dateline is False.
        The default is 1.E-5.
    fix_dateline : bool, optional
        If True, shift longitudes that are on top of the (-180,180) discontinuity
        by the amount in adjust_dateline. 
        The default is True.
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
        If the input geometry is not called geo_column_name or if the CRS or the 
        input geometry (if defined) is different from the specified source_crs.

    Returns
    -------
    output_df : pandas DataFrame
        A data frame with the projected geometry, any specified extra columns,
        plus calculated bounds and centroid. If to_spotfire is True, this data
        frame's geometry is converted to WKB for output into a Spotfire
        data table.

    '''
    source_crs = get_crs(source_crs)
    target_crs = get_crs(target_crs)

    # Extract the geometry if not already a geo series
    geometry_crs = None
    if isinstance(geometry, gpd.geodataframe.GeoDataFrame):
        try:
            geometry = geometry[geo_column_name]
            # Extract the source_crs and compare with the one from input
            geometry_crs = geometry.crs
        except:
            raise RuntimeError('change_crs_geometry: The column '+geo_column_name+' is not a geometry')

    
    if geometry_crs is not None and geometry_crs != source_crs:
        raise RuntimeError("change_crs_geometry: The input geometry's CRS is not the same as the source_crs")

    # Handle missing data, including optional extra_columns data frame
    geometry, extra_columns = io_utilities._handle_missing_data_geometry(geometry, extra_columns)

    # Translate geometry from wkb if it is not already a shapely geometry
    if not isinstance(list(geometry)[0],shapely.geometry.base.BaseGeometry):
        geometry = io_utilities._geo_series_from_wkb(geometry,crs=source_crs)
        
    # Build a new geo dataframe
    geo_df = gpd.GeoDataFrame({geo_column_name:geometry})
    geo_df.set_geometry(geo_column_name)

    # Project to new crs
    output_df=_project_geometry(target_crs,geo_df, geometry_column_name=geo_column_name,
                                adjust_dateline=adjust_dateline, fix_dateline=fix_dateline)


    # Prepare from Spotfire output if required
    output_df =io_utilities.create_shapefile_output(output_df, 
                                                        to_spotfire,
                                                        target_crs, 
                                                        extra_columns, 
                                                        geo_column_name,
                                                        centroid_style = centroid_style)
        
    
    return output_df



###################################################################
# MAIN ------------------------------------------------------------
if __name__ == '__main__':
    print('Executed crs_utilities')