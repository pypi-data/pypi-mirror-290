
# --- LIBRARIES ---------------------------------------------------------------
import pandas as pd
import numpy as np
import shapely
import geopandas as gpd

# spotfire_dsml libraries
from spotfire_dsml.geo_analytics import crs_utilities, io_utilities, shape_utilities

###############################################################################
# Spatial Joins:
# Calculations involving joining two or more geometries.

# Use geopandas, shapely for transformations and other calculations
###############################################################################

# --- EXTERNAL FUNCTIONS ------------------------------------------------------

def points_in_polygons(polygon_geometry,polygon_id,point_first_coordinate,
                    point_second_coordinate,point_id, 
                    return_near_matches=False,max_distance=0.0, distance_unit = 'metre',
                    handle_multiple_matches='join',
                    source_crs='EPSG:4326',projected_crs='EPSG:3857'):
    '''
    Function to compare the positions of a set of point coordinates to a set of 
    polygon-like geometries, to find which polygon the points fall within.
    If requested, points which are close, but not quite inside, a polygon
    can be matched too. This may be useful if polygons approximate a
    rugged coastline for instance, and points are located near the coast.

    Parameters
    ----------
    polygon_geometry : geopandas GeoSeries
        A vector containing the geometry of the polygons to match to.
    polygon_id : array-like
        A vector containing the ids of the polygons.
        Expected data types are integer or string.
    point_first_coordinate : array-like
        A vector of floats containing the latitude (or the x coordinate) of the points.
    point_second_coordinate : array-like
        A vector of floats containing the longitude (or the y coordinate) of the points.
    point_id : array-like
        A vector containing the ids of the points.
    return_near_matches : bool, optional
        If True, also match points that are close to polygons within a
        specified buffer distance. 
        The default is False.
    max_distance : float, optional
        If return_near_matches is True, the buffer distance to use. 
        If specified, must be greater than zero for the near matches
        to be calculated.
        Ignored if return_near_matches is False.
        The default is 0.0.
    distance_unit : str, optional
        The unit for max_distance. 
        The default is 'metre'.
    handle_multiple_matches: str, optional
        One of {'join','random_select'}.
        If 'join' then the resulting polygon_id is the concatenation of
        all matches, in alphabetical order. If 'random_select' then the
        resulting polygon_id is a randomly selected match.
    source_crs : int,str, pyproj CRS, optional
        The current CRS of the input points and geometries. 
        The default is 'EPSG:4326'.
    projected_crs : int,str, pyproj CRS, optional
        The projected CRS to use when calculating near matches. 
        The default is 'EPSG:3857'.

    Raises
    ------
    RuntimeError
        If the projected_crs is not a projected CRS, or if handle_multiple_matches
        is not recognized.

    Returns
    -------
    polygon_id : pandas Series
        The id of the matched polygon, or empy if no match found.
        One row per initial point.
    distance_metres : pandas Series
        The distance from the closest polygon in meters, if a near-match, 
        or zero otherwise.
        One row per initial point.

    '''
    
    source_crs=crs_utilities.get_crs(source_crs)
    projected_crs=crs_utilities.get_crs(projected_crs)
    if not crs_utilities.crs_is_projected(projected_crs):
        raise RuntimeError('points_in_polygons: The crs ',projected_crs,' should be projected.')
        
    #Polygons -------------------------
    # Translate geometry from wkb if it is not already a shapely geometry
    if not isinstance(list(polygon_geometry)[0],shapely.geometry.base.BaseGeometry):
        polygon_geometry = io_utilities._geo_series_from_wkb(polygon_geometry,crs=source_crs)
        
    # Temporarily cast polygon_id to a string, but keep the original data type
    if not isinstance(polygon_id,pd.Series):
        #pandas can represent integer data with possibly missing values using
        # "Int64" (note the capital "I") to differentiate from NumPy’s 'int64' dtype
        nullable_int = pd.Int64Dtype() 
        if isinstance(polygon_id[0],int): 
            polygon_id = pd.Series(polygon_id, dtype=nullable_int)
        else:
            polygon_id = pd.Series(polygon_id)
            
    # Save the data type of the polygon id
    polygon_id_dtype = polygon_id.dtype
    # Temporarily turn it into a string
    polygon_id = polygon_id.astype(str)

    # Build a new geo dataframe
    polygons_gdf = gpd.GeoDataFrame({'geometry':polygon_geometry})
    polygons_gdf['polygon_id']=polygon_id
    
    #Points -----------------------------------
    points_gdf=shape_utilities.create_points_from_coordinates(source_crs,
                                                            point_first_coordinate,
                                                            point_second_coordinate)
    points_gdf['point_id']=point_id
    
    #################################################################################
    # Spatial Join
    result = gpd.tools.sjoin(points_gdf, polygons_gdf, how="left",predicate='intersects')
    
    # Post-process 1:
    # If we have any missed coordinates, add some info on nearest polygon
    if max_distance is not None:
        if max_distance <= 1.0E-4: return_near_matches=False
    
    missed=result.loc[pd.isna(result['polygon_id'])]
    if len(missed)>0 and return_near_matches:
        max_distance_metres = max_distance * io_utilities._convert_unit(distance_unit, 'metre')
        missed_coordinates_index=missed.index
        missed_coordinates=points_gdf.iloc[missed_coordinates_index]
        missed_coordinates=missed_coordinates.to_crs(crs=projected_crs)
        
        polygons_gdf_tmp=polygons_gdf.to_crs(crs=projected_crs)
        result2 = gpd.tools.sjoin_nearest(missed_coordinates, polygons_gdf_tmp, 
                                        how='left',
                                        max_distance=max_distance_metres,
                                        distance_col='distance_metres')
        result2=result2.to_crs(crs=source_crs)

        #print (result2.loc[~result2['polygon_id'].isna()])
        result3=result.drop(missed_coordinates_index,axis=0)
        result=pd.concat([result2,result3])
        result.loc[pd.isna(result['distance_metres']),'distance_metres']=0.0
    else:
        result['distance_metres']=0.0
        
    # Post-process2
    if result.shape[0]==points_gdf.shape[0]:
        # Sort by original index so column has the correct order when output
        result.sort_index(inplace=True)
        polygon_id_column = result['polygon_id']
        distance_column = result['distance_metres']
    else:
        # Does a point belong to more than one polygon?
        # Temporarily turn nan into empty strings to make sure all rows are strings
        result['polygon_id'].replace(np.nan, '', regex=True, inplace=True)
        result.sort_values(by='polygon_id',inplace=True)
        result_group = result.groupby(level=0)
        if handle_multiple_matches == 'join':
            polygon_id_column=result_group['polygon_id'].apply(', '.join)
        elif handle_multiple_matches == 'random_select':
            polygon_id_column=result_group['polygon_id'].apply(lambda x: x.sample(1)).reset_index(drop=True)
        else:
            raise RuntimeError('points_in_polygons: handle_multiple_matches not recognized')
            
        polygon_id_column.replace('',np.nan, regex=True, inplace=True)
        polygon_id_column.sort_index(inplace=True)   
        # Do we also have different distances?
        distance_column=result_group['distance_metres'].apply(min)

    # Output columns
    polygon_id = polygon_id_column.astype(polygon_id_dtype)
    distance_metres = distance_column
    
    # If there are no matches, Spotfire needs to be told the data type
    # explicitly via metadata.
    # Restore data type of polygon id in case no point matches a polygon
    if polygon_id_dtype == pd.Int64Dtype():
        polygon_id.attrs['spotfire_type'] = "LongInteger"
    elif polygon_id_dtype == pd.Int32Dtype():
        polygon_id.attrs['spotfire_type'] = "Integer"
    else:
        polygon_id.attrs['spotfire_type'] = "String"

    return (polygon_id,distance_metres)

###################################################################
# MAIN ------------------------------------------------------------
if __name__ == '__main__':
    print('Executed spatial joins')