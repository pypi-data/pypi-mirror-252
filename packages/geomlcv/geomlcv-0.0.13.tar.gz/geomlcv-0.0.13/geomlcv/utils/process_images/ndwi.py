import matplotlib.pyplot as plt
import numpy as np
import pyproj
from affine import Affine
from shapely.geometry import Point, Polygon
from shapely.ops import transform

# TODO: cleanup this reference
# bbox_coords = eval(dfout.iloc[0].aoi_bounds)
# raster_width, raster_height = eval(dfout.iloc[0].aoi_window_wh)


def bounds(ndwi, bbox_coords, aoi_window_wh, range_low=0, range_high=1):
    masked_ndwi = np.ma.masked_where((ndwi < range_low) | (ndwi > range_high), ndwi)

    water_pixels = np.count_nonzero(~masked_ndwi.mask)

    ndwi_channel = ndwi[:, :, 0]

    # Create a contour plot
    contour_object = plt.contour(
        ndwi_channel, levels=[range_low, range_high], colors="r"
    )

    plt.close()  # Uncomment this line if you don't want to see the contour plot

    # Extract contour values
    contour_vertices_list = []
    contour_areas = []
    for collection in contour_object.collections:
        paths = collection.get_paths()
        for path in paths:
            vertices = path.vertices
            contour_vertices_list.append(vertices)
            # Calculate the area of the contour using the Shoelace formula
            area = np.abs(
                0.5
                * np.sum(
                    vertices[:, 0] * np.roll(vertices[:, 1], 1)
                    - vertices[:, 1] * np.roll(vertices[:, 0], 1)
                )
            )
            contour_areas.append(area)

    # Find the index of the largest contour
    largest_contour_index = np.argmax(contour_areas)

    # Get the vertices of the largest contour
    largest_contour_vertices = contour_vertices_list[largest_contour_index]

    # Dimensions of the raster
    raster_width, raster_height = aoi_window_wh

    # Calculate scaling factors
    x_scale = (bbox_coords[2] - bbox_coords[0]) / raster_width
    y_scale = (bbox_coords[3] - bbox_coords[1]) / raster_height

    # Create an affine transformation (Assuming no rotation and top-left origin)
    affine_transform = Affine.translation(
        bbox_coords[0], bbox_coords[3]
    ) * Affine.scale(x_scale, -y_scale)

    # Apply affine transformation to each point of the pit lake contour
    georeferenced_points = []

    for contour_point in largest_contour_vertices:
        point = Point(*affine_transform * (contour_point[0], contour_point[1]))
        georeferenced_points.append(point)

    # Transform the contour points into a polygon
    polygon_coords = Polygon(georeferenced_points)

    ###################################### AREA ######################################
    # Choose the appropiate UTM zone based on the centroid's longitude
    utm_zone = int((polygon_coords.centroid.x + 180) / 6) + 1
    utm_crs = f"+proj=utm + zone={utm_zone} + ellps=WGS84"
    projected_polygon = transform(
        pyproj.Transformer.from_crs("EPSG:4326", utm_crs, always_xy=True).transform,
        polygon_coords,
    )
    return projected_polygon


def area(polygon_coords):
    ###################################### AREA ######################################
    # Choose the appropiate UTM zone based on the centroid's longitude
    utm_zone = int((polygon_coords.centroid.x + 180) / 6) + 1
    utm_crs = f"+proj=utm + zone={utm_zone} + ellps=WGS84"
    projected_polygon = transform(
        pyproj.Transformer.from_crs("EPSG:4326", utm_crs, always_xy=True).transform,
        polygon_coords,
    )

    return projected_polygon.area


def cone_volume(area):
    import math

    return np.round(area ** (3 / 2) / (20 * math.sqrt(math.pi)) / 1_000, 2)
