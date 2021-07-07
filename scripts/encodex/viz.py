import pandas as pd
from matplotlib import pyplot as plt
from typing import Union

def plot_range_coverage(
    signals: pd.DataFrame,
    chromosome: str = "Genome position",
    annotation = None,
    ax: Union[None, plt.axis] = None
) -> plt.axis:
    """
    Plot normalized signal over a genomic range, from multiple bigWig files
    ----------
    signals
        A data frame of read coverage signal in a genomic range.
    ax
        If there is a figure already present, plot on this axis.
    Returns
    -------
    The matplotlib axis of the plot.
    """
    
    if ax is None:
        fig, ax = plt.subplots()
    
    sliding = signals.max().max()
    start =  signals.index.min()
    end = signals.index.max()
    mid_range = (start + end) / 2
    
    if annotation is not None:
        tracks = annotation.loc[((annotation.Chr == chromosome) & (annotation.Transcript == "gene")) & ((annotation.Start_g < end) & (annotation.End_g > start))]
        annot_step = sliding * 0.3
        annot_i = 0
        for index, row in tracks.iterrows():
            annot_i = annot_i - annot_step
            ax.fill_between([row["Start_g"], row["End_g"]], annot_i, annot_i + sliding * 0.2, color="silver")
            text_start = row["Start_g"] if row["Start_g"] > start else start
            ax.text(text_start, annot_i, row["gene_id"], ha="left", va="bottom")
    
    for i, xpr in enumerate(signals.columns):
        baseline = sliding * i
        ax.fill_between(signals.index, signals[xpr] + baseline, baseline, label=xpr)
        ax.text(mid_range, baseline + (sliding - 0.3*sliding), xpr, ha="center", va="top")
    
    ax.set_xlim(start, end)
    ax.set_xlabel(chromosome)
    ax.set_ylabel("Normalized signal intensity")
    ax.set_yticklabels([])
    ax.yaxis.set_ticks_position("none")
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    return ax