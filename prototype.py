import tkinter as tk
import datetime as dt

class Rectangle:
    EDGE_WIDTH = 10

    def __init__(self, canvas, x0, y0, x1, y1, outline='black', width=0, **kwargs):
        self.canvas = canvas
        self.snappy = False
        if type(self.canvas) == Grid:
            self.snappy = True
        self.id = None
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.outline = outline
        self.width = width
        self.kwargs = kwargs

        self.components = {}

        self.create_base()
        self.setup_binds()
    
    def get_id(self):
        return self.id
    
    def get_coords(self):
        return self.x0, self.y0, self.x1, self.y1

    def create_base(self):
        self.id = self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline=self.outline, width=self.width, **self.kwargs)

    def setup_binds(self):
        self.canvas.tag_bind(self.id, '<Button 1>', self.select)
        if self.snappy:
            self.canvas.tag_bind(self.id, '<B1-Motion>', self.snappy_drag)
        else:
            self.canvas.tag_bind(self.id, '<B1-Motion>', self.drag)
        self.canvas.tag_bind(self.id, '<Motion>', self.hover_cursor)
        self.canvas.tag_bind(self.id, '<Leave>', lambda event: self.canvas.winfo_toplevel().config(cursor=''))

    def hover_cursor(self, event=None, selected=None):
        if event is not None:
            selected = self.get_edge(event)
        # North & South
        if (selected & (1 << 3)) or (selected & (1 << 1)):
            self.canvas.winfo_toplevel().config(cursor='sb_v_double_arrow')
        # East & West
        if (selected & (1 << 2)) or (selected & (1 << 0)):
            self.canvas.winfo_toplevel().config(cursor='sb_h_double_arrow')
        # NW & SE
        if ((selected & (1 << 3)) and (selected & (1 << 0))) or ((selected & (1 << 1)) and (selected & (1 << 2))):
            self.canvas.winfo_toplevel().config(cursor='size_nw_se')
        # NE & SW
        if ((selected & (1 << 3)) and (selected & (1 << 2))) or ((selected & (1 << 1)) and (selected & (1 << 0))):
            self.canvas.winfo_toplevel().config(cursor='size_ne_sw')
        # Center
        if (selected == 0b0000):
            self.canvas.winfo_toplevel().config(cursor='fleur')

    def leave_cursor(self, event):
        if (event.x < self.x0) or (event.x > self.x1) or (event.y < self.y0) or (event.y > self.y1):
            self.canvas.winfo_toplevel().config(cursor='')

    def get_edge(self, event):
        b = 0b0000
        # North
        if (event.y <= self.y0+Rectangle.EDGE_WIDTH):
            b += 8
        # East
        if (self.x1-Rectangle.EDGE_WIDTH <= event.x):
            b += 4
        # South
        if (self.y1-Rectangle.EDGE_WIDTH <= event.y):
            b += 2
        # West
        if (event.x <= self.x0+Rectangle.EDGE_WIDTH):
            b += 1
        return b
    
    def coords(self, x0, y0, x1, y1):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.canvas.coords(self.id, x0, y0, x1, y1)

    def update_component(self, component, x0=None, y0=None, x1=None, y1=None):
        for key, coord in {'x0':x0, 'y0':y0, 'x1':x1, 'y1':y1}.items():
            if coord is not None:
                self.components[component][key] = coord

    def select(self, event):
        global selected, start_x, start_y, shape, initial_coords
        selected = self.get_edge(event)
        initial_coords = {}
        if self.snappy:
            start_x, start_y = self.canvas.grid_coord(event)
            shape = self.canvas.get_shape(self).copy()
            for c, s in self.components.items():
                initial_coords[c] = {'position':s['position'],
                                     'x0':s['x0'],
                                     'y0':s['y0'],
                                     'x1':s['x1'],
                                     'y1':s['y1']}
        else:
            start_x, start_y = event.x, event.y
            # TODO: Either make Rectangle only snappy or fix logic for non-snappy
            initial_coords = {'x0':self.x0,
                                'y0':self.y0,
                                'x1':self.x1,
                                'y1':self.y1}
        

    def drag(self, event):
        global selected, start_x, start_y, initial_coords
        dx = event.x - start_x
        dy = event.y - start_y
        self.cursor(selected=selected)
        # North
        if (selected & (1 << 3)) and (initial_coords['y0'] + dy <= initial_coords['y1'] - (3 * Rectangle.EDGE_WIDTH)):
            self.y0 = initial_coords['y0'] + dy
        # East
        if (selected & (1 << 2)) and (initial_coords['x1'] + dx >= initial_coords['x0'] + (3 * Rectangle.EDGE_WIDTH)):
            self.x1 = initial_coords['x1'] + dx
        # South
        if (selected & (1 << 1)) and (initial_coords['y1'] + dy >= initial_coords['y0'] + (3 * Rectangle.EDGE_WIDTH)):
            self.y1 = initial_coords['y1'] + dy
        # West
        if (selected & (1 << 0)) and (initial_coords['x0'] + dx <= initial_coords['x1'] - (3 * Rectangle.EDGE_WIDTH)):
            self.x0 = initial_coords['x0'] + dx
        # Center
        if (selected == 0b0000):
            self.x0 = initial_coords['x0'] + dx
            self.y0 = initial_coords['y0'] + dy
            self.x1 = initial_coords['x1'] + dx
            self.y1 = initial_coords['y1'] + dy
        
        self.coords(self.x0, self.y0, self.x1, self.y1)
    
    def snappy_drag(self, event):
        global selected, start_x, start_y, initial_coords
        x, y = self.canvas.grid_coord(event)
        dx = x - start_x
        dy = y - start_y
        self.hover_cursor(selected=selected)

        bump_north = shape['y0'] + dy < 0
        bump_east = shape['x1'] + dx >= self.canvas.columns
        bump_south = shape['y1'] + dy >= self.canvas.rows
        bump_west = shape['x0'] + dx < 0
        for c, s in initial_coords.items():
            if (s['y0'] + dy < 0):
                bump_north = True
            if (s['x1'] + dx >= self.canvas.columns):
                bump_east = True
            if (s['y1'] + dy >= self.canvas.rows):
                bump_south = True
            if (s['x0'] + dx < 0):
                bump_west = True

        # North
        if (selected & (1 << 3)) and (shape['y0'] + dy <= shape['y1']) and not bump_north:
            self.canvas.set_shape_coords(self, y0=shape['y0']+dy)
            for c, s in initial_coords.items():
                if s['position'] == 'north':
                    c.canvas.set_shape_coords(c, y0=initial_coords[c]['y0']+dy, y1=initial_coords[c]['y1']+dy)
                    self.components[c]['y0'] = initial_coords[c]['y0'] + dy
                    self.components[c]['y1'] = initial_coords[c]['y1'] + dy
                c.update_component(component=self, y0=shape['y0']+dy)

        # East
        if (selected & (1 << 2)) and (shape['x1'] + dx >= shape['x0']) and not bump_east:
            self.canvas.set_shape_coords(self, x1=shape['x1']+dx)
            for c, s in initial_coords.items():
                if s['position'] == 'east':
                    c.canvas.set_shape_coords(c, x0=initial_coords[c]['x0']+dx, x1=initial_coords[c]['x1']+dx)
                    self.components[c]['x0'] = initial_coords[c]['x0'] + dx
                    self.components[c]['x1'] = initial_coords[c]['x1'] + dx
                c.update_component(component=self, x1=shape['x1']+dx)
        # South
        if (selected & (1 << 1)) and (shape['y1'] + dy >= shape['y0']) and not bump_south:
            self.canvas.set_shape_coords(self, y1=shape['y1']+dy)
            for c, s in initial_coords.items():
                if s['position'] == 'south':
                    c.canvas.set_shape_coords(c, y0=initial_coords[c]['y0']+dy, y1=initial_coords[c]['y1']+dy)
                    self.components[c]['y0'] = initial_coords[c]['y0'] + dy
                    self.components[c]['y1'] = initial_coords[c]['y1'] + dy
                c.update_component(component=self, y1=shape['y1']+dy)
        # West
        if (selected & (1 << 0)) and (shape['x0'] + dx <= shape['x1']) and not bump_west:
            self.canvas.set_shape_coords(self, x0=shape['x0']+dx)
            for c, s in initial_coords.items():
                if s['position'] == 'west':
                    c.canvas.set_shape_coords(c, x0=initial_coords[c]['x0']+dx, x1=initial_coords[c]['x1']+dx)
                    self.components[c]['x0'] = initial_coords[c]['x0'] + dx
                    self.components[c]['x1'] = initial_coords[c]['x1'] + dx
                c.update_component(component=self, x0=shape['x0']+dx)
        # Center
        if (selected == 0b0000):
            if not (bump_north or bump_south):
                self.canvas.set_shape_coords(self, y0=shape['y0']+dy, y1=shape['y1']+dy)
                for c, s in initial_coords.items():
                    c.canvas.set_shape_coords(c, y0=initial_coords[c]['y0']+dy, y1=initial_coords[c]['y1']+dy)
                    self.components[c]['y0'] = initial_coords[c]['y0'] + dy
                    self.components[c]['y1'] = initial_coords[c]['y1'] + dy
                    c.update_component(component=self, y0=shape['y0']+dy)
                    c.update_component(component=self, y1=shape['y1']+dy)
            if not (bump_east or bump_west):
                self.canvas.set_shape_coords(self, x0=shape['x0']+dx, x1=shape['x1']+dx)
                for c, s in initial_coords.items():
                    c.canvas.set_shape_coords(c, x0=initial_coords[c]['x0']+dx, x1=initial_coords[c]['x1']+dx)
                    self.components[c]['x0'] = initial_coords[c]['x0'] + dx
                    self.components[c]['x1'] = initial_coords[c]['x1'] + dx
                    c.update_component(component=self, x0=shape['x0']+dx)
                    c.update_component(component=self, x1=shape['x1']+dx)

        self.x0, self.y0, self.x1, self.y1 = self.canvas.calculate_shape_coords(shape)
        for c, s in self.components.items():
            x0, y0, x1, y1 = c.canvas.calculate_shape_coords(s)
            c.coords(x0, y0, x1, y1)
        self.canvas.draw_grid()

    def attach(self, other, is_prime=True):
        a = self.canvas.get_shape(self).copy()
        b = self.canvas.get_shape(other).copy()

        position = None
        # North
        if (a['y0']-1 == b['y1']) and ((a['x0']-1 < b['x1']) or (a['x1'] > b['x0']-1)):
            position = 'north'
        # East
        elif (a['x1'] == b['x0']-1) and ((a['y0']-1 < b['y1']) or (a['y1'] > b['y0']-1)):
            position = 'east'
        # South
        elif (a['y1'] == b['y0']-1) and ((a['x0']-1 < b['x1']) or (a['x1'] > b['x0']-1)):
            position = 'south'
        # West
        elif (a['x0']-1 == b['x1']) and ((a['y0']-1 < b['y1']) or (a['y1'] > b['y0']-1)):
            position = 'west'
        else:
            raise IndexError("Invalid attach target.")
        
        self.components[other] = {'position':position,
                                  'x0':b['x0'],
                                  'y0':b['y0'],
                                  'x1':b['x1'],
                                  'y1':b['y1']}
        print(f'{a}\n{b}')
        print(position)

        if is_prime:
            other.attach(self, is_prime=False)

