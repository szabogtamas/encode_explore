import numpy as np
import pandas as pd
from typing import Union
from io import read_experiment_bw

def extract_genomic_range(
    s3_path: str,
    gn_range: tuple
) -> plt.axis:
    """
    Extract signals corresponding a given genomic range froma bigWig file
    ----------
    s3_path
        Path to bigWig file on S3.
    gn_range
       A genomic range to retrieve. Defined as chromosome, start, end.
    Returns
    -------
    A numpy array of signals.
    """

    chromosome, start, end = gn_range
    bw = read_experiment_bw(s3_path, force_download=True)
    signals = bw.values(chromosome, start, end, numpy=True)

    return signals


def retrieve_bw_paths_by_experiment(
    encodedb_files: pd.DataFrame,
    experiments: list,
    strand: str = "plus strand signal of unique reads",
    assembly: str = "GRCh38"
) -> pd.DataFrame:
    """
    Filter the files manifest to find bigwig files associated withe an experiment
    ----------
    encodedb_files
        The S3 files manifest table.
    experiments
        Experiment accessions to look up.
    strand
        Filter positive strand files by default.
    assembly
        Genome assembly (matching genomic range).
    Returns
    -------
    The filtered dataframe.
    """

    experiments = ["/experiments/" + x for x in experiments]
    bigwigs = encodedb_files.loc[
        (encodedb_files.dataset.isin(experiments)) & (encodedb_files.file_format == "bigWig") & (encodedb_files.output_type == strand)
    ]

    return bigwigs