
# --- LIBRARIES ---------------------------------------------------------------
import pandas as pd
import numpy as np
import shapely
import geopandas as gpd
import geopy
from geopy.distance import geodesic
from pyproj import Geod
import math

# spotfire_dsml libraries
from spotfire_dsml.geo_analytics import crs_utilities, io_utilities

###############################################################################
# Shape Utilities:
#
# Calculations over existing geometries or generation of new geometries.
#    
# Use geopandas, shapely, geopy, pyproj for transformations and other calculations
###############################################################################

# --- INTERNAL FUNCTIONS ------------------------------------------------------
    
def _calculate_bounds(gdf, xmin_name='XMin',xmax_name='XMax',
                    ymin_name='YMin',ymax_name='YMax'):
    '''
    Internal function to calculate the bounds for each row of the geometry 
    column of a geo dataframe.
    The bounds are the minimum and maximum coordinates in two dimensions.
    The CRS can be any valid coordinate reference system. 
    The convention is that X represents the Easting or Longitude,
    and that the Y represents the Northing or Latitude.

    Parameters
    ----------
    gdf : geopandas GeoDataFrane
        The input geo dataframe.
    xmin_name : str, optional
        Name of the column to contain the minimum X. The default is 'XMin'.
    xmax_name : str, optional
        Name of the column to contain the maximum X. The default is 'XMax'.
    ymin_name : str, optional
        Name of the column to contain the minimum Y. The default is 'YMin'.
    ymax_name : str, optional
        Name of the column to contain the maximum Y. The default is 'YMax'.

    Returns
    -------
    shape_bounds : pandas DataFrame
        Data frame containing the bounds as 4 columns.

    '''
    shape_bounds=  gdf.bounds
    shape_bounds = shape_bounds[['minx','maxx','miny','maxy']]
    shape_bounds.columns=[xmin_name,xmax_name,ymin_name,ymax_name]
    return shape_bounds


def _calculate_centroid(crs,gdf, 
                        centroid_style = 'representative', 
                        xc_name='XCenter',yc_name='YCenter'):
    '''
    Internal function to calculate the centroid for each row of the 
    geometry column of a geo dataframe.
    If centroid_style is 'representative', the centroid will be evaluated by geopandas as
    "a (cheaply computed) point that is guaranteed to be within the geometry."
    Otherwise, the geometry centroid will be calculated.
    If the CRS of the input data frame is not projected, 
    and centroid_style = 'projected', it will be re-projected to EPSG:6933, 
    then projected back to the original CRS.
    In most cases, this does not make much difference in the numeric results.
    The convention is that X represents the Easting or Longitude,
    and that the Y represents the Northing or Latitude.
    
    The centroid is calculated using geopandas.
    

    Parameters
    ----------
    crs : int, str, pyproj CRS
        The current coordinate system of the data frame.
    gdf : geopandas GeoDataFrame
        The input geo dataframe.
    centroid_style: str, optional
        if 'representative'  return a representative point that is guaranteed to lie
        within the perimeter;
        if 'original' calculate centroid using the current CRS, regardless of whether it is 
        geographic or projected;
        if 'projected' calculate centroid using a projected CRS, set to EPSG:6933.
        The default is 'representative'..

    xc_name : str, optional
        Name of the column to contain the centroid X. The default is 'XCenter'.
    yc_name : str, optional
        Name of the column to contain the centroid Y. The default is 'YCenter'.

    Returns
    -------
    shape_centroid : pandas DataFrame
        Data frame containing the centroid as 2 columns.

    '''    
    import warnings
    
    if centroid_style == 'representative':
        shape_centroid_points = gdf.representative_point()
        
    else:
        if centroid_style == 'projected' and not crs_utilities.crs_is_projected(crs):
            try:
            # Temporarily project (to 6933) to calculate centroid
                gdf_proj = gdf.to_crs(crs_utilities.get_crs(6933))
                shape_centroid_points = gdf_proj.centroid
                shape_centroid_points = shape_centroid_points.to_crs(crs)
            except:
                raise RuntimeError('_calculate_centroid: could not calculate.')
                
        else:
            # This will generate a UserWarning if the coordinates are geographic
            warnings.filterwarnings('ignore')
            shape_centroid_points = gdf.centroid
            warnings.resetwarnings()
        
    shape_centroid=pd.DataFrame({xc_name:[],yc_name:[]})
    shape_centroid[xc_name] = shape_centroid_points.map(lambda p: p.x)
    shape_centroid[yc_name] = shape_centroid_points.map(lambda p: p.y)   
    
    return shape_centroid


