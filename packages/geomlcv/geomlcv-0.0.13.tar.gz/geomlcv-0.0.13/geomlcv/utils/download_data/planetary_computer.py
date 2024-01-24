import json
from functools import lru_cache
from typing import Dict, Union

import numpy as np
import planetary_computer
import rasterio
from PIL import Image
from pystac.extensions.eo import EOExtension as eo
from pystac_client import Client
from rasterio import features, warp, windows

api = Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)


def _process_aoi(aoi: Union[str, Dict]):
    if isinstance(aoi, str):
        return json.loads(aoi)
    else:
        return aoi


@lru_cache
def get_raster_href_item(
    aoi: Union[str, Dict], time_of_interest="2019-01-01/2023-12-31"
):
    aoi = _process_aoi(aoi)
    search = api.search(
        collections=["sentinel-2-l2a"],
        intersects=aoi,
        datetime=time_of_interest,
        query={"eo:cloud_cover": {"lt": 10}},
    )

    # Check how many items were returned
    items = search.item_collection()

    if len(items) >= 1:
        return min(items, key=lambda item: eo.ext(item).cloud_cover)
    else:
        raise ("Failed to find PC assets for the aoi for the specified date range.")


def get_asset_href(
    aoi: Union[str, Dict], time_of_interest="2019-01-01/2023-12-31", asset="visual"
):
    aoi = _process_aoi(aoi)
    return (
        get_raster_href_item(aoi=aoi, time_of_interest=time_of_interest)
        .assets[asset]
        .href
    )


def get_img_from_href(aoi: Union[str, Dict], asset_href: str):
    aoi = _process_aoi(aoi)

    # Render the AOI from the previous image
    with rasterio.open(asset_href) as ds:
        aoi_bounds = features.bounds(aoi)
        warped_aoi_bounds = warp.transform_bounds("epsg:4326", ds.crs, *aoi_bounds)
        aoi_window = windows.from_bounds(transform=ds.transform, *warped_aoi_bounds)
        band_data = ds.read(window=aoi_window)

    return Image.fromarray(np.transpose(band_data, axes=[1, 2, 0]))


def calculate_ndwi(
    aoi: Union[str, Dict],
    green_href: str = None,
    nir_href: str = None,
    ndwi_range_low: float = 0.05,
    ndwi_range_high: float = 1,
):
    aoi = _process_aoi(aoi)
    aoi_bounds = features.bounds(aoi)

    # Get or create hrefs
    green_href = green_href or get_asset_href(aoi, asset="B03")
    nir_href = nir_href or get_asset_href(aoi, asset="B08")

    bands_href = [green_href, nir_href]

    # Create an empty dictionary to store band data
    band_data = {}

    for band_name, band_href in zip(["green", "nir"], bands_href):
        with rasterio.open(band_href) as ds:
            aoi_bounds = features.bounds(aoi)
            warped_aoi_bounds = warp.transform_bounds("epsg:4326", ds.crs, *aoi_bounds)
            aoi_window = windows.from_bounds(transform=ds.transform, *warped_aoi_bounds)
            band_data[band_name] = np.transpose(ds.read(window=aoi_window), (1, 2, 0))

    # Get separate green and nir data arrays
    green_data = band_data["green"]
    nir_data = band_data["nir"]

    # Calculate NDWI
    ndwi = (green_data - nir_data) / (green_data + nir_data)
    return ndwi, (aoi_window.width, aoi_window.height)

    # # Normalize NDWI values to the range [0, 1] for visualization
    # ndwi_normalized = (ndwi - np.min(ndwi)) / (np.max(ndwi) - np.min(ndwi))

    # Mask NDWI values outside the water range
    #
    # The visible green wavelengths maximize the typical reflectance of the water surface.
    # The near-infrared wavelengths maximize the high reflectance of terrestrial vegetation and soil features,
    # while minimizing the low reflectance of water features.
    # The result of the NDWI equation is positive values for water features and negative ones
    # (or zero) for soil and terrestrial vegetation.
    # https://eos.com/make-an-analysis/ndwi/
    masked_ndwi = np.ma.masked_where(
        (ndwi < ndwi_range_low) | (ndwi > ndwi_range_high), ndwi
    )

    # Count the number of water pixels/valid (non-masked) values in masked_ndwi
    # water_pixels = np.count_nonzero(~masked_ndwi.mask)

    return masked_ndwi
