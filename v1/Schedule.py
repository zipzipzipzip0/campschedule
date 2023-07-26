import tkinter as tk
import PySimpleGUI as sg

class Schedule:
    """
    The Schedule class handles creating a custom-formatted Grid object.
    The user may add Camps to the Schedule, populating the Grid with corresponding Rectangles.
    Alternatively, the user may select a start date and the Schedule will automatically populate
    the Grid with all of the Camps with the selected start date.

    The x-axis of the Grid represents time, with each column corresponding to a set interval.
    The leftmost x-coordinate cooresponds with the start of the day whereas the rightmost corresponds with the end.

    The y-axis of the Grid represents the camps, with each row corresponding to a camp during the selected week.
    Each camp's activities are represented with color-coded rectangles that align with their respective times.
    """

    def __init__(self):
        """
        The Schedule must be initialized with a start time, end time, and minute interval.
        """
        raise NotImplementedError