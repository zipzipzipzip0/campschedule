import tkinter as tk

class Grid(tk.Canvas):
    """
    The Grid class is an extension of the tkinter Canvas widget with the following properties:
    - Upon initialization, the Grid will draw gridlines to the canvas corresponding with the specified number of rows and columns.
    - Inner classes represent different items such as labels and shapes that may be added to the Grid.
    - Items added to the grid are done so using grid coordinates rather than pixel coordinates.
    - Items on the grid are stored in an internal two-dimensional matrix of lists where each list represents the contents of its respective cell.
    - Rows and columns may be added to and deleted from the grid, causing the pre-existing contents to shift accordingly.
    """
    
    ### Inner Classes ###
    class __Cell:
        """
        The Cell class is used to represent a cell in the parent Grid.
        A Cell instance contains its grid coordinates as its contents.
        Methods are provided for calculating the pixel coordinates of the Cell's boundaries based on the parent Grid's line width.
        """

        def __init__(self, x, y, contents=[]):
            """
            The Cell must be initialized using grid coordinates.
            Any contents of the cell declared upon initialization must be in a list.
            """
            self.x, self.y = x, y # TODO: Add a check to make sure that the coordinates are valid.
            if type(contents) == type([]):
                self.contents = contents
            else:
                raise TypeError("Contents declared upon initialization must be in a list.")
        
        def loc(self, pos):
            """
            Returns the pixel coordinate of the specified position, which can be any of the following:
            - 'north', 'east', 'south', 'west': Return the pixel coordinate of the edge of white space within the Cell.
            - 'center': Return the pixel x, y coordinates of the center of white space within the Cell.
            """
            raise NotImplementedError

        def add_item(self, item):
            self.contents.append(item)

        def del_item(self, item):
            raise NotImplementedError

    class __Rectangle:
        """
        The Rectangle class handles a rectangle on the Grid with the following properties:
        - The Rectangle's coordinates always align with the parent Grid's gridlines.
        - The Rectangle can be moved and resized via user interaction with the mouse.
        - The Rectangle can be attached to another Rectangle
        """

        def __init__(self, x0, y0, x1, y1, outline='black', width=0, **kwargs):
            raise NotImplementedError
        
        def coords(self, x0, y0, x1, y1):
            raise NotImplementedError
        
        def select(self, event):
            raise NotImplementedError
        
        def drag(self, event):
            raise NotImplementedError
        
    class __Label:
        """
        The Label class handles a label on the Grid with the following properties:
        - The Label can be moved via user interaction with the mouse.
        - The Label's alignment within its current grid cell can be adjusted.
        """

        def __init__(self, x, y, text, *args, **kwargs):
            return

    ## Constructor ##
    def __init__(self, parent, rows, columns, line_color='black', *args, **kwargs):
        self.rows = rows
        self.columns = columns
        return
    
    ## Getter/Setter Methods ##
    
    ## Drawing ##
    def draw(self):
        """
        Draw the gridlines, shapes, and labels onto the canvas by calling helper methods.
        """
        raise NotImplementedError
    
    def __draw_grid(self):
        """
        Draw the gridlines and grid border.
        """
        raise NotImplementedError
    
    def __draw_shapes(self):
        """
        Draw the shapes in each cell.
        """
        raise NotImplementedError
    
    def __draw_labels(self):
        raise NotImplementedError
    
    def __update_internal(self):
        raise NotImplementedError