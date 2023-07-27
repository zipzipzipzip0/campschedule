import tkinter as tk
import PySimpleGUI as sg

class ScheduleWindow:
    """
    The ScheduleWindow class creates a layout that can be used to create a window.
    The layout consists of a menu bar, a large title, and a formatted grid.
    """
    def __init__(self):
        self.menubar = self.__create_menubar()
        self.title = self.__create_title()
        self.grid = self.__create_grid()
        self.layout = [
            [self.menubar],
            [sg.Column([
                [self.title],
                [self.grid]
            ], element_justification='center', vertical_alignment='center', expand_x=True, expand_y=True)]
        ]
    
    def get_layout(self):
        """
        Returns the layout created upon initialization.
        """
        return self.layout
    
    def __create_menubar(self):
        """
        **The menubar may need to call methods from a helper class.
        """
        menu_layout = [
            ['&File', ['&Open', '&Save', 'E&xit']],
        ]
        return sg.MenuBar(menu_layout)
    
    def __create_title(self):
        font = ("72", 36, "bold")
        text = sg.Text("ACTIVITY SCHEDULE", font=font)
        date = sg.Text("7/31/23 - 8/4/23", font=font)
        title = sg.Column([
            [text, sg.Stretch(), date]
        ], expand_x=True)
        return title
    
    def __create_grid(self):
        """
        Calls upon the Schedule class to generate a custom-formatted instance of the Grid class.
        """
        frame_layout = [
            [sg.Frame('', [[sg.Canvas(size=(100, 100), background_color='lightgray', key='-CANVAS-', expand_x=True, expand_y=True)]],
                      background_color='black', relief=sg.RELIEF_FLAT, pad=(10, 10), expand_x=True, expand_y=True)]
        ]
        
        return sg.Frame("Schedule", frame_layout, expand_x=True, expand_y=True)