import os, subprocess
import pyBigWig
import numpy as np
import pandas as pd
from typing import Union

def read_files_manifest(
    manifest_s3_path: str = "s3://encode-public/encode_file_manifest.tsv",
    manifest_local_path: Union[None, str] = None,
    force_download: bool = False
) -> pd.DataFrame:
    """
    Downloads the files manifest of ENCODE datasets from S3.
    Parameters
    ----------
    manifest_s3_path
        Path to the manifest file on S3 (should not change).
    manifest_local_path
        Local path where manifest file should be saved or is already saved.
    force_download
        If manifest table should be downloaded even if file exists locally.
    Returns
    -------
    A dataframe with metadata for all ENCODE data files.
    """

    cleanup_manifest = False
    manifest_present = False

    # Default option is to download manifest file temporarily and remove it
    if manifest_local_path is None:
        manifest_local_path = "encode_file_manifest.tsv"
        cleanup_manifest = True
    
    # If there is already a manifest file locally, overlapping the manifest name, do not remove
    if os.path.isfile(manifest_local_path):
        cleanup_manifest = False
        manifest_present = True
    
    # Download manifest only if not present already
    if force_download or not manifest_present:
        subprocess.run(["aws", "s3", "cp", manifest_s3_path, manifest_local_path, "--no-sign-request"])
    
    manifest_df = pd.read_csv(manifest_local_path, sep="\t")

    # Remove file if no file name was specified
    if cleanup_manifest:
        os.remove(manifest_local_path)
    
    return manifest_df

def read_experiment_bw(
    bw_s3_path: str,
    bw_local_path: Union[None, str] = None,
    force_download: bool = False
) -> pd.DataFrame:
    """
    Downloads the files manifest of ENCODE datasets from S3.
    Parameters
    ----------
    bw_s3_path
        Path to a bigWig file on S3.
    bw_local_path
        Local path where file should be saved or is already saved.
    force_download
        If bigWig should be downloaded even if it exists locally.
    Returns
    -------
    A bigwig object with signal in genomic ranges.
    """

    cleanup_bw = False
    bw_present = False

    # Default option is to download file temporarily and remove it
    if bw_local_path is None:
        bw_local_path = "experiment.bigWig"
        cleanup_bw = True
    
    # If the file is already present locally, do not remove
    if os.path.isfile(bw_local_path):
        cleanup_bw = False
        bw_present = True
    
    # Download file only if not present already
    if force_download or not bw_present:
        subprocess.run(["aws", "s3", "cp", bw_s3_path, bw_local_path, "--no-sign-request"])
    
    bw = pyBigWig.open(bw_local_path)

    # Remove file if no file name was specified
    if cleanup_bw:
        os.remove(bw_local_path)
    
    return bw