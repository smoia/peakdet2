# -*- coding: utf-8 -*-
"""
Helper class for holding physiological data and associated metadata information
"""
import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedStyle

from peakdet import __version__


class Window:
    def __init__(self, master):

        # Style
        s = ThemedStyle()
        s.theme_use("yaru")

        # Make title
        frame_title = ttk.Frame(master)
        frame_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        label = ttk.Label(frame_title, text="Name of file")
        label.pack()

        # Initialize a variable to interact with the plot
        interaction = tk.IntVar()

        # Create a frame to hold all labelframes in a single column on the left
        left_column = ttk.Frame(master)
        left_column.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

        # Menu to set peak detection parameters
        frame_peakdetvar = ttk.LabelFrame(left_column, text="Peak detection parameters")
        frame_peakdetvar.grid(row=0, column=0, sticky="ew", padx=3, pady=5)

        thresh = ttk.Entry(frame_peakdetvar)
        thresh.insert(0, "Threshold [0,1]")
        thresh.grid(row=0, column=0, padx=5, pady=3)
        dist = ttk.Entry(frame_peakdetvar)
        dist.insert(0, "Distance [0,inf)")
        dist.grid(row=1, column=0, padx=5, pady=3)

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
        radio_rempeaks.pack(padx=5, pady=3)

        channel_list = ["Channel 1", "Channel 2", "Channel 3"]
        reference_channel = ttk.Combobox(frame_movesignal, values=channel_list)
        reference_channel.set("Reference Channel")
        reference_channel.pack(padx=5, pady=3)
        moving_channel = ttk.Combobox(frame_movesignal, values=channel_list)
        moving_channel.set("Moving Channel")
        moving_channel.pack(padx=5, pady=3)

        button_realignsignal = ttk.Button(
            frame_movesignal, text="Run automatic realignment"
        )
        button_realignsignal.pack(padx=5, pady=3)

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
        rightframe = ttk.LabelFrame(left_column)
        rightframe.grid(row=1, column=1, sticky="ns", padx=5, pady=5)


# Create window
root = tk.Tk()
root.geometry("1920x1080")
root.title(f"Peak Editor, prep4phys v{__version__}")
window = Window(root)
root.mainloop()