def _build_envelope_from_geometry(geometry, crs, projected_crs):
    '''
    NOT FOR RELEASE YET

    Parameters
    ----------
    geometry : TYPE
        DESCRIPTION.
    crs : TYPE
        DESCRIPTION.
    projected_crs : TYPE
        DESCRIPTION.

    Returns
    -------
    result : TYPE
        DESCRIPTION.

    '''
    # Build a new geo dataframe and project it
    geo_df = gpd.GeoDataFrame({'geometry':geometry}, crs=crs)
    geo_df= geo_df.to_crs(projected_crs)
    # Envelope, then project back
    result = gpd.GeoDataFrame(geometry=geo_df.envelope).to_crs(crs)
    
    return result


def _build_circle_buffer(seed_lat,seed_lon, radius, angle):
    '''
    Internal function.
    For a pair of geographic latitude, longitude coordinates, given
    a radius and a set of angles, build a circle geometry around the point.
    If the circle overlaps with the discontinuity at (-180,180), split it in two
    and return a multipolygon.
    Use Geopy to generate points that are robust to latitude.

    Parameters
    ----------
    seed_lat : float
        The latitude of the starting point.
    seed_lon : float
        The longitude of the starting point.
    radius : geopy distance
        The desired circle radius as a geopy distance object.
    angle_vector : numpy array
        The angles for creating the points to map the circle.

    Returns
    -------
    Shapely Polygon
        The circle buffer around the given point.

    '''
    center_point = geopy.Point((seed_lat,seed_lon))

    # Generate points on circumference    
    points = [radius.destination(point=center_point, bearing=aa) for aa in angle]
    
    lat_vector = [p.latitude for p in points]
    lon_vector = [p.longitude for p in points]
    
    # Reset vectors that fall beyond -180,180 or -90,90
    lon_vector = [x % (-np.sign(x)*180) if abs(x)>180 else x for x in lon_vector]
    lat_vector = [x % (-np.sign(x)*90)  if abs(x)>90 else x for x in lat_vector]
    
    # Detect if there is a discontinuity in longitude
    delta_longitude = [abs(t - s) for s, t in zip(lon_vector, lon_vector[1:])]
    # Expecting it to be around 359 actually.. so 100 should be safe
    if (max(delta_longitude))>100:
        # Create circles for each side of the (-180,180) line
        circles = []
        circle = [(i,j) for i,j in zip(lon_vector, lat_vector) if i>=0 ]
        if len(circle)>0: circles.append(circle)        
        circle = [(i,j) for i,j in zip(lon_vector, lat_vector) if i<=0 ]
        if len(circle)>0: circles.append(circle)        
        polygons = [shapely.Polygon(cc) for cc in circles]
        return shapely.MultiPolygon(polygons)
    else:
        return shapely.Polygon(zip(lon_vector, lat_vector))


