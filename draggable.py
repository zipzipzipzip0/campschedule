import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

class Block:
    ### Constants
    EDGE_SIZE = 5
    EDGE_FILL = 'gray'
    CIRCLE_RADIUS = 5
    CIRCLE_FILL = 'gray'

    ### Constructor
    def __init__(self, x1, y1, x2, y2, fill='blue', draggable=True, resizable=True):
        # Dictionary stores component id:coord pairs
        self.components = {}

        coords = [x1, y1, x2, y2]
        self.base = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=fill)
        self.components[self.base] = coords
        self.center = [canvas.coords(self.base)[0] + (canvas.coords(self.base)[2] - canvas.coords(self.base)[0]) / 2, canvas.coords(self.base)[1] + (canvas.coords(self.base)[3] - canvas.coords(self.base)[1]) / 2]

        # Handle draggable
        if draggable:
            self.create_drag()

        # Handle resizable
        if resizable:
            self.create_resize()

        print(self.components)
    
    # def store_component(self, component):
    #     self.components[component]
    
    def update_params(self):
        self.center = canvas.coords(self.base)
        self.center = [canvas.coords(self.base)[0] + (canvas.coords(self.base)[2] - canvas.coords(self.base)[0]) / 2, canvas.coords(self.base)[1] + (canvas.coords(self.base)[3] - canvas.coords(self.base)[1]) / 2]
    
    ### Move a component
    def move(self, component, d):
        pass

    ### Select an object
    def select(self, event):
        global start_x, start_y, selected, initial_coords
        start_x = event.x
        start_y = event.y
        selected = event.widget.find_closest(event.x, event.y)[0]

    ### Handle a user dragging the mouse
    def drag(self, event):
        global start_x, start_y, selected, initial_coords
        dx = event.x - start_x
        dy = event.y - start_y

        if selected in self.components:
            for c, initial_coords in self.components.items():
                coords = canvas.coords(c)
                coords[0] = initial_coords[0] + dx
                coords[1] = initial_coords[1] + dy
                coords[2] = initial_coords[2] + dx
                coords[3] = initial_coords[3] + dy
                canvas.coords(c, coords)
        
        self.update_params()

    ### Handle the user resizing an object
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

    ### Create the circle in the center that is used for dragging
    def create_drag(self):
        coords = [self.center[0] - Block.CIRCLE_RADIUS, self.center[1] - Block.CIRCLE_RADIUS, self.center[0] + Block.CIRCLE_RADIUS, self.center[1] + Block.CIRCLE_RADIUS]
        circ = canvas.create_oval(coords[0], coords[1], coords[2], coords[3], fill=Block.CIRCLE_FILL)
        self.components[circ] = coords

        canvas.tag_bind(circ, '<Button 1>', self.select)
        canvas.tag_bind(circ, '<B1-Motion>', self.drag)
    
    ### Create the rectangles on the edges that are used for resizing
    def create_resize(self):
        coords = [canvas.coords(self.base)[0], canvas.coords(self.base)[1], canvas.coords(self.base)[2], canvas.coords(self.base)[1] + Block.EDGE_SIZE]
        edge_n = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_n, '<Button 1>', self.select)
        canvas.tag_bind(edge_n, '<B1-Motion>', lambda event: self.resize(event, dir='vertical'))
        self.components[edge_n] = coords

        coords = [canvas.coords(self.base)[0], canvas.coords(self.base)[3] - Block.EDGE_SIZE, canvas.coords(self.base)[2], canvas.coords(self.base)[3]]
        edge_s = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_s, '<Button 1>', self.select)
        canvas.tag_bind(edge_s, '<B1-Motion>', lambda event: self.resize(event, dir='vertical'))
        self.components[edge_s] = coords

        coords = [canvas.coords(self.base)[2] - Block.EDGE_SIZE, canvas.coords(self.base)[1], canvas.coords(self.base)[2], canvas.coords(self.base)[3]]
        edge_e = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_e, '<Button 1>', self.select)
        canvas.tag_bind(edge_e, '<B1-Motion>', lambda event: self.resize(event, dir='horizontal'))
        self.components[edge_e] = coords

        coords = [canvas.coords(self.base)[0], canvas.coords(self.base)[1], canvas.coords(self.base)[0] + Block.EDGE_SIZE, canvas.coords(self.base)[3]]
        edge_w = canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=Block.EDGE_FILL)
        canvas.tag_bind(edge_w, '<Button 1>', self.select)
        canvas.tag_bind(edge_w, '<B1-Motion>', lambda event: self.resize(event, dir='horizontal'))
        self.components[edge_w] = coords

block = Block(175, 175, 225, 225, draggable=True, resizable=True)

root.mainloop()