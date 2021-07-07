import os, subprocess
import pyBigWig
import numpy as np
import pandas as pd
from typing import Union


def read_from_s3(
    s3_path: str,
    default_path: Union[None, str] = None,
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
    if default_path is None:
        default_path = s3_path.split("/")[-1]

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
        manifest_s3_path, None,  manifest_local_path,
        force_download
    )
    
    # Parse file
    manifest_df = pd.read_csv(manifest_local_path, sep="\t")

    # Remove file if no file name was specified
    if cleanup_manifest:
        os.remove(manifest_local_path)
    
    return manifest_df


def read_genome_annotation(
    annotation_s3_path: str = "s3://encode-public/2019/06/04/8f6cba12-2ebe-4bec-a15d-53f498979de0/gencode.v29.primary_assembly.annotation_UCSC_names.gtf.gz",
    annotation_local_path: Union[None, str] = None,
    force_download: bool = False,
    keep_file: bool = False
) -> pd.DataFrame:
    """
    Downloads the GENCODE genome annotation file from S3.
    Parameters
    ----------
    annotation_s3_path
        Path to the genome annotation gtf.gz file on S3.
    annotation_local_path
        Local path where file should be saved or is already saved.
    force_download
        If bigWig should be downloaded even if it exists locally.
    keep_file
        Do not delete local copy of file after download, even if no explicit path was given.
    Returns
    -------
    A dataframe with all the genome annotations.
    """

    # Download file from S3
    annotation_local_path, cleanup_annotation = read_from_s3(
        annotation_s3_path, None, annotation_local_path,
        force_download
    )

    # Ignore cleanupsignap if requested
    if keep_file:
        cleanup_bw = False
    
    # Parse file
    gtf_names = [
        "Chr", "Source", "Transcript", "Start_g", "End_g", "Score",
        "Strand", "Phase", "Description"
    ]
    genome_annotation_raw = pd.read_csv(
        annotation_local_path, compression="gzip", skiprows=5, sep="\t",
        names=gtf_names, error_bad_lines=False
    )

    # Expand the description column
    cols_to_xpnd = genome_annotation_raw.Description.str.split("; ")
    cols_to_xpnd = cols_to_xpnd.apply(lambda x: {z[0]: z[1].replace('"', "") for z in [y.split(' ') for y in x]})
    cols_to_xpnd = cols_to_xpnd.to_dict()
    cols_to_xpnd = pd.DataFrame.from_dict(cols_to_xpnd, orient='index')

    genome_annotation = pd.concat([genome_annotation_raw.drop("Description", axis=1), cols_to_xpnd], axis=1)
    genome_annotation["Start"] = genome_annotation.apply(lambda x: x["Start_g"] if x["Start_g"] < x["End_g"] else x["End_g"], axis=1)
    genome_annotation["End"] = genome_annotation.apply(lambda x: x["End_g"] if x["Start_g"] < x["End_g"] else x["Start_g"], axis=1)

    # Remove file if no file name was specified
    if cleanup_annotation:
        os.remove(annotation_local_path)
    
    return genome_annotation


def read_experiment_bw(
    bw_s3_path: str,
    bw_local_path: Union[None, str] = None,
    force_download: bool = False,
    keep_file: bool = False
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
    keep_file
        Do not delete local copy of file after download, even if no explicit path was given.
    Returns
    -------
    A bigwig object with signal in genomic ranges.
    """

    # Download file from S3
    bw_local_path, cleanup_bw = read_from_s3(
        bw_s3_path, None, bw_local_path,
        force_download
    )

    # Ignore cleanup signal if requested
    if keep_file:
        cleanup_bw = False
    
    # Parse file
    bw = pyBigWig.open(bw_local_path)

    # Remove file if no file name was specified
    if cleanup_bw:
        os.remove(bw_local_path)
    
    return bw