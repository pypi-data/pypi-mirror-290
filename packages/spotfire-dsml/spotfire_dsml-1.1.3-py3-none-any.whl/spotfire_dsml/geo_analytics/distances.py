
# --- LIBRARIES ---------------------------------------------------------------
import pandas as pd
import numpy as np
import time
import itertools
from geopy.distance import geodesic 

# spotfire_dsml libraries
from spotfire_dsml.geo_analytics import crs_utilities, io_utilities

###############################################################################
# Distances:
# Utilities for calculating geographic or cartesian distances

# Use geopy for geodesic distances
###############################################################################

# --- GLOBAL SETTINGS ---------------------------------------------------------
pd.options.mode.chained_assignment = None  # default='warn'

# --- INTERNAL FUNCTIONS ------------------------------------------------------

def _approx_earth_radius(lat1,lon1,lat2,lon2,ecc2,r_eq):
    '''
    Internal function to calculate the earth radius of curvature between
    two points.

    Parameters
    ----------
    lat1 : float
        The latitude of the first point.
    lon1 : float
        The longitude of the first point.
    lat2 : float
        The latitude of the second point.
    lon2 : float
        The longitude of the second point.
    ecc2 : float
        The squared earth eccentricity.
    r_eq : float
        The earth radius at the equator in meters.

    Returns
    -------
    R : float
        The radius to use to approximate a local radius in haversine.

    '''
    # References:
    # https://en.wikipedia.org/wiki/Earth_radius (Radii of curvature)
    # Lectures from James Clynch: http://clynchg3c.com/Technote/Tnotes.htm  (not secure site)
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # Initial bearing, or forward azimuth
    # https://www.movable-type.co.uk/scripts/latlong.html
    # atan2( sin Δλ * cos φ2 , cos φ1 * sin φ2 − sin φ1 * cos φ2 * cos Δλ )
    bearing = np.arctan2(np.sin(lon2-lon1)*np.cos(lat2),  np.cos(lat1)*np.sin(lat2)-np.sin(lat1)*np.cos(lat2)*np.cos(lon2-lon1)   )
    factor0 = 1-ecc2
    factor1 = 1-ecc2 * np.sin(lat1)**2
    # Earth azimuthal radius of curvature at latitude lat1
    # combines Prime Vertical radius and Meridional radius, simplified algebraic expression
    R = r_eq/((np.cos(bearing)**2 * factor1/factor0 + np.sin(bearing)**2 ) * np.sqrt(factor1)) 

    return R


def _haversine_distance(lat1,lon1,lat2,lon2,R=6371000):
    '''
    Internal function to calculate haversine (great circle) distance between 
    two points.
    The average earth radius in meters (6371000) is used by default.
    The distance is returned in meters.
    
    Parameters
    ----------
    lat1 : float
        The latitude of the first point.
    lon1 : float
        The longitude of the first point.
    lat2 : float
        The latitude of the second point.
    lon2 : float
        The longitude of the second point.
    R : float, optional
        The earth radius in meters. The default is 6371000.

    Returns
    -------
    distance : float
        The haversine distance in meters between the two points.

    '''
    lat1,lon1,lat2,lon2 = map(np.radians, [lat1,lon1,lat2,lon2])
    hav = np.sin((lat2 - lat1)*0.5)**2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1)*0.5)**2    
    distance = 2 * R * np.arcsin(np.sqrt(hav)) 
    return distance

def _geodesic_distance(point1,point2):
    '''
    Internal function to calculate distance between two points using 
    geopy.distance with the geodesic method. The ellipsoid is the default one.
    The distance is returned in meters.

    Parameters
    ----------
    point1 : tuple(float)
        The latitude and longitude of the first point.
    point2 : tuple(float)
        The latitude and longitude of the second point.

    Returns
    -------
    distance : float
        The geodesic distance in meters between the points.

    '''
    distance = geodesic(point1,point2).meters 
    return distance

def _cartesian_distance(x1,y1,x2,y2):
    '''
    Internal function to calculate the cartesian distance (distance on a plane) 
    between two points.
    The points' coordinates are expected to be expressed in meters and so is 
    the returned distance.

    Parameters
    ----------
    x1 : float
        The X value of the first point.
    y1 : float
        The Y value of the first point.
    x2 : float
        The X value of the second point.
    y2 : float
        The Y value of the second point.

    Returns
    -------
    float
        The cartesian distance in meters between the points.

    '''
    return np.sqrt((x1-x2)**2+(y1-y2)**2)

