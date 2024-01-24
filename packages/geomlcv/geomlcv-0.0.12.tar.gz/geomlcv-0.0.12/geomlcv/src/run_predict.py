import glob as glob
import multiprocessing
import sys

import click
import duckdb
from loguru import logger

sys.path.insert(0, "/home/ec2-user/geomlcv/")  # noqa
from geomlcv.utils.download_data.aws import (get_s3_image,
                                             list_s3_objects_in_directory,
                                             structure_s3_key,
                                             write_to_parquet)
from geomlcv.utils.download_data.multiprocess import run_parallel
from geomlcv.utils.nn import run_inference

BUCKET_PATH = "s3://geoml-aquarry/output/gms/16dec2023/tang/"
S3_BASE = "geoml-aquarry/output/predict/23dec2023/"
CONFIDENCE_THRESHOLD = 0.5


def run_inference_multiprocessing(row_data):
    objectid, model_name, img_transform = row_data[0], row_data[1], row_data[2]
    filename = f"tang_{objectid}"
    # Fetch source image from S3, and only continue if it exists
    img = get_s3_image(f"tang_{objectid}")

    out = run_inference(
        img,
        model_name=model_name,
        img_transform=img_transform,
        confidence_threshold=CONFIDENCE_THRESHOLD,
    )

    path_output_file = structure_s3_key(
        model_name=model_name,
        dataset_name="tang",
        img_transform=img_transform,
        filename=filename,
        s3base=S3_BASE,
    )
    write_to_parquet(out, objectid=objectid, path_output_file=path_output_file)


@click.command()
@click.option("--offset", default=1, help="Offset the beginning row.")
@click.option("--chunksize", default=None, help="Number of rows per chunk.")
@click.option("--limit", default=1000, help="Tang dataset size.")
@click.option("--ncores", default=8, help="Number of cores.")
def run(offset, chunksize, limit, ncores):
    logger.debug("Start...")

    con = duckdb.connect()

    con.sql("INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs;")
    con.sql(
        """
        CREATE OR REPLACE TABLE tang AS
        FROM 's3://open-demo-datasets/geoml_aquarry/preprocessed/70k_mine_polygon.parquet'
    """
    )
    logger.debug("Loaded Tang dataset.")

    df = con.sql(
        f"""
            SELECT
                objectid,
                cc,
                centroid,
                lon,
                lat,
                CONCAT(LPAD(objectid, 5, '0')) AS objectid_pad,
                CONCAT('tang_', LPAD(objectid, 5, '0')) AS filename,
                CONCAT('{BUCKET_PATH}', 'tang_', LPAD(objectid, 5, '0'), '.jpg')
                    AS s3path FROM tang LIMIT {limit}
        """
    ).df()
    logger.debug("Preprocess dataset.")

    logger.debug(df.head(2))

    # Existing prediction output files
    existing_objects = {
        "rgb": list(
            set(
                list_s3_objects_in_directory(
                    path="output/predict/23dec2023/dataset=tang/model=RCNN",
                    colors=["rgb"],
                )
            )
        ),
        "pcahog": list(
            set(
                list_s3_objects_in_directory(
                    path="output/predict/23dec2023/dataset=tang/model=RCNN",
                    colors=["pcahog"],
                )
            )
        ),
        "svhog": list(
            set(
                list_s3_objects_in_directory(
                    path="output/predict/23dec2023/dataset=tang/model=RCNN",
                    colors=["svhog"],
                )
            )
        ),
    }

    logger.debug(
        f"""Existing objects: \n
            rgb {len(existing_objects['rgb'])} \n
            pcahog {len(existing_objects['pcahog'])} \n
            svhog {len(existing_objects['svhog'])}
            """
    )

    # Existing Tang images
    existing_tang_images = [
        each.split("_")[1].split(".")[0]
        for each in list_s3_objects_in_directory(
            bucket_name="geoml-aquarry", path="output/gms/16dec2023/tang"
        )
    ]

    # Array of geodataframe rows to process
    model_names = ["RCNN"]
    img_transforms = ["rgb", "pcahog", "svhog"]

    # Create rows to process, for all combinations of models and img_transforms
    rows_to_process = []
    for row in df[offset:].itertuples():
        for model_name in model_names:
            for img_transform in img_transforms:
                # If doesn't already exists in S3 AND if Tang image exists
                if (
                    f"tang_{str(row.objectid_pad)}.parquet"
                    not in existing_objects[img_transform]
                    and str(row.objectid_pad) in existing_tang_images
                ):
                    rows_to_process.append(
                        (row.objectid_pad, model_name, img_transform)
                    )
    logger.debug(f"Rows to process: {len(rows_to_process)}")
    # Break the list into chunks of size equal to CPU count
    # Otherwise, the multiprocess pool would run random rows
    chunk_size = int(chunksize or multiprocessing.cpu_count())
    chunks = [
        rows_to_process[i : i + chunk_size]
        for i in range(0, len(rows_to_process), chunk_size)
    ]

    logger.debug(f"len(chunks), {len(chunks)}")
    logger.debug(f"chunk_size, {chunk_size}")

    # Run chunks of n rows at a time
    for idx, chunk in enumerate(chunks[2:]):
        print(f"Processing chunk {idx + 1} of {len(chunks)}")
        run_parallel(run_inference_multiprocessing, chunk, num_cores=ncores)

    logger.debug("End.")


if __name__ == "__main__":
    run()
