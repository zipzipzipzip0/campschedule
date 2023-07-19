import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

class Block:
    ### Constants
    EDGE_SIZE = 2
    EDGE_FILL = 'black'
    CIRCLE_RADIUS = 5
    CIRCLE_FILL = 'gray'

    ### Constructor
    def __init__(self, x0, y0, x1, y1, fill='blue', draggable=True, resizable=True):
        # Dictionary stores component id:coord pairs
        self.components = {}

        # List stores only ids of edges for edge calculations
        self.edges = [None] * 4

        coords = [x0, y0, x1, y1]
        self.base = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=fill)
        canvas.tag_bind(self.base, '<Button 1>', self.select)
        canvas.tag_bind(self.base, '<B1-Motion>', self.drag)
        canvas.tag_bind(self.base, '<ButtonRelease-1>', self.deselect)

        self.components[self.base] = coords
        self.center = [canvas.coords(self.base)[0] + (canvas.coords(self.base)[2] - canvas.coords(self.base)[0]) / 2, canvas.coords(self.base)[1] + (canvas.coords(self.base)[3] - canvas.coords(self.base)[1]) / 2]

        # # Handle draggable
        # if draggable:
        #     self.circ = self.create_drag()

        # Handle resizable
        if resizable:
            self.create_resize()
        
    # def update_params(self):
    #     self.center = canvas.coords(self.base)
    #     self.center = [canvas.coords(self.base)[0] + (canvas.coords(self.base)[2] - canvas.coords(self.base)[0]) / 2, canvas.coords(self.base)[1] + (canvas.coords(self.base)[3] - canvas.coords(self.base)[1]) / 2]
    
    ### Edge calculations
    def edge_calc(self, e, dir):
        if dir == 'cw':
            return self.edges[(e+1)%4]
        if dir == 'ccw':
            return self.edges[(e+4-1)%4]
        if dir == 'o':
            return self.edges[(e+2)%4]
        return None

    ### Move/resize a component by changing its coordinates
    def adjust(self, c, initial_coords, dx=0, dy=0, dx2=None, dy2=None):
        if dx2 is None:
            dx2 = dx
        if dy2 is None:
            dy2 = dy
        coords = canvas.coords(c)
        coords[0] = initial_coords[0] + dx
        coords[1] = initial_coords[1] + dy
        coords[2] = initial_coords[2] + dx2
        coords[3] = initial_coords[3] + dy2
        canvas.coords(c, coords)

    ### Select an object
    def select(self, event):
        global start_x, start_y, selected, initial_coords
        start_x = event.x
        start_y = event.y
        selected = event.widget.find_closest(event.x, event.y)[0]
    
    ### Deselect an object
    def deselect(self, event):
        self.center = [canvas.coords(self.base)[0] + (canvas.coords(self.base)[2] - canvas.coords(self.base)[0]) / 2, canvas.coords(self.base)[1] + (canvas.coords(self.base)[3] - canvas.coords(self.base)[1]) / 2]
        for component in self.components.keys():
            self.components[component] = canvas.coords(component)

    ### Handle a user dragging the mouse
    def drag(self, event):
        global start_x, start_y, selected, initial_coords
        dx = event.x - start_x
        dy = event.y - start_y

        if selected in self.components:
            for c, initial_coords in self.components.items():
                self.adjust(c, initial_coords, dx=dx, dy=dy)
        
    ### Handle the user resizing an object
    def resize(self, event, dir):
        global start_x, start_y, selected, initial_coords
        dx = event.x - start_x
        dy = event.y - start_y

        if selected in self.components:
            if (dir == 'vertical') and (canvas.coords(selected)[3] < self.center[1] - Block.EDGE_SIZE):
                # North edge
                self.adjust(selected, self.components[selected], dx=0, dy=dy, dx2=0, dy2=dy)
                self.adjust(self.base, self.components[self.base], dx=0, dy=dy, dx2=0, dy2=0)
                for e in [edge for edge in [self.edge_calc(0, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=0, dy=dy, dx2=0, dy2=0)
                #self.adjust(self.circ, self.components[self.circ], dx=0, dy=dy/2, dx2=0, dy2=dy/2)
            elif (dir == 'vertical') and (canvas.coords(selected)[1] > self.center[1] + Block.EDGE_SIZE):
                # South edge
                self.adjust(selected, self.components[selected], dx=0, dy=dy, dx2=0, dy2=dy)
                self.adjust(self.base, self.components[self.base], dx=0, dy=0, dx2=0, dy2=dy)
                for e in [edge for edge in [self.edge_calc(2, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=0, dy=0, dx2=0, dy2=dy)
                #self.adjust(self.circ, self.components[self.circ], dx=0, dy=dy/2, dx2=0, dy2=dy/2)
            elif (dir == 'horizontal') and (canvas.coords(selected)[2] > self.center[0] + Block.EDGE_SIZE):
                # East edge
                self.adjust(selected, self.components[selected], dx=dx, dy=0, dx2=dx, dy2=0)
                self.adjust(self.base, self.components[self.base], dx=0, dy=0, dx2=dx, dy2=0)
                for e in [edge for edge in [self.edge_calc(1, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=0, dy=0, dx2=dx, dy2=0)
                #self.adjust(self.circ, self.components[self.circ], dx=dx/2, dy=0, dx2=dx/2, dy2=0)
            elif (dir == 'horizontal') and (canvas.coords(selected)[0] < self.center[0] - Block.EDGE_SIZE):
                # West edge
                self.adjust(selected, self.components[selected], dx=dx, dy=0, dx2=dx, dy2=0)
                self.adjust(self.base, self.components[self.base], dx=dx, dy=0, dx2=0, dy2=0)
                for e in [edge for edge in [self.edge_calc(3, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=dx, dy=0, dx2=0, dy2=0)
                #self.adjust(self.circ, self.components[self.circ], dx=dx/2, dy=0, dx2=dx/2, dy2=0)

    ### Create the circle in the center that is used for dragging
    # def create_drag(self):
    #     coords = [self.center[0] - Block.CIRCLE_RADIUS, self.center[1] - Block.CIRCLE_RADIUS, self.center[0] + Block.CIRCLE_RADIUS, self.center[1] + Block.CIRCLE_RADIUS]
    #     circ = canvas.create_oval(coords[0], coords[1], coords[2], coords[3], fill=Block.CIRCLE_FILL)
    #     self.components[circ] = coords

    #     canvas.tag_bind(circ, '<Button 1>', self.select)
    #     canvas.tag_bind(circ, '<B1-Motion>', self.drag)
    #     canvas.tag_bind(circ, '<ButtonRelease-1>', self.deselect)
    #     return circ
    
    ### Create the rectangles on the edges that are used for resizing
    def create_resize(self):
        # North edge
        coords = [canvas.coords(self.base)[0], canvas.coords(self.base)[1], canvas.coords(self.base)[2], canvas.coords(self.base)[1] + Block.EDGE_SIZE]
        edge_n = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_n, '<Button 1>', self.select)
        canvas.tag_bind(edge_n, '<B1-Motion>', lambda event: self.resize(event, dir='vertical'))
        canvas.tag_bind(edge_n, '<ButtonRelease-1>', self.deselect)
        self.components[edge_n] = coords
        self.edges[0] = edge_n

        # South edge
        coords = [canvas.coords(self.base)[0], canvas.coords(self.base)[3] - Block.EDGE_SIZE, canvas.coords(self.base)[2], canvas.coords(self.base)[3]]
        edge_s = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_s, '<Button 1>', self.select)
        canvas.tag_bind(edge_s, '<B1-Motion>', lambda event: self.resize(event, dir='vertical'))
        canvas.tag_bind(edge_s, '<ButtonRelease-1>', self.deselect)
        self.components[edge_s] = coords
        self.edges[2] = edge_s

        # East edge
        coords = [canvas.coords(self.base)[2] - Block.EDGE_SIZE, canvas.coords(self.base)[1], canvas.coords(self.base)[2], canvas.coords(self.base)[3]]
        edge_e = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_e, '<Button 1>', self.select)
        canvas.tag_bind(edge_e, '<B1-Motion>', lambda event: self.resize(event, dir='horizontal'))
        canvas.tag_bind(edge_e, '<ButtonRelease-1>', self.deselect)
        self.components[edge_e] = coords
        self.edges[1] = edge_e

        # West edge
        coords = [canvas.coords(self.base)[0], canvas.coords(self.base)[1], canvas.coords(self.base)[0] + Block.EDGE_SIZE, canvas.coords(self.base)[3]]
        edge_w = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_w, '<Button 1>', self.select)
        canvas.tag_bind(edge_w, '<B1-Motion>', lambda event: self.resize(event, dir='horizontal'))
        canvas.tag_bind(edge_w, '<ButtonRelease-1>', self.deselect)
        self.components[edge_w] = coords
        self.edges[3] = edge_w

class Grid:
    ### Constructor
    def __init__(self, x0, y0, x1, y1, rows, columns):
        canvas.create_rectangle(x0, y0, x1, y1)

        self.rows = rows
        self.row_height = (y1 - y0) / rows
        self.row_coords = [y0]
        for r in range(1, rows):
            y = y0 + r * self.row_height
            self.row_coords.append(y)
            canvas.create_line(x0, y, x1, y)
        self.row_coords.append(y1)

        self.columns = columns
        self.column_width = (x1 - x0) / columns
        self.column_coords = [x0]
        for c in range(1, columns):
            x = x0 + c * self.column_width
            self.column_coords.append(x)
            canvas.create_line(x, y0, x, y1)
        self.column_coords.append(x1)
    
class Snappable(Block):
    SNAP_RANGE = 5

    def __init__(self, grid, x0, y0, x1, y1, fill='blue', draggable=True, resizable=True):
        self.grid = grid
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        super().__init__(self.grid.column_coords[x0], self.grid.row_coords[y0], self.grid.column_coords[x1], self.grid.row_coords[y1], fill=fill, draggable=draggable, resizable=resizable)
    
    ### Handle the user resizing an object
    def resize(self, event, dir):
        global start_x, start_y, selected, initial_coords
        dx = 0
        dy = 0
        if (self.x0 > 0) and (event.x < self.grid.column_coords[self.x0-1] + Snappable.SNAP_RANGE):
            dx = self.grid.column_coords[self.x0-1] - self.grid.column_coords[self.x0]
        elif (self.x1 < self.grid.columns) and (event.x > self.grid.column_coords[self.x1+1] - Snappable.SNAP_RANGE):
            dx = self.grid.column_coords[self.x1+1] - self.grid.column_coords[self.x1]
        elif (self.y0 > 0) and (event.y < self.grid.row_coords[self.y0-1] + Snappable.SNAP_RANGE):
            dy = self.grid.row_coords[self.y0-1] - self.grid.row_coords[self.y0]
        elif (self.y1 < self.grid.rows) and (event.y > self.grid.row_coords[self.y1+1] - Snappable.SNAP_RANGE):
            dy = self.grid.row_coords[self.y1+1] - self.grid.row_coords[self.y1]
        
        if selected in self.components:
            if (dir == 'vertical') and (canvas.coords(selected)[3] < self.center[1] - Block.EDGE_SIZE):
                # North edge
                self.adjust(selected, self.components[selected], dx=0, dy=dy, dx2=0, dy2=dy)
                self.adjust(self.base, self.components[self.base], dx=0, dy=dy, dx2=0, dy2=0)
                for e in [edge for edge in [self.edge_calc(0, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=0, dy=dy, dx2=0, dy2=0)
                #self.adjust(self.circ, self.components[self.circ], dx=0, dy=dy/2, dx2=0, dy2=dy/2)
            elif (dir == 'vertical') and (canvas.coords(selected)[1] > self.center[1] + Block.EDGE_SIZE):
                # South edge
                self.adjust(selected, self.components[selected], dx=0, dy=dy, dx2=0, dy2=dy)
                self.adjust(self.base, self.components[self.base], dx=0, dy=0, dx2=0, dy2=dy)
                for e in [edge for edge in [self.edge_calc(2, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=0, dy=0, dx2=0, dy2=dy)
                #self.adjust(self.circ, self.components[self.circ], dx=0, dy=dy/2, dx2=0, dy2=dy/2)
            elif (dir == 'horizontal') and (canvas.coords(selected)[2] > self.center[0] + Block.EDGE_SIZE):
                # East edge
                self.adjust(selected, self.components[selected], dx=dx, dy=0, dx2=dx, dy2=0)
                self.adjust(self.base, self.components[self.base], dx=0, dy=0, dx2=dx, dy2=0)
                for e in [edge for edge in [self.edge_calc(1, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=0, dy=0, dx2=dx, dy2=0)
                #self.adjust(self.circ, self.components[self.circ], dx=dx/2, dy=0, dx2=dx/2, dy2=0)
            elif (dir == 'horizontal') and (canvas.coords(selected)[0] < self.center[0] - Block.EDGE_SIZE):
                # West edge
                self.adjust(selected, self.components[selected], dx=dx, dy=0, dx2=dx, dy2=0)
                self.adjust(self.base, self.components[self.base], dx=dx, dy=0, dx2=0, dy2=0)
                for e in [edge for edge in [self.edge_calc(3, d) for d in ['cw', 'ccw']] if edge is not None]:
                    self.adjust(e, self.components[e], dx=dx, dy=0, dx2=0, dy2=0)
                #self.adjust(self.circ, self.components[self.circ], dx=dx/2, dy=0, dx2=dx/2, dy2=0)

#block = Block(175, 175, 225, 225, draggable=True, resizable=True)
grid = Grid(100, 100, 300, 300, 6, 4)
snap = Snappable(grid, 1, 1, 2, 2)

root.mainloop()