# --- EXTERNAL FUNCTIONS ------------------------------------------------------

# The most flexible version
# Always calculates distance in meters first

def calculate_earth_distance(crs,unit,distance_method,nn_method,first_axis1,
                             second_axis1,first_id=None,
                             first_axis2=None,second_axis2=None,
                             second_id=None):
    '''
    Main function to calculate the distance between two sets of points.
    Flat distance: no altitude correction.
    Any or all of:
    - Haversine (for Spherical CRS)
    - Haversine with local radius approximation (for Spherical CRS)
    - Geodesic (for Spherical CRS)
    - Cartesian (for Projected CRS)
    
    Calculate Nearest Neighbours for any or all distances.
    Limit output to distance buffer, if specified.
    Calculate distances within one dataset or between two datasets.

    The user can specify multiple distance methods and nearest-neighbour 
    evaluation methods in lists. The nearest-neighbour methods must be
    a subset of the distance methods.
    
    Only distances compatible with the CRS of the input coordinates
    can be calculated within a single call. I.e. geographic (angular) distances
    cannot be calculated in the same call as cartesian distances.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The CRS of the input coordinates.
    unit : str
        The desired unit for the distance calculation.
    distance_method : str, list(str)
        The method or list of methods to use.
        All or any of 'haversine', 'haversine_r', 'geodesic', 'cartesian'.
    nn_method : str, list(str)
        The method of list of methods to use for evaluating nearest neighbours.
        If must be a subset of distance_method.
    first_axis1 : array-like
        The x axis or the latitude of the first set of points.
    second_axis1 : array-like
        The y axis or the longitude of the first set of points.
    first_id : array-like, optional
        The row identifier for the first set of points.
        If not specified, a vector with prefix 'ID1' will be generated.
        The default is None.
    first_axis2 : array-like, optional
        The x axis or the latitude of the second set of points. 
        If not specified, the distances within the first set of points
        will be calculated.
        The default is None.
    second_axis2 : array-like, optional
        The y axis or the longitude of the second set of points. 
        If not specified, the distances within the first set of points
        will be calculated. The default is None.
    second_id : array-like, optional
        The row identifier for the second set of points. 
        If not specified, and first_axis2 and second_axis2 are not None,
        a vector with prefix 'ID2' will be generated. 
        If not specified, and first_axis2 and second_axis2 are None,
        the vector for first_id will be used. 
        The default is None.

    Raises
    ------
    RuntimeError
        If the specified distance method is not implemented, or if
        the nearest-neighbour method is not a subset of the distance
        method; or if the distance method is "cartesian" but the coordinates
        are specified in a geographic CRS, or if the distance method is
        not "cartesian" but the coordinates are in a projected CRS.

    Returns
    -------
    combo : pandas DataFrame
        A distance matrix with one row per pair of points, one column
        per distance method and one column per nearest-neighbour method.
    time_dict : dict
        A dictionary with the elapsed time for the distance calculations.

    '''

    # If we only have specified one distance method, put it into a list
    if isinstance(distance_method,str):  distance_method = [distance_method]
    # Same for the nearest neighbour method
    if isinstance(nn_method,str):  nn_method = [nn_method]

    # Check distance and nearest neighbours methods
    methods = ['haversine','haversine_r','geodesic','cartesian']
    if not set(distance_method).issubset(set(methods)):
        raise RuntimeError('calculate_earth_distance: incorrect distance method, should be in ',','.join(methods))
    if not set(nn_method).issubset(set(distance_method)):
        raise RuntimeError('calculate_earth_distance: incompatible nearest neighbour method, should be in ',','.join(distance_method))
       

    # Unit can be metres, kilometers, feet or miles, in a few spelling formats
    unit_factor = io_utilities._convert_unit('metre', unit)

    # Determine which distance calculations are allowed with this crs
    crs_is_projected = crs_utilities.crs_is_projected(crs)
    if crs_is_projected and 'cartesian' not in distance_method:
        raise RuntimeError('calculate_earth_distance: You can only calculate cartesian distances with a projected coordinate system')
    if crs_is_projected==False and 'cartesian' in distance_method:
        raise RuntimeError('calculate_earth_distance: You can not calculate cartesian distances with a geographic coordinate system')
        
    single_table=False
    # Create the two data frames
    first_id = io_utilities._check_id(first_id, len(first_axis1), 'ID1')
    table1 = pd.DataFrame({'first_axis':first_axis1,'second_axis':second_axis1,'id':first_id})
    table1 = io_utilities._handle_missing_data_coords(table1,['first_axis','second_axis'])
    
    # Work out whether there is one or two tables
    # Ideally the caller did not define a second table... but this is
    # not guaranteed
    if first_axis2 is not None and second_axis2 is not None \
        and not first_axis1.equals(first_axis2) \
        and not second_axis1.equals(second_axis2):
        second_id = io_utilities._check_id(second_id, len(first_axis2), 'ID2')
        table2 = pd.DataFrame({'first_axis':first_axis2,'second_axis':second_axis2,'id':second_id})
        table2 = io_utilities._handle_missing_data_coords(table2,['first_axis','second_axis'])

    else:
        single_table=True
        table2=table1.copy()   
        
    # Join the tables with a full join
    combo=table1.merge(table2, how='cross')

    if single_table:
        # Handle self joins within the same dataset
        combo=combo.loc[combo['id_x']!=combo['id_y']]
        # Concatenate ids in order to identify distinct pairs
        combo['id_xy'] = ['_'.join(x) for x in np.sort(combo[['id_x','id_y']])]
        # Keep only distinct pairs
        combo.drop_duplicates(subset='id_xy',inplace=True)
        combo.drop(columns=['id_xy'], inplace=True)
    
    # If we only have specified one distance method, put it into a list
    if isinstance(distance_method,str):  distance_method = [distance_method]
    
    time_dict = dict.fromkeys(distance_method)
    for ddm in distance_method:
        if ddm=='haversine':
            time_start =time.time()
            combo['distance_'+ddm] = _haversine_distance(combo['first_axis_x'],combo['second_axis_x'],
                                                         combo['first_axis_y'],combo['second_axis_y'])
            time_dict[ddm]=time.time()-time_start
        elif ddm=='haversine_r':
            radius_equator = 6378137.0  # equatorial radius in m (semi major axis)           
            radius_pole    = 6356752.3 # polar radius in m (semi minor axis)
            eccentricity2 = 1-(radius_pole**2/radius_equator**2) #squared eccentricity of an ellipse
            time_start =time.time()
            combo['earth_radius']= [_approx_earth_radius(x1,y1,x2,y2,eccentricity2,radius_equator) 
                                    for x1,y1,x2,y2 in zip(combo['first_axis_x'],combo['second_axis_x'],
                                                           combo['first_axis_y'],combo['second_axis_y'])]
            combo['distance_'+ddm] = _haversine_distance(combo['first_axis_x'],combo['second_axis_x'],
                                                         combo['first_axis_y'],combo['second_axis_y'],
                                                         combo['earth_radius'])
            time_dict[ddm]=time.time()-time_start
            combo.drop(columns=['earth_radius'], inplace=True)
        elif ddm == 'geodesic':
            time_start =time.time()
            a = list(zip(combo['first_axis_x'],combo['second_axis_x']))
            b = list(zip(combo['first_axis_y'],combo['second_axis_y']))
            combo_points = list(zip(a, b))
            combo['distance_'+ddm]  = [i for i in itertools.starmap(_geodesic_distance, combo_points)]
            
            # Neater but slower
            #combo['p1']=list(zip(combo['first_axis_x'],combo['second_axis_x']))
            #combo['p2']=list(zip(combo['first_axis_y'],combo['second_axis_y']))
            #combo['distance_'+ddm]  = combo[['p1','p2']].apply(lambda x: _geodesic_distance(*x), axis=1)
           
            time_dict[ddm]=time.time()-time_start
        elif ddm=='cartesian':
            time_start =time.time()
            combo['distance_'+ddm] = combo[['first_axis_x','second_axis_x',
                                            'first_axis_y','second_axis_y']].apply(lambda x: _cartesian_distance(*x), axis=1)
            time_dict[ddm]=time.time()-time_start    

        # Cast distance from metres to desired unit
        combo['distance_'+ddm] = combo['distance_'+ddm] *unit_factor

    ## NEAREST NEIGHBOURS
    # If we only have specified one nearest neighbour method, put it into a list
    if set(nn_method).issubset(distance_method) == False:
        raise RuntimeError('calculate_earth_distance: the method for calculating nearest neighbours must be one of the selected distance methods.')
        
    for nnm in nn_method:
        combo['nn_rank_'+nnm] = combo.groupby(['id_x'])['distance_'+nnm].rank('dense', ascending=True)
        
    # Rename columns appropriately
    coords_columns=['first_axis_x','second_axis_x','first_axis_y','second_axis_y','id_x','id_y']
    if crs_is_projected:
        rename_columns = ['x1','y1','x2','y2','id1','id2']
    else:
        rename_columns = ['lat1','lon1','lat2','lon2','id1','id2']
    rename_dict = { k:v for (k,v) in zip(coords_columns, rename_columns)} 
    combo.rename(columns=rename_dict,inplace=True)

    return (combo,time_dict)

