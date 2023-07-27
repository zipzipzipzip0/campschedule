import tkinter as tk
import PySimpleGUI as sg
from ScheduleWindow import ScheduleWindow

def main():
    sg.theme('DarkGrey')

    w = ScheduleWindow()
    layout = w.get_layout()

    window = sg.Window("Schedule", layout, resizable=True, finalize=True)
    window.maximize()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Maximize":
            window.maximize()
        elif event == "Restore":
            window.normal()

    window.close()

if __name__ == '__main__':
    main()