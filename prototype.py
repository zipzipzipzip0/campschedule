import tkinter as tk
import datetime as dt

class Grid(tk.Canvas):
    LINE_WIDTH = 2
    def __init__(self, parent, rows, columns, line_color='black', *args, **kwargs):
        # Initialize canvas
        super().__init__(parent, *args, **kwargs)
        
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.rows = rows
        self.row_coords = []
        self.locked_rows = []

        self.columns = columns
        self.column_coords = []
        self.locked_columns = []

        self.line_color = line_color

        self.bind('<Configure>', self.draw_grid)
    
    def update_row_coords(self):
        self.height = self.winfo_height()
        self.row_coords = []
        y0 = sum(self.locked_rows)
        for r in range(0, self.rows - 1):
            if r < len(self.locked_rows):
                self.row_coords.append(self.locked_rows[r])
            else:
                y = y0 + (r - len(self.locked_rows) + 1) * ((self.height - y0) / (self.rows - len(self.locked_rows)))
                self.row_coords.append(y)
    
    def update_column_coords(self):
        self.width = self.winfo_width()
        self.column_coords = []
        x0 = sum(self.locked_columns)
        for c in range(0, self.columns - 1):
            if c < len(self.locked_columns):
                self.column_coords.append(self.locked_columns[c])
            else:
                x = x0 + (c - len(self.locked_columns) + 1) * ((self.width - x0) / (self.columns - len(self.locked_columns)))
                self.column_coords.append(x)

    def lock_row(self, h, row=None):
        if (row is not None) and (row >= len(self.locked_rows)):
            raise KeyError
        elif (row is not None) and (row < len(self.locked_rows)):
            self.locked_rows[row] = h
        else:
            self.locked_rows.append(h)
        self.draw_grid()
    
    def lock_column(self, w, column=None):
        if (column is not None) and (column >= len(self.locked_columns)):
            raise KeyError
        elif (column is not None) and (column < len(self.locked_rows)):
            self.locked_columns[column] = w
        else:
            self.locked_columns.append(w)
        self.draw_grid()

    def unlock_row(self):
        if len(self.locked_rows) > 0:
            self.locked_rows.pop()
            self.draw_grid()

    def unlock_column(self):
        if len(self.locked_columns) > 0:
            self.locked_columns.pop()
            self.draw_grid()

    def draw_grid(self, event=None):
        self.update_column_coords()
        self.update_row_coords()
        for r in self.row_coords:
            self.create_line(0, r, self.width, r, width=Grid.LINE_WIDTH, fill=self.line_color)
        for c in self.column_coords:
            self.create_line(c, 0, c, self.height, width=Grid.LINE_WIDTH, fill=self.line_color)
class Schedule(tk.Tk):
    TITLE = 'Pool & Playground Schedule'
    FRAME_COLOR = 'lightblue'
    MARGIN_SIZE = 5
    def __init__(self):
        # Create root window
        super().__init__()
        self.title(Schedule.TITLE)

        # Window size
        self.state('zoomed')
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.bind('<Configure>', self.on_resize)

        # Create elements
        self.title = self.create_title()
        self.schedule = self.create_schedule()
        self.option_menu = self.create_option_menu()

        self.update_elements()

    def update_elements(self):
        # TODO: Once Grid class is implemented, use a custom grid to store window elements
        self.title.place(x=Schedule.MARGIN_SIZE, y=Schedule.MARGIN_SIZE, width=0.7 * (self.width - 2 * Schedule.MARGIN_SIZE), height=80)
    
    ### Title and date selector
    def create_title(self):
        frame = tk.Frame(self)
        frame.config(bg=Schedule.FRAME_COLOR)
        frame.config(width=0.7 * (self.width - 2 * Schedule.MARGIN_SIZE), height=80)

        title = tk.Label(frame, text=Schedule.TITLE, font=('Arial', 32))
        title.config(bg=Schedule.FRAME_COLOR)
        title.place(x=Schedule.MARGIN_SIZE, y=Schedule.MARGIN_SIZE)

        #TODO: Date selector

        return frame
    
    ### Grid containing camp names, times, and respective scheduled activities
    def create_schedule(self):
        START_TIME = dt.time(hour=9, minute=0) # 9:00 AM
        END_TIME = dt.time(hour=16, minute=0)  # 4:00 PM
        MINUTE_INTERVAL = dt.time(minute=15)   # 15 minutes
        # Camp names
        # Times
        # New camp button
        return
    
    ### Option menu with various settings
    def create_option_menu(self):
        # Visibility options
        # Secondary date selector
        # Save & print buttons
        return
    
    def on_resize(self, event):
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        #print(f'Window Dimensions: {self.width} x {self.height}')

def test():
    root = tk.Tk()
    root.geometry('400x400')

    frame = tk.Frame(root)
    frame.config(highlightbackground='black', highlightcolor='black', highlightthickness=2)
    frame.place(x=100, y=100, width=200, height=200)

    grid = Grid(frame, 5, 5)
    grid.lock_row(100)
    grid.pack()

    root.mainloop()

def main():
    root = Schedule()
    root.mainloop()

if __name__ == '__main__':
    test()
    #main()