# Targeted versions **************************************************

def calculate_distance_matrix(crs,unit,buffer,distance_method,first_axis1,
                             second_axis1,first_id=None,
                             first_axis2=None,second_axis2=None,
                             second_id=None):
    '''
    Wrapper around calculate_earth_distance to calculate the distance between 
    two sets of points with a single method.

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The CRS of the input coordinates.
    unit : str
        The desired unit for the distance calculation.
    buffer : float
        The maximum distance to be returned, in the same units.
        If buffer is specified as None, all distances will be returned.
    distance_method : str
        The method to use.
        One of 'haversine','haversine_r','geodesic','cartesian'
        The nearest neighbours will be calculated with the same method.
    first_axis1 : array-like
        The x axis or the latitude of the first set of points.
    second_axis1 : array-like
        The y axis or the longitude of the first set of points.
    first_id : array-like, optional
        The row identifier for the first set of points.
        If not specified, a vector with prefix 'ID1' will be generated.
        The default is None.
    first_axis2 : array-like, optional
        The x axis or the latitude of the second set of points. 
        If not specified, the distances within the first set of points
        will be calculated.
        The default is None.
    second_axis2 : array-like, optional
        The y axis or the longitude of the second set of points. 
        If not specified, the distances within the first set of points
        will be calculated. The default is None.
    second_id : array-like, optional
        The row identifier for the second set of points. 
        If not specified, and first_axis2 and second_axis2 are not None,
        a vector with prefix 'ID2' will be generated. 
        If not specified, and first_axis2 and second_axis2 are None,
        the vector for first_id will be used. 
        The default is None.

    Returns
    -------
    distance_matrix : pandas DataFrame
        A distance matrix with one row per pair of points, one column
        for the distance and one column per nearest-neighbours.        
        If the buffer is too small, and the resulting distance matrix
        has no rows, a distance matrix with all zero distances between
        each point for the first set and itself, and all nearest neighbours 
        set to 1 will be returned, to avoid returning an empty data frame.

    '''
        
    # Distance is calculated in the required units
    distance_matrix, _ = calculate_earth_distance(crs,unit,distance_method,distance_method,
                                                  first_axis1,
                                                  second_axis1,first_id,
                                                  first_axis2,second_axis2,
                                                  second_id)
    
    # Rename to standard column names
    distance_matrix.rename(columns={"distance_"+distance_method: "distance", "nn_rank_"+distance_method: "nn_rank"}, inplace=True)
    
    if buffer is not None:
        distance_matrix = distance_matrix.loc[distance_matrix['distance']<=buffer]
        if distance_matrix.shape[0]==0:
            # Return something: the distance of each point to itself
            first_id = io_utilities._check_id(first_id, len(first_axis1))
            cols = distance_matrix.columns
            cols_first = [c for c in cols if c.endswith('1')]
            cols_second = [c for c in cols if c.endswith('2')]
            distance_matrix=pd.DataFrame(data=zip(first_axis1,second_axis1,
                                                  first_id,first_axis1,
                                                  second_axis1,first_id),
                                         columns=cols_first+cols_second)

            distance_matrix['distance']=0.0
            distance_matrix['nn_rank']=1 
            
    
    return distance_matrix


