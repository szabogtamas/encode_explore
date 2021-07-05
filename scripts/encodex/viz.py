from matplotlib import pyplot as plt
from typing import Union

def plot_range_coverage(
    signals: list,
    ax: Union[None, plt.axis] = None
) -> plt.axis:
    """
    Plot normalized signal over a genomic range, from multiple bigWig files
    ----------
    signals
        List of numpy arrays representing read coverage.
    ax
        If there is a figure already present, plot on this axis.
    Returns
    -------
    The matplotlib axis of the plot.
    """
    
    if ax is None:
        fig, ax = plt.subplots()
    for signal_values in signals:
        ax.plot(range(len(signal_values)), signal_values)
        ax.set_ylim(0, 3)
    return ax