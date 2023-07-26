import PySimpleGUI as sg
from ScheduleWindow import ScheduleWindow

def test1():
    # w = ScheduleWindow()
    # layout = w.get_layout()
    layout = [[sg.Text(text="Hello World")]]

    window = sg.Window("Schedule", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

    window.close()

if __name__ == '__main__':
    test1()