def _build_bounding_rectangle(seed_lat,seed_lon,dist_diag,angle, dist_hei):
    '''
    Internal function. 
    For a pair of geographic latitude, longitude coordinates, given
    a diagonal distance and the diagonal angle, build a 
    rectangular bounding box around the point.
    Use Geopy to generate points that are robust to latitude.
    If the box overlaps with the discontinuity at (-180,180), split it in two
    and return a multipolygon.
    

    Parameters
    ----------
    seed_lat : float
        The latitude of the starting point.
    seed_lon : float
        The longitude of the starting point.
    dist_diag : geopy distance
        The diagonal distance from the starting point to the rectangle corner,
        as a geopy distance object.
    angle : float
        The angle between the diagonal and the horizontal width.
    dist_diag : geopy distance
        The half height distance from the starting point to the rectangle top.
        Used when splitting the bounding box across the (-180,180) line.

    Returns
    -------
    Shapely Polygon
        The rectangular bounding box around the given point.

    '''
    center_point = geopy.Point((seed_lat,seed_lon))
    p1 = dist_diag.destination(point=center_point, bearing=angle)
    p2 = dist_diag.destination(point=center_point, bearing=180-angle)
    p3 = dist_diag.destination(point=center_point, bearing=-(180-angle))
    p4 = dist_diag.destination(point=center_point, bearing=-angle)

    lon_vector = [p.longitude for p in [p1,p2,p3,p4]]
    lat_vector = [p.latitude for p in [p1,p2,p3,p4]]
    
    # Detect if there is a discontinuity in longitude
    delta_longitude = [abs(t - s) for s, t in zip(lon_vector, lon_vector[1:])]
    # Expecting it to be around 359 actually.. so 100 should be safe
    if (max(delta_longitude))>100:
        boxes = []
        # Create boxes for each side of the (-180,180) line
        # The box would be a line if we simply cut it in two, as we would only
        # be left with two points.
        # We need to add two points each side of the
        # discontinuity line to close it 
        box = [(i,j) for i,j in zip(lon_vector, lat_vector) if i>=0 ]

        new_seed = geopy.Point((seed_lat,180.0))
        p5 = dist_hei.destination(point=new_seed, bearing=0)
        p6 = dist_hei.destination(point=new_seed, bearing=180)
        lon_add = [p.longitude for p in [p5,p6]]
        lat_add = [p.latitude for p in [p5,p6]]
        add_box = [(i,j) for i,j in zip(lon_add,lat_add)  ]
        if len(box)>0: boxes.append(box+add_box)    
        
        box = [(i,j) for i,j in zip(lon_vector, lat_vector) if i<=0 ]

        new_seed = geopy.Point((seed_lat,-180.0))
        p5 = dist_hei.destination(point=new_seed, bearing=180)
        p6 = dist_hei.destination(point=new_seed, bearing=0)
        lon_add = [p.longitude for p in [p5,p6]]
        lat_add = [p.latitude for p in [p5,p6]]
        add_box = [(i,j) for i,j in zip(lon_add,lat_add)  ]               
        if len(box)>0: boxes.append(box+add_box)  
        
        polygons = [shapely.Polygon(cc) for cc in boxes]
        return shapely.MultiPolygon(polygons)
    else:
        return shapely.Polygon(zip(lon_vector, lat_vector))
    

# --- FOR FUTURE IMPLEMENTATION -----------------------------------------------

def __create_envelope_from_coordinates(a,b=None,source_crs='EPSG:4326'):
    '''
    NOT FULLY IMPLEMENTED YET. DO NOT USE.
    '''
    source_crs = crs_utilities.get_crs(source_crs)
    projected_crs = crs_utilities.get_crs('web mercator')
    points_gdf = create_points_from_coordinates(source_crs, a,b)
    geometry = points_gdf.unary_union
    return _build_envelope_from_geometry(geometry, source_crs, projected_crs)


def __create_envelope(geometry,source_crs='EPSG:4326'):
    '''
    NOT FULLY IMPLEMENTED YET. DO NOT USE.
    
    From an input geometry, return its envelope as a data frame.
    The envelope of a geometry is the bounding rectangle. That is, the point 
    or smallest rectangular polygon (with sides parallel to the 
    coordinate axes) that contains the geometry.
    
    '''
    source_crs = crs_utilities.get_crs(source_crs)
    projected_crs = crs_utilities.get_crs('web mercator')
    
    # Translate geometry from wkb if it is not already a shapely geometry
    if not isinstance(list(geometry)[0],shapely.geometry.base.BaseGeometry):
        geometry = io_utilities._geo_series_from_wkb(geometry,crs=source_crs)
            
    return _build_envelope_from_geometry(geometry, source_crs, projected_crs)


# NOTES FOR FUTURE DEVELOPMENT
#unary_union: returns a geometry containing the union of all geometries in the GeoSeries.
#does it need a projection?
#circle = circle_buffer['geometry'][0]
    
#lat_max = max(latlon['y'])
#lat_min = min(latlon['y'])
#divider=shapely.Linestr([(-180,-90),(-180,90)])
#line_gdf = gpd.GeoDataFrame(geometry=[divider])
#lines = line_gdf.loc[(line_gdf.geometry.intersects(circle)) & (~line_gdf.geometry.touches(circle))]

#split_polys = split(circle, line_gdf.geometry.iloc[0])
#circle1=split_polys.geoms[0]
#split_polys.geoms[1]