class Grid(tk.Canvas):
    """
    A custom tkinter Canvas widget that displays a grid with elements and shapes.

    Parameters:
        parent (tk.Tk or tk.Toplevel): The parent widget.
        rows (int): The number of rows in the grid.
        columns (int): The number of columns in the grid.
        line_color (str, optional): The color of the gridlines. Default is 'black'.
        *args: Additional arguments to be passed to the superclass (tk.Canvas).
        **kwargs: Additional keyword arguments to be passed to the superclass (tk.Canvas).

    Author:
        Aidan Stawasz
    """
    ### Constants ###
    LINE_WIDTH = 2

    ### Constructor ###
    def __init__(self, parent, rows, columns, line_color='black', *args, **kwargs):
        """
        Initialize the Grid widget.

        Parameters:
            parent (tk.Tk or tk.Toplevel): The parent widget.
            rows (int): The number of rows in the grid.
            columns (int): The number of columns in the grid.
            line_color (str, optional): The color of the gridlines. Default is 'black'.
            *args: Additional arguments to be passed to the superclass (tk.Canvas).
            **kwargs: Additional keyword arguments to be passed to the superclass (tk.Canvas).
        """
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
        self.elements = {}
        self.shapes = {}

        self.line_color = line_color

        self.bind('<Configure>', self.draw_grid)
    
    ### Getter/Setter methods ##
    def rows(self):
        return self.rows
    
    def columns(self):
        return self.columns

    def get_gridline_coords(self):
        return self.row_coords, self.column_coords

    def get_shape(self, shape):
        return self.shapes[shape]
    
    def set_shape_coords(self, shape, x0=None, y0=None, x1=None, y1=None):
        if x0 is not None:
            self.shapes[shape]['x0'] = x0
        if y0 is not None:
            self.shapes[shape]['y0'] = y0
        if x1 is not None:
            self.shapes[shape]['x1'] = x1
        if y1 is not None:
            self.shapes[shape]['y1'] = y1

    ### Draw the grid ###
    def draw_grid(self, event=None):
        """
        Redraw the grid, gridlines, elements, and shapes when the canvas is resized.

        Parameters:
            event (tk.Event, optional): The event that triggered the grid redraw. Default is None.
        """
        self.update_column_coords()
        self.update_row_coords()
        self.draw_gridlines()
        #print("Gridlines:\t", self.find_all())
        self.draw_elements()
        #print("Elements:\t", self.find_all())
        self.draw_shapes()
        #print("Shapes:\t\t", self.find_all())

    def draw_gridlines(self):
        """
        Draw the gridlines and border of the grid.
        """
        for g in self.gridlines:
            self.delete(g)
        for r in self.row_coords:
            row = self.create_line(0, r, self.width, r, width=Grid.LINE_WIDTH, fill=self.line_color)
            self.gridlines.append(row)
        for c in self.column_coords:
            column = self.create_line(c, 0, c, self.height, width=Grid.LINE_WIDTH, fill=self.line_color)
            self.gridlines.append(column)
        cb = 1 + Grid.LINE_WIDTH
        border = self.create_rectangle(cb, cb, self.width-cb, self.height-cb, outline=self.line_color, width=Grid.LINE_WIDTH)
        self.gridlines.append(border)

    def draw_elements(self):
        """
        Draw the elements in the grid at their respective positions.
        """
        for e in self.elements.values():
            self.delete(e['id'])
        for e in self.elements.values():
            if type(e['element']) == type(tk.Label()):
                x, y = self.calculate_element_coords(e)
                #print(f'x = {coords[0]}\ny = {coords[1]}')
                e['element'].place(x=x, y=y)

    def draw_shapes(self):
        """
        Draw the shapes on the grid.
        """
        # No need to delete/remake old shapes, just resize them
        for key, s in self.shapes.items():
            x0, y0, x1, y1 = self.calculate_shape_coords(s)
            #self.coords(key, x0, y0, x1, y1)
            key.coords(x0, y0, x1, y1)

    ### Calculating coordinates ###
    def update_row_coords(self):
        """
        Update the y-coordinates of the rows in the grid.
        """
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
        """
        Update the x-coordinates of the columns in the grid.
        """
        self.width = self.winfo_width()
        self.column_coords = []
        x0 = sum(self.locked_columns)
        for c in range(0, self.columns - 1):
            if c < len(self.locked_columns):
                self.column_coords.append(self.locked_columns[c])
            else:
                x = x0 + (c - len(self.locked_columns) + 1) * ((self.width - x0) / (self.columns - len(self.locked_columns)))
                self.column_coords.append(x)

    def calculate_element_coords(self, e):
        """
        Calculate the coordinates for placing an element within a grid cell.

        Parameters:
            e (dict): A dictionary representing the element and its properties.

        Returns:
            tuple: The x and y coordinates for placing the element on the canvas.
        """
        row_coords = [0] + self.row_coords + [self.height]
        column_coords = [0] + self.column_coords + [self.width]
        row_height = row_coords[e['x']+1] - row_coords[e['x']]
        column_width = column_coords[e['y']+1] - column_coords[e['y']]
        w = e['element'].winfo_reqwidth()
        h = e['element'].winfo_reqheight()
        x_coords = [column_coords[e['x']] + e['padx'], column_coords[e['x']] + column_width/2 - w/2, column_coords[e['x']+1] - e['padx']]
        y_coords = [row_coords[e['y']] + e['pady'], row_coords[e['y']] + row_height/2 - h/2, row_coords[e['y']+1] - e['pady']]
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
        return x_coords[x], y_coords[y]

    def calculate_shape_coords(self, s):
        """
        Calculate the coordinates for drawing a shape within the grid.

        Parameters:
            s (dict): A dictionary representing the shape and its properties.

        Returns:
            tuple: The x and y coordinates of the shape's top-left and bottom-right corners.
        """
        row_coords = [0] + self.row_coords + [self.height]
        column_coords = [0] + self.column_coords + [self.width]
        x0 = column_coords[s['x0']]
        y0 = row_coords[s['y0']]
        x1 = column_coords[s['x1']+1]
        y1 = row_coords[s['y1']+1]
        #print(x0, y0, x1, y1)
        return x0, y0, x1, y1

    ### Adding to the grid ###
    def add_row(self, r=1):
        """
        Add rows to the grid.

        Parameters:
            r (int, optional): The number of rows to add. Default is 1.
        """
        self.rows += r
        self.draw_grid()

    def add_column(self, c=1):
        """
        Add columns to the grid.

        Parameters:
            c (int, optional): The number of columns to add. Default is 1.
        """
        self.columns += c
        self.draw_grid()

    def add_element(self, element, x, y, padx=1, pady=1, alignment='nw'):
        """
        Add an element to the grid.

        Parameters:
            element (tk.Widget): The tkinter widget to be added.
            x (int): The column index for placing the element.
            y (int): The row index for placing the element.
            padx (int, optional): The horizontal padding around the element. Default is 1.
            pady (int, optional): The vertical padding around the element. Default is 1.
            alignment (str, optional): The alignment of the element within its cell. Default is 'nw'.

        Raises:
            KeyError: If the specified row or column index is outside the grid boundaries.
        """
        if not ((x in range(0, self.columns)) and (y in range(0, self.rows))):
            raise KeyError("Not in grid.")
        new_element = {'element' : element,
                       'id' : element.winfo_id(),
                       'x' : x,
                       'y' : y,
                       'padx' : padx,
                       'pady' : pady,
                       'alignment' : alignment}
        #self.elements.append(new_element) # TODO: Use a dictionary for easy reference when a user wants to edit an element
        self.elements[element] = new_element
        self.draw_grid()

    def add_shape(self, shape, x0, y0, x1=None, y1=None, fill='gray', outline=('black', 0)):
        """
        Add a shape to the grid.

        Parameters:
            shape (str): The type of shape to add (currently supports 'rectangle').
            x0 (int): The column index of the top-left corner of the shape.
            y0 (int): The row index of the top-left corner of the shape.
            x1 (int, optional): The column index of the bottom-right corner of the shape. Default is None (for single-cell shapes).
            y1 (int, optional): The row index of the bottom-right corner of the shape. Default is None (for single-cell shapes).
            fill (str, optional): The fill color of the shape. Default is 'gray'.
            outline (tuple, optional): The outline color and width of the shape. Default is ('black', 2).

        Raises:
            KeyError: If the specified row or column index is outside the grid boundaries.
            ValueError: If the coordinates of the shape are invalid.
        """
        if x1 is None:
            x1 = x0
        if y1 is None:
            y1 = y0
        if not (all(c in range(0, self.rows) for c in [y0, y1]) and all(c in range(0, self.columns) for c in [x0, x1])):
            raise KeyError("Not in grid.")
        if not ((x0 <= x1) and (y0 <= y1)):
            raise ValueError("Invalid key arguments.")
        
        s = None
        if shape == 'rectangle':
            #s = self.create_rectangle(0, 0, 0, 0, fill=fill, outline=outline[0], width=outline[1])
            s = Rectangle(self, 0, 0, 0, 0, fill=fill, outline=outline[0], width=outline[1])
        else:
            raise TypeError("Invalid shape.")
        self.shapes[s] = {'shape' : shape,
                          'x0' : x0,
                          'y0' : y0,
                          'x1' : x1,
                          'y1' : y1}
        #self.bind_shape(s)
        #print(self.shapes)
        self.draw_grid()
        return s

    ### Binds for user interaction ###
    def bind_element(self, element):
        raise NotImplementedError
    
    def bind_shape(self, shape):
        self.tag_bind(shape, '<Button 1>', self.select)
        self.tag_bind(shape, '<B1-Motion>', self.drag)

    ### Deleting from the grid ###
    def del_row(self, r=1):
        """
        Delete rows from the grid.

        Parameters:
            r (int, optional): The number of rows to delete. Default is 1.

        Raises:
            ValueError: If the number of rows to delete is greater than the current number of rows.
        """
        if r >= self.rows:
            raise ValueError("Grid requires at least one row.")
        self.rows -= r
        self.draw_grid()

    def del_column(self, c=1):
        """
        Delete columns from the grid.

        Parameters:
            c (int, optional): The number of columns to delete. Default is 1.

        Raises:
            ValueError: If the number of columns to delete is greater than the current number of columns.
        """
        if c >= self.columns:
            raise ValueError("Grid requires at least one column.")
        self.columns -= c
        self.draw_grid()

    def del_element(self): # TODO: Implement
        """
        Delete an element from the grid.

        Note: This method is intended to be implemented by the developer as it requires specific logic based on the application.

        Raises:
            NotImplementedError: If the method is not overridden.
        """
        raise NotImplementedError("Method 'del_element' must be implemented in a subclass.")
    
    def del_shape(self): # TODO: Implement
        """
        Delete a shape from the grid.

        Note: This method is intended to be implemented by the developer as it requires specific logic based on the application.

        Raises:
            NotImplementedError: If the method is not overridden.
        """
        raise NotImplementedError("Method 'del_shape' must be implemented in a subclass.")

    ### Locking/unlocking rows & columns ###
    def lock_row(self, h, row=None):
        """
        Lock a row in the grid to a specific height.

        Parameters:
            h (int): The height (in pixels) to which the row should be locked.
            row (int, optional): The row index to lock. If not provided, a new locked row will be added to the grid.

        Raises:
            KeyError: If the specified row index is outside the grid boundaries.
        """
        if (row is not None) and (row >= len(self.locked_rows)):
            raise KeyError
        elif (row is not None) and (row < len(self.locked_rows)):
            self.locked_rows[row] = h
        else:
            self.locked_rows.append(h)
        self.draw_grid()
    
    def lock_column(self, w, column=None):
        """
        Lock a column in the grid to a specific width.

        Parameters:
            w (int): The width (in pixels) to which the column should be locked.
            column (int, optional): The column index to lock. If not provided, a new locked column will be added to the grid.

        Raises:
            KeyError: If the specified column index is outside the grid boundaries.
        """
        if (column is not None) and (column >= len(self.locked_columns)):
            raise KeyError
        elif (column is not None) and (column < len(self.locked_rows)):
            self.locked_columns[column] = w
        else:
            self.locked_columns.append(w)
        self.draw_grid()

    def unlock_row(self):
        """
        Unlock the last locked row in the grid.
        """
        if len(self.locked_rows) > 0:
            self.locked_rows.pop()
            self.draw_grid()

    def unlock_column(self):
        """
        Unlock the last locked column in the grid.
        """
        if len(self.locked_columns) > 0:
            self.locked_columns.pop()
            self.draw_grid()

    ### Moving within the grid ###
    def grid_coord(self, event=None, x=None, y=None):
        row_coords = [0] + self.row_coords + [self.height]
        column_coords = [0] + self.column_coords + [self.width]

        if event is not None:
            x, y = event.x, event.y
        
        gx = 0
        while (gx < self.columns) and (x > column_coords[gx+1]):
            gx += 1
        gy = 0
        while (gy < self.rows) and (y > row_coords[gy+1]):
            gy += 1
        #print(x, y)
        return gx, gy

    # def select(self, event):
    #     global selected, initial_coords, start_x, start_y
    #     selected = event.widget.find_closest(event.x, event.y)[0]
    #     initial_coords = self.shapes[selected].copy()
    #     start_x, start_y = self.grid_coord(event)
    #     #print(initial_coords)
    #     #print(self.shapes[selected])

    # def drag(self, event):
    #     global selected, initial_coords, start_x, start_y
    #     x, y = self.grid_coord(event)
    #     dx = x - start_x
    #     dy = y - start_y
        
    #     bump_left = initial_coords['x0'] + dx < 0
    #     bump_right = initial_coords['x1'] + dx >= self.columns
    #     bump_top = initial_coords['y0'] + dy < 0
    #     bump_bottom = initial_coords['y1'] + dy >= self.rows

    #     if not (bump_left or bump_right):
    #         self.shapes[selected]['x0'] = initial_coords['x0'] + dx
    #         self.shapes[selected]['x1'] = initial_coords['x1'] + dx
    #     if not (bump_top or bump_bottom):
    #         self.shapes[selected]['y0'] = initial_coords['y0'] + dy
    #         self.shapes[selected]['y1'] = initial_coords['y1'] + dy

    #     # if bump_left:
    #     #     print(f"bump left!\tx0: {self.shapes[selected]['x0']}\tx0+dx: {initial_coords['x0'] + dx}")
    #     # if bump_right:
    #     #     print(f"bump right!\tx1: {self.shapes[selected]['x1']}\tx1+dx: {initial_coords['x1'] + dx}")
    #     # if bump_top:
    #     #     print(f"bump top!\ty0: {self.shapes[selected]['y0']}\ty0+dy: {initial_coords['y0'] + dy}")
    #     # if bump_bottom:
    #     #     print(f"bump bottom!\ty1: {self.shapes[selected]['y1']}\ty1+dy: {initial_coords['y1'] + dy}")
    #     self.draw_shapes()

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

