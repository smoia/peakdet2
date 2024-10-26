# -*- coding: utf-8 -*-
"""
Helper class for holding physiological data and associated metadata information
"""
import tkinter as tk
from tkinter import ttk

from peakdet import __version__


class Window:
    def __init__(self, master):

        # Make title
        frame_title = ttk.Frame(master)
        frame_title.pack()
        label = tk.Label(frame_title, text="Name of file")
        label.pack()

        # Initialize a variable to interact with the plot
        interaction = tk.IntVar()

        # Menu to set peak detection parameters
        frame_peakdetvar = ttk.LabelFrame(master, text="Peak detection parameters")
        frame_peakdetvar.pack(side=tk.LEFT, padx=5, pady=3)

        thresh = tk.Entry(frame_peakdetvar, relief=tk.SUNKEN)
        thresh.insert(0, "Threshold [0,1]")
        thresh.pack(padx=5, pady=3)
        dist = tk.Entry(frame_peakdetvar, relief=tk.SUNKEN)
        dist.insert(0, "Distance [0,inf)")
        dist.pack(padx=5, pady=3)

        # Menu for automatic peak detection
        frame_peakdet = ttk.Frame(master)
        frame_peakdet.pack(side=tk.LEFT, padx=5, pady=3)

        button_runpeakdet = tk.Button(frame_peakdet, text="Run peak detection")
        button_runpeakdet.pack(padx=5, pady=3)

        # Menu for peak editing
        frame_editpeaks = ttk.LabelFrame(master, text="Edit Peaks")
        frame_editpeaks.pack(side=tk.LEFT, padx=5, pady=3)

        radio_delpeaks = tk.Radiobutton(
            frame_editpeaks, text="Delete peaks", variable=interaction, value=1
        )
        radio_delpeaks.pack(padx=5, pady=3)
        radio_addpeaks = tk.Radiobutton(
            frame_editpeaks, text="Add single peak", variable=interaction, value=2
        )
        radio_addpeaks.pack(padx=5, pady=3)
        radio_detpeaks = tk.Radiobutton(
            frame_editpeaks,
            text="Multi-peaks estimation",
            variable=interaction,
            value=3,
        )
        radio_detpeaks.pack(padx=5, pady=3)

        # Menu for artefact marking (what was peak "rejection")
        frame_markartefact = ttk.LabelFrame(master, text="Artefacts")
        frame_markartefact.pack(side=tk.LEFT, padx=5, pady=3)

        radio_rempeaks = tk.Radiobutton(
            frame_markartefact, text="Mark Artefact", variable=interaction, value=4
        )
        radio_rempeaks.pack(padx=5, pady=3)

        # Menu for realignment
        frame_movesignal = ttk.LabelFrame(master, text="Realign timeseries")
        frame_movesignal.pack(side=tk.LEFT, padx=5, pady=3)

        radio_rempeaks = tk.Radiobutton(
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

        button_realignsignal = tk.Button(
            frame_movesignal, text="Run automatic realignment"
        )
        button_realignsignal.pack(padx=5, pady=3)

        # Menu for plot interaction
        frame_plotinteraction = ttk.LabelFrame(master, text="Plot interaction")
        frame_plotinteraction.pack(side=tk.LEFT, padx=5, pady=3)

        radio_scroll = tk.Radiobutton(
            frame_plotinteraction, text="Scroll", variable=interaction, value=6
        )
        radio_scroll.pack(padx=5, pady=3)
        radio_zoom = tk.Radiobutton(
            frame_plotinteraction, text="Zoom", variable=interaction, value=6
        )
        radio_zoom.pack(padx=5, pady=3)

        # Plots!
        rightframe = ttk.LabelFrame(master)
        rightframe.pack(side=tk.RIGHT)


# Create window
root = tk.Tk()
root.geometry("1920x1080")
root.title(f"Peak Editor, prep4phys v{__version__}")
window = Window(root)
root.mainloop()
