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

        self.gridlines = []
        self.elements = []

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

    def add_row(self, r=1):
        self.rows += r
        self.draw_grid()

    def add_column(self, c=1):
        self.columns += c
        self.draw_grid()

    def del_row(self, r=1):
        if r >= self.rows:
            raise ValueError("Grid requires at least one row.")
        self.rows -= r
        self.draw_grid()

    def del_column(self, c=1):
        if c >= self.columns:
            raise ValueError("Grid requires at least one column.")
        self.columns -= c
        self.draw_grid()

    def add_element(self, element, x0, y0, x1=None, y1=None, padx=1, pady=1, alignment='nw'):
        if x1 is None:
            x1 = x0
        if y1 is None:
            y1 = y0
        if not (all(c in range(0, self.rows) for c in [y0, y1]) and all(c in range(0, self.columns) for c in [x0, x1])):
            raise KeyError("Not in grid.")
        if not ((x0 <= x1) and (y0 <= y1)):
            raise ValueError("Invalid key arguments.")
        new_element = {'element' : element,
                       'id' : element.winfo_id(),
                       'x0' : x0,
                       'y0' : y0,
                       'x1' : x1,
                       'y1' : y1,
                       'padx' : padx,
                       'pady' : pady,
                       'alignment' : alignment}
        self.elements.append(new_element) # TODO: Use a dictionary for easy reference when a user wants to edit an element
        self.draw_grid()

    def draw_grid(self, event=None):
        self.update_column_coords()
        self.update_row_coords()
        self.draw_gridlines()
        self.draw_elements()

    def draw_gridlines(self):
        for g in self.gridlines:
            self.delete(g)
        for r in self.row_coords:
            row = self.create_line(0, r, self.width, r, width=Grid.LINE_WIDTH, fill=self.line_color)
            self.gridlines.append(row)
        for c in self.column_coords:
            column = self.create_line(c, 0, c, self.height, width=Grid.LINE_WIDTH, fill=self.line_color)
            self.gridlines.append(column)

    def draw_elements(self):
        for e in self.elements:
            self.delete(e['id'])
        for e in self.elements:
            if type(e['element']) == type(tk.Label()):
                coords = self.calculate_element_coords(e)
                #print(f'x = {coords[0]}\ny = {coords[1]}')
                e['element'].place(x=coords[0]+e['padx'], y=coords[1]+e['pady'])

    def calculate_element_coords(self, e):
        row_coords = [0] + self.row_coords + [self.height]
        column_coords = [0] + self.column_coords + [self.width]
        row_height = row_coords[e['x0']+1] - row_coords[e['x0']]
        column_width = column_coords[e['y0']+1] - column_coords[e['y0']]
        w = e['element'].winfo_reqwidth()
        h = e['element'].winfo_reqheight()
        x_coords = [column_coords[e['x0']] + e['padx'], column_coords[e['x0']] + column_width/2 - w/2, column_coords[e['x0']+1] - e['padx']]
        y_coords = [row_coords[e['y0']] + e['pady'], row_coords[e['y0']] + row_height/2 - h/2, row_coords[e['y0']+1] - e['pady']]
        if e['alignment'] == 'nw':
            x = 0
            y = 0
        elif e['alignment'] == 'w':
            x = 0
            y = 1
        elif e['alignment'] == 'sw':
            x = 0
            y = 2
        elif e['alignment'] == 'n':
            x = 1
            y = 0
        elif e['alignment'] == 'c':
            x = 1
            y = 1
        elif e['alignment'] == 's':
            x = 1
            y = 2
        elif e['alignment'] == 'ne':
            x = 2
            y = 0
        elif e['alignment'] == 'e':
            x = 2
            y = 1
        elif e['alignment'] == 'se':
            x = 2
            y = 2
        else:
            raise ValueError("Invalid alignment")
        return [x_coords[x], y_coords[y]]

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
    grid.pack()

    label = tk.Label(grid, text="test")
    grid.add_element(label, x0=1, y0=1, alignment='c')

    b1 = tk.Button(root, text="Add Row", command=grid.add_row)
    b1.grid(row=0, column=0)
    b2 = tk.Button(root, text="Add Column", command=grid.add_column)
    b2.grid(row=0, column=1)
    b3 = tk.Button(root, text="Delete Row", command=grid.del_row)
    b3.grid(row=0, column=2)
    b4 = tk.Button(root, text="Delete Column", command=grid.del_column)
    b4.grid(row=0, column=3)

    root.mainloop()

def main():
    root = Schedule()
    root.mainloop()

if __name__ == '__main__':
    test()
    #main()