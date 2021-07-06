import pandas as pd
from matplotlib import pyplot as plt
from typing import Union

def plot_range_coverage(
    signals: pd.DataFrame,
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
    for xpr in signals.columns:
        signal_values = signals[xpr]
        ax.plot(range(len(signal_values)), signal_values, label=xpr)
        ax.set_ylim(0, 3)
    return ax