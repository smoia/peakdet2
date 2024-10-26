# -*- coding: utf-8 -*-
"""
Helper class for holding physiological data and associated metadata information
"""
from copy import deepcopy

import numpy as np


class Physio:
    """
    Class to hold physiological data and relevant information.

    Parameters
    ----------
    data : array_like
        Input data array or a list of lists.
    fs : array_like, optional
        Sampling rates corresponding to each channel in `data` (Hz). Default: None
    history : list of tuples, optional
        Functions performed on `data`. Default: None
    metadata : dict, optional
        Metadata associated with `data`. Default: None

    Attributes
    ----------
    data : :obj:`numpy.ndarray`
        Physiological waveform with shape (n_samples, n_channels)
    fs : :obj:`numpy.ndarray`
        Array of sampling rates corresponding to each channel in Hz
    history : list of tuples
        History of functions that have been performed on `data`, with relevant
        parameters provided to functions.
    peaks : list of :obj:`numpy.ndarray`
        List of 1D arrays, each containing indices of peaks in each channel of `data`
    troughs : list of :obj:`numpy.ndarray`
        List of 1D arrays, each containing indices of troughs in each channel of `data`
    """

    def __init__(
        self, data, fs=None, ch_names=None, history=None, metadata=None, suppdata=None
    ):
        """Initialise Physio object."""
        self._data = np.asarray(deepcopy(data))
        if self._data.ndim > 2:
            raise ValueError(f"Provided data dimensionality {self._data.ndim} > 2.")
        if self._data.ndim == 1:
            self._data = self._data[:, np.newaxis]

        if not np.issubdtype(self._data.dtype, np.number):
            raise ValueError(
                f"Provided data of type {self._data.dtype} is not numeric."
            )

        self._fs = np.asarray(deepcopy(fs), dtype=np.float64)
        if self._fs.ndim == 0:
            self._fs = np.full(self._data.shape[1], self._fs)
        elif self._fs.shape[0] != self._data.shape[1] or self._fs.ndim > 1:
            raise ValueError(
                "Specified frequency must be either a number or a 1D array with length equal to the number of channels in data."
            )

        self._ch_names = (
            [f"ch{i}" for i in range(self._data.shape[1])]
            if ch_names is None
            else deepcopy(ch_names)
        )
        if not isinstance(self._ch_names, list) or any(
            [not isinstance(f, str) for f in self._ch_names]
        ):
            raise TypeError(
                "Provided channels name list must be a list-of-strings. Please check inputs."
            )

        self._history = [] if history is None else deepcopy(history)
        if not isinstance(self._history, list) or any(
            [not isinstance(f, tuple) for f in self._history]
        ):
            raise TypeError(
                f"Provided history {history} must be a list-of-tuples. Please check inputs."
            )

        if metadata is not None:
            if not isinstance(metadata, dict):
                raise TypeError(f"Provided metadata {metadata} must be dict-like.")
            for k in ["peaks", "troughs"]:
                if k in metadata:
                    if not isinstance(metadata[k], list) or any(
                        [
                            not isinstance(arr, np.ndarray) or arr.ndim != 1
                            for arr in metadata[k]
                        ]
                    ):
                        raise TypeError(f"{k} must be a list of 1D numpy arrays.")
                    if len(metadata[k]) != self._data.shape[1]:
                        raise ValueError(
                            f"{k} must have length equal to the number of channels in data."
                        )
                else:
                    metadata[k] = [
                        np.empty(0, dtype=int) for _ in range(self._data.shape[1])
                    ]
            self._metadata = dict(**deepcopy(metadata))

        else:
            self._metadata = {
                "peaks": [np.empty(0, dtype=int) for _ in range(self._data.shape[1])],
                "troughs": [np.empty(0, dtype=int) for _ in range(self._data.shape[1])],
                "reject": [[] for _ in range(self._data.shape[1])],
            }

    def __array__(self):
        return self.data

    def __getitem__(self, slicer):
        return self.data[slicer]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "{name}(size={size}, fs={fs})".format(
            name=self.__class__.__name__, size=self.data.size, fs=self.fs
        )

    __repr__ = __str__

    @property
    def data(self):
        """Physiological data."""
        return self._data

    @property
    def ndim(self):
        """Ndarray ndim."""
        return self._data.ndim

    @property
    def shape(self):
        """Ndarray ndim."""
        return self._data.shape

    @property
    def nsamples(self):
        """
        Property. Returns number of channels (ch).

        Returns
        -------
        int
            Number of channels
        """
        return self._data.shape[0]

    @property
    def nch(self):
        """
        Property. Returns number of channels (ch).

        Returns
        -------
        int
            Number of channels
        """
        return self._data.shape[1]

    @property
    def fs(self):
        """Sampling rate of data (Hz)."""
        return self._fs

    @property
    def history(self):
        """Functions that have been performed on / modified `data`."""
        return self._history

    @property
    def peaks(self):
        """Return indices of detected peaks in `data`."""
        return self._masked("peaks")

    @property
    def troughs(self):
        """Return indices of detected troughs in `data`."""
        return self._masked("troughs")

    @property
    def rejected(self):
        """Return indices of rejected areas in `data`."""
        return self._metadata["reject"]

    @property
    def _masked(self, k):
        mask_range = []
        for sublist in self._metadata["reject"]:
            ranges = []
            for start, end in sublist:
                ranges.append(np.arange(start, end))
            concatenated = np.concatenate(ranges) if ranges else np.array([], dtype=int)
            mask_range.append(concatenated)

        mask = []
        for n, array in enumerate(self._metadata[k]):
            mask.append(
                np.ma.masked_array(
                    self._metadata[k], mask=np.isin(array, mask_range[n])
                )
            )

        return mask
