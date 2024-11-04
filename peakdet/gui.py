# -*- coding: utf-8 -*-
"""
Helper function to initialize a GUI window for visualizing and editing physiological data.
"""
import tkinter as tk
from copy import deepcopy
from tkinter import ttk

from darkdetect import theme
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sv_ttk import set_theme

from peakdet import __version__

from .viz import plot_physiodata


def emptyfunc(physio=None):
    # Momentarily here for menu
    pass


class Window:
    def __init__(self, master, physio=None, fs=None):
        # This whole thing works only if "physio" is shallow-copied. Otherwise, it does not.

        # ## Temporary channel for preview
        channel_list = ["Channel 1", "Channel 2", "Channel 3"]

        # ## Style
        set_theme(theme())

        # ######################## Menus ######################## #

        # ## Create menu
        master.option_add("*tearOff", tk.FALSE)
        menu_master = tk.Menu(master)
        # menu_master.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 5))

        # File menu
        menu_file = tk.Menu(menu_master, tearoff=0)
        menu_master.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Load", command=lambda: emptyfunc(physio))
        menu_file.add_command(label="Save", command=lambda: emptyfunc(physio))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=master.destroy)

        # Options menu
        menu_options = tk.Menu(menu_master, tearoff=0)
        menu_master.add_cascade(label="Options", menu=menu_options)
        menu_options.add_command(label="About", command=lambda: emptyfunc())
        menu_options.add_command(label="Documentation", command=lambda: emptyfunc())
        menu_options.add_separator()
        menu_theme = tk.Menu(menu_master, tearoff=0)
        menu_options.add_cascade(label="Theme", menu=menu_theme)
        menu_theme.add_command(label="Light", command=lambda: set_theme("light"))
        menu_theme.add_command(label="Dark", command=lambda: set_theme("dark"))

        master.config(menu=menu_master)

        # ## Report active file
        frame_title = ttk.Frame(master)
        frame_title.grid(row=0, column=0, columnspan=2, sticky="new", pady=(10, 5))
        label = ttk.Label(frame_title, text="Name of file")
        label.grid(row=0, column=0)

        # ######################## Left Frame ######################## #

        # ## Initialize a variable to interact with the plot
        interaction = tk.IntVar()
        detect_opposite = tk.BooleanVar(value=False)
        point_type = ["Peaks", "Troughs", "Zero cross", "1st Deriv", "2nd Deriv"]

        # ## Create a frame to hold all labelframes in a single column on the left
        left_column = ttk.Frame(master)
        left_column.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

        # Frame for all peak detection related
        frame_peakdet = ttk.LabelFrame(left_column, text="Point detection")
        frame_peakdet.grid(row=0, column=0, sticky="ew", padx=3, pady=5)

        label_activechannel = ttk.Label(frame_peakdet, text="Channel: ")
        label_activechannel.grid(row=0, column=0, sticky="se", padx=(5, 1), pady=3)
        box_activechannel = ttk.Combobox(frame_peakdet, values=channel_list)
        box_activechannel.set("Active Channel")
        box_activechannel.grid(row=0, column=1, sticky="sw", padx=(1, 5), pady=3)

        label_pointtype = ttk.Label(frame_peakdet, text="Point: ")
        label_pointtype.grid(row=1, column=0, sticky="se", padx=(5, 1), pady=3)
        box_pointtype = ttk.Combobox(frame_peakdet, values=point_type)
        box_pointtype.set("Active Channel")
        box_pointtype.grid(row=1, column=1, sticky="sw", padx=(1, 5), pady=3)

        label_thresh = ttk.Label(frame_peakdet, text="Threshold [0, 1]: ")
        label_thresh.grid(row=2, column=0, sticky="nw", padx=(5, 1), pady=3)
        entry_thresh = ttk.Entry(frame_peakdet, width=5)
        entry_thresh.insert(0, "0.2")
        entry_thresh.grid(row=2, column=1, sticky="ne", padx=(1, 5), pady=3)

        label_dist = ttk.Label(frame_peakdet, text="Distance [0, inf): ")
        label_dist.grid(row=3, column=0, sticky="w", padx=(5, 1), pady=3)
        entry_dist = ttk.Entry(frame_peakdet, width=5)
        entry_dist.insert(0, "0")
        entry_dist.grid(row=3, column=1, sticky="e", padx=(1, 5), pady=3)

        check_autodetect = ttk.Checkbutton(
            frame_peakdet,
            text="Automatically detect opposite",
            variable=detect_opposite,
            onvalue=True,
            offvalue=False,
        )
        check_autodetect.grid(
            row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=3
        )

        button_runpointdet = ttk.Button(frame_peakdet, text="Run detection")
        button_runpointdet.grid(row=5, column=0, columnspan=2, padx=5, pady=3)

        # Frame for peak editing
        frame_editpoints = ttk.LabelFrame(left_column, text="Edit Points")
        frame_editpoints.grid(row=1, column=0, sticky="ew", padx=3, pady=5)

        radio_delpoints = ttk.Radiobutton(
            frame_editpoints, text="Delete points", variable=interaction, value=1
        )
        radio_delpoints.pack(anchor="w", padx=5, pady=3)
        radio_addpoints = ttk.Radiobutton(
            frame_editpoints, text="Add one point", variable=interaction, value=2
        )
        radio_addpoints.pack(anchor="w", padx=5, pady=3)
        radio_detpoints = ttk.Radiobutton(
            frame_editpoints,
            text="Multi-point estimation",
            variable=interaction,
            value=3,
        )
        radio_detpoints.pack(anchor="w", padx=5, pady=3)

        # Frame for realignment
        frame_movesignal = ttk.LabelFrame(left_column, text="Realign timeseries")
        frame_movesignal.grid(row=2, column=0, sticky="ew", padx=3, pady=5)

        radio_manualrealign = ttk.Radiobutton(
            frame_movesignal, text="Manual realignment", variable=interaction, value=4
        )
        radio_manualrealign.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=3
        )

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

        # Frame for plot interaction
        frame_plotinteraction = ttk.LabelFrame(left_column, text="Plot interaction")
        frame_plotinteraction.grid(row=3, column=0, sticky="ew", padx=3, pady=5)

        # radio_scroll = ttk.Radiobutton(
        #     frame_plotinteraction, text="Scroll", variable=interaction, value=8
        # )
        # radio_scroll.pack(padx=5, pady=3)
        # radio_zoom = ttk.Radiobutton(
        #     frame_plotinteraction, text="Zoom", variable=interaction, value=9
        # )
        # radio_zoom.pack(padx=5, pady=3)

        # Frame for artefact marking (what was peak "rejection")
        frame_markartefact = ttk.LabelFrame(left_column, text="Artefacts")
        frame_markartefact.grid(row=4, column=0, sticky="ew", padx=3, pady=5)

        radio_markartefact = ttk.Radiobutton(
            frame_markartefact, text="Mark Artefact", variable=interaction, value=5
        )
        radio_markartefact.pack(anchor="w", padx=5, pady=3)

        label_QA = ttk.Label(frame_markartefact, text="Annotations")
        label_QA.pack(padx=5, pady=(3, 1))
        text_QA = tk.Text(frame_markartefact, height=10, width=30)
        text_QA.pack(expand=True, fill=tk.BOTH)
        button_annotate = ttk.Button(frame_markartefact, text="Annotate")
        button_annotate.pack(padx=5, pady=3)

        # ######################## Right Frame ######################## #

        # ## Plots!
        right_column = ttk.Frame(master)
        right_column.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Get right_column dimensions to pass to plot_physiodata
        right_column.update_idletasks()  # Ensure geometry information is updated
        left_column.update_idletasks()  # Ensure geometry information is updated
        plot_height = right_column.winfo_height() / 100
        plot_width = (master.winfo_width() - left_column.winfo_width() - 10) / 100

        fig, axes = plot_physiodata(
            physio, fs=fs, height=plot_height, width=plot_width, show=False
        )
        canvas = FigureCanvasTkAgg(fig, master=right_column)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, frame_plotinteraction)
        toolbar.update()
        toolbar.pack(anchor="c", padx=5, pady=3)


def edit_physio(physio=None, fs=None):
    # Call window
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title(f"Peak Editor, prep4phys v{__version__}")
    new_physio = deepcopy(physio)
    _ = Window(root, new_physio, fs)
    root.mainloop()

    return new_physio


if __name__ == "__main__":
    import numpy as np

    physio = np.random.randn(300, 3)
    edit_physio(physio=physio, fs=100)
