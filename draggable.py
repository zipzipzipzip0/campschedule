import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

class Block:
    # Constants
    EDGE_SIZE = 5
    EDGE_FILL = 'gray'
    CIRCLE_RADIUS = 5
    CIRCLE_FILL = 'gray'

    def __init__(self, x1, y1, x2, y2, fill='blue', draggable=True, resizable=True):
        # Local vars
        self.coords = [x1, y1, x2, y2]
        self.fill = fill
        self.components = []

        # Handle base
        self.base = self.create_base()
        self.center = [self.coords[0] + (self.coords[2] - self.coords[0]) / 2, self.coords[1] + (self.coords[3] - self.coords[1]) / 2]

        # Handle draggable
        if draggable:
            self.create_drag()

        # Handle resizable
        if resizable:
            self.create_resize()
    
    def update_params(self):
        self.center = canvas.coords(self.base)
        self.center = [self.coords[0] + (self.coords[2] - self.coords[0]) / 2, self.coords[1] + (self.coords[3] - self.coords[1]) / 2]
    
    def select(self, event):
        global start_x, start_y, selected, initial_coords
        start_x = event.x
        start_y = event.y
        selected = event.widget.find_closest(event.x, event.y)[0]
        initial_coords = [canvas.coords(c).copy() for c in self.components]

    def drag(self, event):
        global start_x, start_y, selected, initial_coords
        dx = event.x - start_x
        dy = event.y - start_y

        if selected in self.components:
            for c in range(0, len(self.components)):
                coords = canvas.coords(self.components[c])
                coords[0] = initial_coords[c][0] + dx
                coords[1] = initial_coords[c][1] + dy
                coords[2] = initial_coords[c][2] + dx
                coords[3] = initial_coords[c][3] + dy
                canvas.coords(self.components[c], coords)
        
        self.update_params()

    def resize(self, event, dir):
        global start_x, start_y, selected, initial_coords
        dx = event.x - start_x
        dy = event.y - start_y

        if selected in self.components:
            if (dir == 'vertical') and (canvas.coords(selected)[3] < self.center[1] + Block.EDGE_SIZE):
                # North edge
                # Drag north edge
                # Extend base
                # Extend east and west edges
                # Update circle
                pass
            if (dir == 'vertical') and (canvas.coords(selected)[1] > self.center[1] - Block.EDGE_SIZE):
                # South edge
                pass
            if (dir == 'horizontal') and (canvas.coords(selected)[2] > self.center[0] - Block.EDGE_SIZE):
                # East edge
                pass
            if (dir == 'horizontal') and (canvas.coords(selected)[0] < self.center[0] + Block.EDGE_SIZE):
                # West edge
                pass

    
    def create_base(self):
        base = canvas.create_rectangle(self.coords[0], self.coords[1], self.coords[2], self.coords[3], fill=self.fill)
        self.components.append(base)
        return base

    def create_drag(self):
        circ = canvas.create_oval(self.center[0] - Block.CIRCLE_RADIUS, self.center[1] - Block.CIRCLE_RADIUS, self.center[0] + Block.CIRCLE_RADIUS, self.center[1] + Block.CIRCLE_RADIUS, fill=Block.CIRCLE_FILL)
        self.components.append(circ)

        canvas.tag_bind(circ, '<Button 1>', self.select)
        canvas.tag_bind(circ, '<B1-Motion>', self.drag)
    
    def create_resize(self):
        edges = []
        
        edge_n = canvas.create_rectangle(self.coords[0], self.coords[1], self.coords[2], self.coords[1] + Block.EDGE_SIZE, fill=Block.EDGE_FILL)
        edge_s = canvas.create_rectangle(self.coords[0], self.coords[3] - Block.EDGE_SIZE, self.coords[2], self.coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_n, '<Button 1>', self.select)
        canvas.tag_bind(edge_n, '<B1-Motion>', lambda event: self.resize(event, dir='vertical'))
        canvas.tag_bind(edge_s, '<Button 1>', self.select)
        canvas.tag_bind(edge_s, '<B1-Motion>', lambda event: self.resize(event, dir='vertical'))
        edges.append(edge_n)
        edges.append(edge_s)
        
        edge_e = canvas.create_rectangle(self.coords[2] - Block.EDGE_SIZE, self.coords[1], self.coords[2], self.coords[3], fill=Block.EDGE_FILL)
        edge_w = canvas.create_rectangle(self.coords[0], self.coords[1], self.coords[0] + Block.EDGE_SIZE, self.coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_e, '<Button 1>', self.select)
        canvas.tag_bind(edge_e, '<B1-Motion>', lambda event: self.resize(event, dir='horizontal'))
        canvas.tag_bind(edge_w, '<Button 1>', self.select)
        canvas.tag_bind(edge_w, '<B1-Motion>', lambda event: self.resize(event, dir='horizontal'))
        edges.append(edge_e)
        edges.append(edge_w)

        for e in edges:
            self.components.append(e)

block = Block(175, 175, 225, 225, draggable=True, resizable=True)

root.mainloop()