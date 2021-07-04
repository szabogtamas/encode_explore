import subprocess
import pandas as pd
from typing import Union

def read_files_manifest(
    manifest_s3_path: str = "s3://encode-public/encode_file_manifest.tsv",
    manifest_local_path: Union[None, str, list] = None
) -> pd.DataFrame:
    """
    Downloads the files manifest of ENCODE datasets from S3.
    Parameters
    ----------
    manifest_s3_path
        Path to the manifest file on S3 (should not change).
    manifest_local_path
        Local path where manifest file should be saved or is already saved.
    Returns
    -------
    A dataframe with metadata for all ENCODE data files.
    """

    if manifest_local_path is None:
        manifest_local_path = "encode_file_manifest.tsv"
    manifest_df = subprocess.run(["aws", "s3", "cp", manifest_s3_path, manifest_local_path, "--no-sign-request"])

    return manifest_df