def test_rectangle():
    root = tk.Tk()
    root.geometry('400x400')

    frame = tk.Frame(root)
    frame.config(highlightbackground='black', highlightcolor='black', highlightthickness=2)
    frame.place(x=75, y=75, width=250, height=250)

    canvas = tk.Canvas(frame)
    canvas.pack()

    rect = Rectangle(canvas, 85, 85, 165, 165, fill='pink')
    
    root.mainloop()

def test_grid():
    root = tk.Tk()
    root.geometry('400x400')

    frame = tk.Frame(root)
    frame.config(highlightbackground='black', highlightcolor='black', highlightthickness=2)
    frame.place(x=75, y=75, width=250, height=250)

    grid = Grid(frame, 7, 7)
    grid.pack()

    # print("Making Label...")
    # label = tk.Label(grid, text="test")
    # grid.add_element(label, 1, 1, alignment='c')

    print("Making Rectangle...")
    rect1 = grid.add_shape('rectangle', 1, 1, 2, 3, fill='cornflower blue')
    rect2 = grid.add_shape('rectangle', 3, 1, 5, 2, fill='coral')

    #rect1.attach(rect2)

    b1 = tk.Button(root, text="Add Row", command=grid.add_row)
    b1.grid(row=0, column=0)
    b2 = tk.Button(root, text="Add Column", command=grid.add_column)
    b2.grid(row=0, column=1)
    b3 = tk.Button(root, text="Delete Row", command=grid.del_row)
    b3.grid(row=0, column=2)
    b4 = tk.Button(root, text="Delete Column", command=grid.del_column)
    b4.grid(row=0, column=3)

    b5 = tk.Button(root, text="Attach", command=lambda:rect1.attach(rect2))
    b5.grid(row=0, column=4)

    root.mainloop()

def main():
    root = Schedule()
    root.mainloop()

if __name__ == '__main__':
    #test_rectangle()
    test_grid()
    #main()