def __create_convex_hull(a,b=None,source_crs='EPSG:4326',projected_crs='utm'):
    '''
    NOT FULLY IMPLEMENTED YET. DO NOT USE.

    The convex hull of a set of points X in Euclidean space 
    is the smallest convex set containing X.
    '''

    source_crs = crs_utilities.get_crs(source_crs)
    # Create Points from input coordinates
    geo_points_df = create_points_from_coordinates(source_crs, a, b)

    # UTM is the best for small areas, as it preserves distances well
    if isinstance(projected_crs,str) and projected_crs.lower().strip() == 'utm':
        projected_crs = crs_utilities.calculate_median_utm(a,b)
    projected_crs = crs_utilities.get_crs(projected_crs)
    
    if not crs_utilities.crs_is_projected(projected_crs):
        raise RuntimeError('add_circle_buffer: The crs ',projected_crs,' should be projected.')
    
    # Project geometry to calculate convex hull
    geom=geo_points_df['geometry'].to_crs(projected_crs)
    # Calculate circle buffer and project back
    #hull=gpd.GeoDataFrame(geometry=geom.unary_union.convex_hull,crs=projected_crs)
    #result = hull.to_crs(source_crs) 
    
    result = gpd.GeoDataFrame(geometry=[geo_points_df.unary_union.convex_hull], crs=source_crs)

    return result


# --- EXTERNAL FUNCTIONS ------------------------------------------------------


def create_points_from_coordinates(source_crs,a,b=None,geometry_column_name='geometry'):
    '''
    Create a geo data frame of Point geometries from a set of coordinates.
    The coordinates can come as two separate columns of data (a and b) 
    or as a single tuple (a).
    If the source crs is projected, the column names assigned to the coordinates
    will be x and y, otherwise they will be lat and lon.
    
    Parameters
    ----------
    source_crs : int, str, pyproj CRS
        The CRS of the input coordinates.
    a : tuple or array-like
        The coordinates (if a tuple) or the first coordinate (if an array).
    b : array-like, optional
        The second coordinate (if a is a vector) or empty if a is a tuple. 
        The default is None.
    geometry_column_name : str, optional
        The name of the column to contain the generated geometry. 
        The default is 'geometry'.
    
    Returns
    -------
    geo_points_df : geopandas data frame
        A geo data frame containing the input coordinates expressed 
        as spatial Points.

    '''

    source_crs = crs_utilities.get_crs(source_crs)
    source_is_projected = crs_utilities.crs_is_projected(source_crs)
    if source_is_projected:
        col_names=['x','y']
    else:
        col_names=['lat','lon']
        
    coords_df = io_utilities._input_coordinates(col_names,a,b)

    # Make sure the order is as expected
    if source_is_projected: #projected coordinates are always x then y
        geo_points_df = gpd.GeoDataFrame(coords_df, 
                                        geometry=gpd.points_from_xy(coords_df.iloc[:,0], 
                                                                    coords_df.iloc[:,1]), crs=source_crs)
    else: #reverse order as Points are expressed as lon and lat
        geo_points_df = gpd.GeoDataFrame(coords_df, 
                                        geometry=gpd.points_from_xy(coords_df.iloc[:,1], 
                                                                    coords_df.iloc[:,0]), crs=source_crs)
        
    if geometry_column_name != 'geometry':
        geo_points_df.rename_geometry(geometry_column_name,inplace=True)    
    return geo_points_df


