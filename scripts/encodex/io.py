import os, subprocess
import pyBigWig
import numpy as np
import pandas as pd
from typing import Union


def read_from_s3(
    s3_path: str,
    default_path: str,
    local_path: Union[None, str] = None,
    force_download: bool = False
) -> tuple:
    """
    Helper function downloading a file from S3 if not yet present.
    Parameters
    ----------
    s3_path
        Path to the file on S3.
    default_path
        A default file name to use.
    local_path
        Local path where file should be saved or is already saved.
    force_download
        If manifest table should be downloaded even if file exists locally.
    Returns
    -------
    A file path string and boolean value indicating file if file should be removed.
    """

    file_present = False
    cleanup_file = False

    # Default option is to download manifest file temporarily and remove it
    if local_path is None:
        local_path = default_path
        cleanup_file = True
    
    # If there is already a file locally, with overlapping name, do not remove
    if os.path.isfile(local_path):
        file_present = True
        cleanup_file = False
    
    # Download manifest only if not present already
    if force_download or not file_present:
        subprocess.run(["aws", "s3", "cp", s3_path, local_path, "--no-sign-request"])
    
    return local_path, cleanup_file


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

    # Download file from S3
    manifest_local_path, cleanup_manifest = read_from_s3(
        manifest_s3_path, "encode_file_manifest.tsv",
        manifest_local_path, force_download
    )
    
    # Parse file
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
    
    # Use base filename as default name for bw files
    base_filename = bw_s3_path.split("/")[-1]

    # Download file from S3
    bw_local_path, cleanup_bw = read_from_s3(
        bw_s3_path, base_filename,
        bw_local_path, force_download
    )
    
    # Parse file
    bw = pyBigWig.open(bw_local_path)

    # Remove file if no file name was specified
    if cleanup_bw:
        os.remove(bw_local_path)
    
    return bw