import numpy as np
import pandas as pd
from typing import Union
from . import io as module_io


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

    experiments = ["/experiments/" + x + "/" for x in experiments]
    m1 = encodedb_files.dataset.isin(experiments)
    m2 = (encodedb_files.file_format == "bigWig")
    m3 = (encodedb_files.output_type == strand)
    m4 = (encodedb_files.assembly == assembly)
    bigwigs = encodedb_files.loc[m1 & m2 & m3 & m4]

    return bigwigs


def extract_genomic_range(
    s3_path: str,
    gn_range: tuple
) -> pd.DataFrame:
    """
    Extract signals corresponding a given genomic range from a bigWig file
    ----------
    s3_path
        Path to bigWig file on S3.
    gn_range
       A genomic range to retrieve. Defined as chromosome, start, end.
    Returns
    -------
    A dataframe of signals at genomic positions.
    """

    chromosome, start, end = gn_range
    experiment_id = s3_path.split("/")[-1]
    experiment_id = experiment_id.split(".")[0]
    bw = module_io.read_experiment_bw(s3_path, keep_file=True)
    signals = bw.values(chromosome, start, end, numpy=True)

    signal_tab = pd.DataFrame({"Position": range(start, end), experiment_id: signals})
    signal_tab = signal_tab.set_index("Position")

    return signal_tab


def combine_experiment_signals(
    s3_paths: list,
    gn_range: tuple
) -> pd.DataFrame:
    """
    Extract signals corresponding a given genomic range from multiple experiments and combine into a df
    ----------
    s3_paths
        Paths to bigWig files on S3.
    gn_range
       A genomic range to retrieve. Defined as chromosome, start, end.
    Returns
    -------
    A dataframe of signals at genomic positions.
    """

    signal_tab = None
    
    for bw in s3_paths:
        stb = extract_genomic_range(bw, gn_range)
        if signal_tab is None:
            signal_tab = stb
        else:
            signal_tab = signal_tab.join(stb)
    
    return signal_tab