def calculate_area(gdf, unit='km', crs = None, method='equal area projection'):
    '''
    Calculate the area of a vector of polygon geometries.
    Either use the geodesic method implemented in the 
    geometry_area_perimeter function of pyproj, or 
    temporarily project to EPSG:6933 and calculate area on a plane.
    
    If the input dataset is a geopandas GeoSeries, the input crs must be
    specified. If the input dataset is a geopandas GeoDataFrame, the crs
    will be taken from the data frame if present, and the input CRS ignored.
    
    Parameters
    ----------
    crs : int, str, pyproj CRS, optional
        The current coordinate system of the data frame.
        The default is None. If not specified, it will be extracted
        from the input gdf, if it is a geo data frame.
    gdf : geopandas GeoDataFrame or GeoSeries, or pandas Series or list.
        The input geometry.
        If specified as a pandas Series or a list, assume it is in WKB format.
        If specified as a geopandas object, the CRS is extracted and compared to
        the input crs.
    method: str, optional
        If 'equal area projection' then the geometry will first be projected
        on to an equal area projection that is valid world-wide (EPSG:6933).
        If 'geodesic' then the area will be calculated using the 
        geometry_area_perimeter function of pyproj. If the input CRS is not
        geographic, it will be temporarily projected to gps (EPSG:4326)
        The geodesic method is more accurate, but typically slower.

    Raises
    ------
    RuntimeError
        If the input data is a geopandas GeoDataFrame and its CRS does not
        correspond to the CRS specified in input, or if the input data is a
        geopandas GeoSeries and the input crs was not specified.
        
    Returns
    -------
    shape_area : pandas Series
        Series containing the area of each row in the input data frame.

    '''    
    
    if crs is not None:
        crs = crs_utilities.get_crs(crs)
    
    # Areas are originally calculated in square metres in both methods
    factor = io_utilities._convert_unit('metre', unit)

    # It could be a geo series or WKB series or a data frame or a geo data frame
    if isinstance(gdf, pd.Series):
        geometry_type='series'
    elif isinstance(gdf, gpd.GeoDataFrame):
        geometry_type='data_frame'
    else:
        geometry_type='list'
    
    if geometry_type=='series' or geometry_type=='list':
        if isinstance(gdf,gpd.GeoSeries):
            geometry = gdf.copy()
            geometry_crs = geometry.crs
        else:
            geometry = io_utilities._geo_series_from_wkb(gdf,crs=None)
            geometry_crs = None
        geo_df = gpd.GeoDataFrame(geometry=geometry,crs=geometry_crs)
    elif geometry_type == 'data_frame':
        geometry = gdf.geometry
        geometry_crs =gdf.crs  
        geo_df = gdf.copy()

    if geometry_crs is not None and crs is not None and geometry_crs != crs:
        raise RuntimeError("calculate_area: The input geometry's CRS is not the same as the input crs")    
    elif geometry_crs is not None and crs is None:
        crs = geometry_crs
        
    if crs is None:
        raise RuntimeError("calculate_area: No CRS could be specified")    
        
    # Check whether CRS is geographic
    if crs_utilities._is_lat_lon(crs) and method == 'geodesic':
        geod = Geod(ellps="WGS84")
        shape_area = pd.Series([abs(geod.geometry_area_perimeter(gg)[0]) for gg in geometry])
    # If CRS not geographic, and method is geodesic, project to 4326 first
    elif ~crs_utilities._is_lat_lon(crs) and method == 'geodesic':
        # Temporarily project (to gps EPSG:4326) to calculate area
        geo_df_gps = geo_df.to_crs(crs_utilities.get_crs(4326))
        geod = Geod(ellps="WGS84")
        shape_area = pd.Series([abs(geod.geometry_area_perimeter(gg)[0]) for gg in geo_df_gps.geometry])
    else: #method is equal area projection
        # Temporarily project (to EPSG:6933) to calculate area
        # https://epsg.io/6933
        geo_df_proj = geo_df.to_crs(crs_utilities.get_crs(6933))
        shape_area= geo_df_proj.area
    
    return shape_area*factor*factor

def create_circle_buffer(radius,unit,a,b=None, circle_id=None, source_crs='EPSG:4326'):
    '''
    Create a circle buffer geometry with a specified radius around a set of point
    coordinates. Only implemented for geographic latitude and longitude.
    If the circle has a potential discontinuity at (-180,180), split it in two 
    circle portions.
    The coordinates are expected as latitude, longitude.

    Parameters
    ----------
    radius : float
        The desired radius around the points.
    unit : str
        The unit for the radius.
        Recognized units are:
        'm','metre','meter','meters'
        'km','kilometer','kilometers','kilometre','kilometres'
        'mile','miles'.
    a : tuple or array-like
        The coordinates (if a tuple) or the first coordinate (if an array).
    b : array-like, optional
        The second coordinate (if a is a vector) or empty if a is a tuple.
        The default is None.
    circle_id: list, pandas Series, optional
        The desired id column for the generated circle. It will be named
        "circle_id".
        The default is None (an id column will not be generated)
    source_crs : int, str, pyproj CRS, optional
        The CRS of the points. The default is 'EPSG:4326'.

    Raises
    ------
    RuntimeError
        If the CRS is not standard EPSG:4326.

    Returns
    -------
    circle_buffer : geopandas GeoDataFrame
        Geo data frame with geometry corresponding to the circle buffer 
        for each point.

    '''

    source_crs = crs_utilities.get_crs(source_crs)

    if not crs_utilities._is_lat_lon(source_crs):
        raise RuntimeError('create_circle_buffer: The source crs ',crs_utilities.get_crs_code(source_crs),
                        ' is not EPSG:4326. Please provide standard latitude and longitude coordinates.')

    # We use metre to construct the circle
    radius *= io_utilities._convert_unit(unit,'metre')
    # Generate all angles: 90 should suffice to draw a circle 
    n_points = 90
    angle_vector = np.linspace(0,360,n_points)         
    # General geopy distance object
    radius = geodesic(meters =radius) 

    # Initialize with the input coordinates
    circle_buffer = io_utilities._input_coordinates(['lat','lon'], a,b)
    
    # List of circle buffers for each initial point
    circle_buffer= circle_buffer.apply(lambda x:  _build_circle_buffer(x.lat, 
                                                                    x.lon, 
                                                                    radius, 
                                                                    angle_vector), axis=1)
    circle_buffer.name = 'geometry'
    circle_buffer = gpd.GeoDataFrame(circle_buffer,geometry='geometry',crs=source_crs)
    
    # Assign an id column if desired
    if isinstance(circle_id,pd.Series) or isinstance(circle_id,list):
        circle_buffer['circle_id']=io_utilities._check_id(circle_id, circle_buffer.shape[0])

    # Split any multi-polygons we generated into separate rows, with a polygon for each row   
    circle_buffer = circle_buffer.explode(ignore_index=True)
    
    return circle_buffer

