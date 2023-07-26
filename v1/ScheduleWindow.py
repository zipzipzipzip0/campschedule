import tkinter as tk
import PySimpleGUI as sg

class ScheduleWindow:
    """
    The ScheduleWindow class creates a layout that can be used to create a window.
    The layout consists of a menu bar, a large title, and a formatted grid.
    """
    def __init__(self):
        raise NotImplementedError
    
    def get_layout(self):
        """
        Return a layout that can be used to make a window. Calls helper methods for each window element.
        """
        raise NotImplementedError
    
    def __create_menubar(self):
        """
        **The menubar may need to call methods from a helper class.
        """
        raise NotImplementedError
    
    def __create_title(self):
        raise NotImplementedError
    
    def __create_grid(self):
        """
        Calls upon the Schedule class to generate a custom-formatted instance of the Grid class.
        """
        raise NotImplementedError