# Return a table with the source dataset and the details of its nearest neighbour from the target dataset
# Optional a table with connecting lines
#check inputs to earth distance!!!!
def calculate_nearest_neighbors(crs,distance_unit,distance_method,first_axis1,
                             second_axis1,first_id=None,
                             first_axis2=None,second_axis2=None,
                             second_id=None):
    '''
    

    Parameters
    ----------
    
    crs : int, str, pyproj CRS
        The CRS of the input coordinates.
    distance_unit : str
        The desired unit for the distance calculation.
    distance_method : str
        The method to use.
        One of 'haversine','haversine_r','geodesic','cartesian'
        The nearest neighbours will be calculated with the same method.
    first_axis1 : array-like
        The x axis or the latitude of the first set of points.
    second_axis1 : array-like
        The y axis or the longitude of the first set of points.
    first_id : array-like, optional
        The row identifier for the first set of points.
        If not specified, a vector with prefix 'ID1' will be generated.
        The default is None.
    first_axis2 : array-like, optional
        The x axis or the latitude of the second set of points. 
        If not specified, the distances within the first set of points
        will be calculated.
        The default is None.
    second_axis2 : array-like, optional
        The y axis or the longitude of the second set of points. 
        If not specified, the distances within the first set of points
        will be calculated. The default is None.
    second_id : array-like, optional
        The row identifier for the second set of points. 
        If not specified, and first_axis2 and second_axis2 are not None,
        a vector with prefix 'ID2' will be generated. 
        If not specified, and first_axis2 and second_axis2 are None,
        the vector for first_id will be used. 
        The default is None.

    Raises
    ------
    RuntimeError
        If an error occurs with the calculation.

    Returns
    -------
    nearest_neighbor : pandas DataFrame
        A distance matrix between all points of the first set and
        their nearest neighbours from the second set (or from all
        pairs within the first set).
    lines : pandas DataFrame
        A table with two rows for each point, specifying the start and end
        of the line connecting a point to its nearest neighbour.

    '''
    # The unit does not matter for nearest neighbour but still should matter
    # for the distance results
    nn_method = distance_method
    nearest_neighbor, _ = calculate_earth_distance(crs,distance_unit,distance_method,nn_method,
                                                  first_axis1,
                                                  second_axis1,first_id,
                                                  first_axis2,second_axis2,
                                                  second_id)
    
    
    nearest_neighbor.rename(columns={"distance_"+distance_method: "distance", "nn_rank_"+distance_method: "nn_rank"}, inplace=True)
    #Keep only the first neighbour for dataset 1
    nearest_neighbor = nearest_neighbor.loc[nearest_neighbor['nn_rank']==1]
    nearest_neighbor.drop(columns='nn_rank',inplace=True)
    columns_set = set(nearest_neighbor.columns)
    # Generate a dataset with connecting lines
    spherical_coords0=['lat','lon']
    spherical_coords1 = ['lat1','lon1']
    spherical_coords2 = ['lat2','lon2']
    spherical_coords = spherical_coords1+spherical_coords2
    projected_coords0=['x','y']
    projected_coords1 = ['x1','y1']
    projected_coords2 = ['x2','y2']
    projected_coords = projected_coords1+projected_coords2
    if set(spherical_coords).issubset(columns_set):
        coords0 = spherical_coords0
        coords  = spherical_coords
        coords1 = spherical_coords1
        coords2 = spherical_coords2
    elif set(projected_coords).issubset(columns_set):
        coords0 = projected_coords0
        coords = projected_coords
        coords1 = projected_coords1
        coords2 = projected_coords2
    else:
        raise RuntimeError('calculate_nearest_neighbors: unexpected column names')
       
    lines = nearest_neighbor[coords]
    n_lines = lines.shape[0]+1
    lines['line_id']=list(range(1,n_lines))
    lines1 = lines[['line_id']+coords1]
    lines1.columns=['line_id']+coords0
    lines1['type']='source'
    lines2 = lines[['line_id']+coords2]
    lines2.columns=['line_id']+coords0
    lines2['type']='target'
    lines = pd.concat([lines1,lines2],axis=0)
    return (nearest_neighbor,lines)

### THE END