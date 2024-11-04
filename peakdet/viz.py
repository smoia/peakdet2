# -*- coding: utf-8 -*-
"""
Function to plot physiological data.
"""
import os
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def get_screen_size():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def plot_physiodata(
    data,
    fs=None,
    startcol=None,
    endcol=None,
    height=None,
    width=None,
    transpose=False,
    show=True,
):
    """
    Plot physiological signals in an array

    Parameters
    ----------
    data : numpy.ndarray, peakdet.Physio, or str
        2D array of physio data (timepoints * channels) or path to it.
    fs : None, optional
        Sample frequency of physiological data, used to plot against time.
    startcol : None, optional
        First column (channel) to use. If None, starts from 0.
    endcol : None, optional
        Last column (channel) to use. If None, ends at -1.
    height : None, optional
        Height of plot. If None, it automatically computes it based on # of channels.
    width : None, optional
        Width of plot. If None, it uses the whole screen width.
    transpose : bool, optional
        Transpose data. Default is false.
    show : bool, optional
        Plot the data. If False, returns figure and axes instead.

    Raises
    ------
    IOError
        If it cannot read the data
    Warning
        If the data is 3+D
    """
    # If data is a string and it's an existing path, read the data.
    if isinstance(data, str):
        if os.path.exists(data):
            ext = os.path.splitext(data)[-1]

            if ext == ".gz":
                ext == os.path.splitext(os.path.splitext(data)[0])[-1]

            if ext == ".tsv":
                data = np.genfromtxt(data, delimiter="\t")
            elif ext == ".csv":
                data = np.genfromtxt(data, delimiter=",")
            else:
                data = np.genfromtxt(data)
        else:
            raise IOError(f"Cannot find {data}")

    # If data is a physio object, do some stuff
    if hasattr(data, "history"):
        # If it has a frequency and fs is specified, warn and continue, else read it
        if data.fs is not None:
            if fs is not None:
                raise Warning(
                    f"Using sampling frequency {fs} instead of data's {data.fs}"
                )
            else:
                fs = data.fs
        data = data.data

    # Compute time if fs is given
    if fs is not None:
        time = np.arange(data.shape[0]) / fs

    if data.ndim == 1:
        data = data[..., np.newaxis]
    elif data.ndim > 2:
        raise Warning("Data has more axes than possible to plot. Using first two.")
        data = data[(...,) + (slice(1),) * (data.ndim - 2)].squeeze()

    data = data.T if transpose else data

    data = data[:, startcol:endcol]

    # Create a figure with as many rows as the columns of the 2D array
    if width is None:
        width = int(str(get_screen_size()[0])[:-2])
    if height is None:
        height = data.shape[1] * (width / 16) * 0.9

    fig, axes = plt.subplots(
        nrows=data.shape[1], ncols=1, figsize=(width, height), sharex=True
    )

    if data.shape[1] == 1:
        axes = [axes]

    # Plot each column in a separate row
    for i in range(data.shape[1]):
        if fs is None:
            axes[i].plot(data[:, i])
        else:
            axes[i].plot(time, data[:, i])
        axes[i].set_title(f"Channel {i+1}")

    # Adjust layout and show the plot
    plt.tight_layout()

    if show:
        plt.show()
    else:
        return fig, axes