def create_bounding_box(width,height,unit,a,b=None,box_id=None,source_crs='EPSG:4326'):
    '''
    Build a rectangular bounding box around a set of point
    coordinates. Only implemented for geographic latitude and longitude.

    Parameters
    ----------
    width : float
        The desired width of the box.
    height : float
        The desired height of the box.
    unit : TYPE
        The unit for width and height.
        Recognized units are:
        'm','metre','meter','meters'
        'km','kilometer','kilometers','kilometre','kilometres'
        'mile','miles'.
    a : tuple or array-like
        The coordinates (if a tuple) or the first coordinate (if an array).
    b : array-like, optional
        The second coordinate (if a is a vector) or empty if a is a tuple.
        The default is None.
    box_id: list, pandas Series, optional
        The desired id column for the generated box. It will be named
        "box_id".
        The default is None (an id column will not be generated)
    source_crs : int, str, pyproj CRS, optional
        The CRS of the points. The default is 'EPSG:4326'.

    Raises
    ------
    RuntimeError
        If the CRS is not standard EPSG:4326.

    Returns
    -------
    bounding_box : geopandas GeoDataFrame
        Geo data frame with geometry corresponding to the rectangular 
        bounding box for each point.

    '''

    source_crs = crs_utilities.get_crs(source_crs)

    if not crs_utilities._is_lat_lon(source_crs):
        raise RuntimeError('create_bounding_box: The crs ',crs_utilities.get_crs_code(source_crs),
                        ' is not EPSG:4326. Please provide standard latitude and longitude coordinates.')

    # We use metre to construct the rectangle
    width *= io_utilities._convert_unit(unit,'metre')
    height *= io_utilities._convert_unit(unit,'metre')
    diag = np.sqrt((height/2)**2 + (width/2)**2)
    
    
    if width==height:
        angle = 45.0
    else:
        angle = math.acos(0.5*height/diag)*180/np.pi
        
    # General geopy distance objects
    dist_diag = geodesic(meters =diag) 
    dist_hei = geodesic(meters =height/2) 
    
    # Initialize with the input coordinates
    bounding_box = io_utilities._input_coordinates(['lat','lon'], a,b)
    
    # List of bounding boxes for each initial point
    bounding_box = bounding_box.apply(lambda x: _build_bounding_rectangle(x.lat, 
                                                                        x.lon, 
                                                                        dist_diag,angle,dist_hei), axis=1)
    bounding_box.name = 'geometry'    
    bounding_box = gpd.GeoDataFrame(bounding_box,geometry='geometry',crs=source_crs)

    # Assign an id column if desired
    if isinstance(box_id,pd.Series) or isinstance(box_id,list):
        bounding_box['box_id']=io_utilities._check_id(box_id, bounding_box.shape[0])

    # Split any multi-polygons we generated into separate rows, with a polygon for each row
    bounding_box = bounding_box.explode(ignore_index=True)
    
    return bounding_box

###################################################################
# MAIN ------------------------------------------------------------
if __name__ == '__main__':
    print('Executed shape_utilities')