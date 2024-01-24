import glob as glob
import json
import multiprocessing

import click
import duckdb
import geopandas as gpd
import numpy as np
import pandas as pd
from loguru import logger
from rasterio import features, warp, windows
from shapely import box
from shapely.geometry import shape
import multiprocesspandas

from geomlcv.utils.download_data.planetary_computer import calculate_ndwi

ndwi_range_low: float = 0.01
ndwi_range_high: float = 1


def get_ndwi(row):
    try:
        out_ndwi, aoi_window_wh = calculate_ndwi(
            aoi=row.geometry,
            ndwi_range_low=ndwi_range_low,
            ndwi_range_high=ndwi_range_high,
        )
        return {"ndwi": json.dumps(out_ndwi.tolist()), "aoi_window_wh": aoi_window_wh}
    except Exception as e:
        print("exception", e)
        return {"ndwi": -1, "aoi_window_wh": -1}


def parallel_function(chunk, i):
    chunk["ndwi_vars"] = chunk.apply_parallel(
        get_ndwi, num_processes=multiprocessing.cpu_count()
    )
    chunk["aoi_bounds"] = chunk.geometry.apply(
        lambda x: features.bounds(x.__geo_interface__)
    )
    chunk = pd.concat([chunk, chunk["ndwi_vars"].apply(pd.Series)], axis=1).drop(
        columns=["ndwi_vars"]
    )
    chunk.to_csv(
        f"/home/ec2-user/geomlcv/docs/notebooks/.data/out_ndwi/ndwi_mask_{i}.csv"
    )


@click.command()
@click.option("--skip", multiple=True)
def run(skip):
    logger.debug("Start...")

    con = duckdb.connect()

    con.sql("INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;")

    # 1. Tang
    df_tang = con.sql(
        "SELECT *, 'tang' AS dataset FROM read_parquet('s3://geoml-aquarry/output/postprocess/jan2024/tang_predictions_boxes_geo.parquet')"
    ).df()
    df_tang = gpd.GeoDataFrame(
        df_tang, geometry=df_tang.box_coords.apply(lambda x: box(*x))
    )
    # df_tang.drop('box_coords', inplace=True, axis='columns')
    # 2. Verified pitlakes
    df_vp = con.sql(
        """SELECT *, 1.0 AS score, 2.0 AS label, 'vp' AS dataset  FROM 's3://geoml-aquarry/output/postprocess/jan2024/verified_pitlakes_bbox.parquet'"""
    ).df()
    df_vp["geometry"] = df_vp["geometry_geojson"].apply(lambda x: shape(json.loads(x)))
    df_vp.drop("geometry_geojson", inplace=True, axis="columns")
    # 3. Concat
    gdf_pitlakes = pd.concat([df_tang, df_vp], ignore_index=True)
    logger.debug("Loaded datasets.")
    # 4. Query sentinel via Planetary Computer
    # 4.1 Break up df into chunks
    n = 1_000
    n_chunks = np.ceil(len(gdf_pitlakes) / n)
    # 4.2 Create a grouping key for each chunk
    gdf_pitlakes["chunk"] = np.arange(len(gdf_pitlakes)) // n

    # Run for each chunk
    for i, chunk in gdf_pitlakes.groupby("chunk"):
        logger.info(f"Runing chunk {i}...")
        if i in [int(each) for each in skip]:  # Skip chunks
            continue
        parallel_function(chunk, i)

    logger.debug("End.")


if __name__ == "__main__":
    run()
