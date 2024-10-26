# -*- coding: utf-8 -*-
"""
Helper class for holding physiological data and associated metadata information
"""
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from darkdetect import theme
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sv_ttk import set_theme

from peakdet import __version__


class Window:
    def __init__(self, master):

        # Temporary channel for preview
        channel_list = ["Channel 1", "Channel 2", "Channel 3"]

        # Style
        set_theme(theme())

        # Make title
        frame_title = ttk.Frame(master)
        frame_title.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 5))
        label = ttk.Label(frame_title, text="Name of file")
        label.grid(row=0, column=0)

        # Initialize a variable to interact with the plot
        interaction = tk.IntVar()

        # Create a frame to hold all labelframes in a single column on the left
        left_column = ttk.Frame(master)
        left_column.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

        # Menu to set peak detection parameters
        frame_peakdetvar = ttk.LabelFrame(left_column, text="Peak detection parameters")
        frame_peakdetvar.grid(row=0, column=0, sticky="ew", padx=3, pady=5)

        label_thresh = ttk.Label(frame_peakdetvar, text="Threshold [0, 1]: ")
        label_thresh.grid(row=0, column=0, sticky="nw", pady=3)
        entry_thresh = ttk.Entry(frame_peakdetvar, width=5)
        entry_thresh.insert(0, "0.2")
        entry_thresh.grid(row=0, column=1, sticky="ne", pady=3)
        label_dist = ttk.Label(frame_peakdetvar, text="Distance [0, inf): ")
        label_dist.grid(row=1, column=0, sticky="w", pady=3)
        entry_dist = ttk.Entry(frame_peakdetvar, width=5)
        entry_dist.insert(0, "0")
        entry_dist.grid(row=1, column=1, sticky="e", pady=3)
        label_activechannel = ttk.Label(frame_peakdetvar, text="Channel: ")
        label_activechannel.grid(row=2, column=0, sticky="se", pady=3)
        box_activechannel = ttk.Combobox(frame_peakdetvar, values=channel_list)
        box_activechannel.set("Active Channel")
        box_activechannel.grid(row=2, column=1, sticky="sw", pady=3)

        # Menu for automatic peak detection
        frame_peakdet = ttk.Frame(left_column)
        frame_peakdet.grid(row=1, column=0, sticky="ew", padx=3, pady=5)

        button_runpeakdet = ttk.Button(frame_peakdet, text="Run peak detection")
        button_runpeakdet.pack(padx=5, pady=3)

        # Menu for peak editing
        frame_editpeaks = ttk.LabelFrame(left_column, text="Edit Peaks")
        frame_editpeaks.grid(row=2, column=0, sticky="ew", padx=3, pady=5)

        radio_delpeaks = ttk.Radiobutton(
            frame_editpeaks, text="Delete peaks", variable=interaction, value=1
        )
        radio_delpeaks.pack(padx=5, pady=3)
        radio_addpeaks = ttk.Radiobutton(
            frame_editpeaks, text="Add single peak", variable=interaction, value=2
        )
        radio_addpeaks.pack(padx=5, pady=3)
        radio_detpeaks = ttk.Radiobutton(
            frame_editpeaks,
            text="Multi-peaks estimation",
            variable=interaction,
            value=3,
        )
        radio_detpeaks.pack(padx=5, pady=3)

        # Menu for artefact marking (what was peak "rejection")
        frame_markartefact = ttk.LabelFrame(left_column, text="Artefacts")
        frame_markartefact.grid(row=3, column=0, sticky="ew", padx=3, pady=5)

        radio_rempeaks = ttk.Radiobutton(
            frame_markartefact, text="Mark Artefact", variable=interaction, value=4
        )
        radio_rempeaks.pack(padx=5, pady=3)

        # Menu for realignment
        frame_movesignal = ttk.LabelFrame(left_column, text="Realign timeseries")
        frame_movesignal.grid(row=4, column=0, sticky="ew", padx=3, pady=5)

        radio_rempeaks = ttk.Radiobutton(
            frame_movesignal, text="Manual realignment", variable=interaction, value=5
        )
        radio_rempeaks.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=3)

        label_reference = ttk.Label(frame_movesignal, text="Reference: ")
        label_reference.grid(row=1, column=0, sticky="e", pady=3)
        box_referencechannel = ttk.Combobox(frame_movesignal, values=channel_list)
        box_referencechannel.set("Reference Channel")
        box_referencechannel.grid(row=1, column=1, sticky="w", pady=3)
        label_moving = ttk.Label(frame_movesignal, text="Moving: ")
        label_moving.grid(row=2, column=0, sticky="e", pady=3)
        box_movingchannel = ttk.Combobox(frame_movesignal, values=channel_list)
        box_movingchannel.set("Moving Channel")
        box_movingchannel.grid(row=2, column=1, sticky="w", pady=3)

        button_realignsignal = ttk.Button(
            frame_movesignal, text="Run automatic realignment"
        )
        button_realignsignal.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=3
        )

        # Menu for plot interaction
        frame_plotinteraction = ttk.LabelFrame(left_column, text="Plot interaction")
        frame_plotinteraction.grid(row=5, column=0, sticky="ew", padx=3, pady=5)

        radio_scroll = ttk.Radiobutton(
            frame_plotinteraction, text="Scroll", variable=interaction, value=6
        )
        radio_scroll.pack(padx=5, pady=3)
        radio_zoom = ttk.Radiobutton(
            frame_plotinteraction, text="Zoom", variable=interaction, value=7
        )
        radio_zoom.pack(padx=5, pady=3)

        # Plots!
        rightframe = ttk.Frame(master)
        rightframe.grid(row=1, column=1, sticky="ns", padx=5, pady=5)


# Create window
root = tk.Tk()
root.geometry("1920x1080")
root.title(f"Peak Editor, prep4phys v{__version__}")
window = Window(root)
root.mainloop()
