import tkinter as tk
from tkinter import ttk
import datetime as dt
import pandas as pd
import numpy as np

matrix = pd.read_csv('Camps Matrix.csv')
camps = matrix.loc[matrix['Start Date'] == '17-Jul', 'Camp Name']

root = tk.Tk()
MARGIN_X = 20
MARGIN_Y = 20

DAY_START = dt.time(hour=9)
DAY_END = dt.time(hour=16)
INCREMENT = dt.timedelta(minutes=15)

time_difference = (DAY_END.hour * 60 + DAY_END.minute) - (DAY_START.hour * 60 + DAY_START.minute)
num_intervals = int(time_difference // (INCREMENT.total_seconds() // 60))

### Make title label (place later after window size is determined)
title = tk.Label(root, text='Pool & Playground Times', font=('Arial', 24, 'bold'))

### TODO: Make OptionMenu for camp week
def handle_selection(selection):
    print("Selected: ", selection)

start_date = tk.StringVar()

GRID_X = MARGIN_X
GRID_Y = MARGIN_Y + title.winfo_reqheight()
GRID_WIDTH = 1200
ROW_HEIGHT = 30

### Create preliminary canvas with small height
grid = tk.Canvas(root, width=GRID_WIDTH, height=100)
grid.place(x=GRID_X, y=GRID_Y)

### Create camp labels to calculate left margin
grid_margin_left = 0
grid_camp_labels = []
for c in range(0, len(camps)):
    label = grid.create_text(GRID_WIDTH//2, grid.winfo_height()//2, anchor='c', text=camps[c], font=('Arial', 12))
    grid_margin_left = max(grid_margin_left, grid.bbox(label)[2] - grid.bbox(label)[0])
    grid_camp_labels.append(label)
grid_margin_left += 4

### Create time labels to calculate top margin
grid_margin_top = 0
grid_time_labels = []
times = []
for t in range(0, num_intervals):
    time = (dt.datetime.combine(dt.date.today(), DAY_START) + INCREMENT * t).time()
    times.append(time)

    label = grid.create_text(GRID_WIDTH//2, grid.winfo_height()//2, anchor='c', text=time.strftime('%I:%M').lstrip('0'), angle=45, font=('Arial', 12))
    grid_margin_top = max(grid_margin_top, grid.bbox(label)[3] - grid.bbox(label)[1])
    grid_time_labels.append(label)
grid_margin_top += 4
#print(times)

### Calculate new dimensions of grid
grid_height=(grid_margin_top + ROW_HEIGHT*len(camps))
grid.config(height=grid_height)

### Create place to store gridline coordinates
gridlines = [[], []]

### Place camp labels and draw horizontal lines
for c in range(0, len(camps)):
    #offset = ((grid.bbox(grid_camp_labels[c])[3] - grid.bbox(grid_camp_labels[c])[1]) // 2)
    y = grid_margin_top + (c * ROW_HEIGHT)
    gridlines[1].append(y)
    grid.coords(grid_camp_labels[c], 1 + grid_margin_left // 2, y + (ROW_HEIGHT // 2))
    grid.create_line(0, y, GRID_WIDTH, y)
gridlines[1].append(grid_height)

### Place time labels and draw vertical lines
column_width = (GRID_WIDTH - grid_margin_left) / num_intervals
for t in range(0, num_intervals):
    x = grid_margin_left + (t * column_width)
    gridlines[0].append(x)
    grid.coords(grid_time_labels[t], x + (column_width / 2), 2 + (grid_margin_top / 2))
    grid.create_line(x, 0, x, grid_height)
gridlines[0].append(GRID_WIDTH)

### Calculate "true" grid width (only the inner grid)
true_grid_width = GRID_WIDTH - grid_margin_left

### Draw borders of the grid
grid.create_line(2, 2, GRID_WIDTH, 2)
grid.create_line(2, 2, 2, grid_height)
grid.create_line(2, grid_height, GRID_WIDTH, grid_height)
grid.create_line(GRID_WIDTH, 2, GRID_WIDTH, grid_height)

### Re-size window to fit grid
window_x = GRID_X + GRID_WIDTH + MARGIN_X
window_y = GRID_Y + grid_height + MARGIN_Y
root.geometry(f'{window_x}x{window_y}')

### Place title at top-center of window
title.place(x=(window_x // 2)-(title.winfo_reqwidth() // 2))


### Draggable rectangles

# class Block:
#     def __init__(self, draggable=True):
#         self.draggable=draggable
    
#     def attach(self, other):
#         # Check if other is adjacent
        

rectangles = []

selected_rectangle = None
initial_rect_coords = None

THRESHOLD_DISTANCE = 50

def start_drag(event):
    global start_x, start_y, selected_rectangle, initial_rect_coords
    start_x = event.x
    start_y = event.y
    selected_rectangle = event.widget.find_closest(event.x, event.y)[0]
    initial_rect_coords = grid.coords(selected_rectangle)

def drag(event):
    global start_x, start_y, selected_rectangle, initial_rect_coords
    dx = event.x - start_x
    dy = event.y - start_y
    rect_coords = initial_rect_coords.copy()

    if selected_rectangle in rectangles:
        if abs(event.x - (rect_coords[0] + rect_coords[2]) / 2) < THRESHOLD_DISTANCE:
            rect_coords[0] += dx
            rect_coords[2] += dx
        elif event.x < rect_coords[0] + 5:
            rect_coords[0] = event.x
        elif event.x > rect_coords[2] - 5:
            rect_coords[2] = event.x
    
    grid.coords(selected_rectangle, rect_coords)

### Draw rectangles for all camps with pool time
POOL_DURATION = 45
LOCKER_DURATION = 15
PLAYGROUND_DURATION = 30

def time_to_rect(start, end, fill='blue'):
    start = start - start.combine(start.date(), DAY_START)
    end = end - end.combine(end.date(), DAY_START)

    start = start.total_seconds() / (time_difference * 60)
    end = end.total_seconds() / (time_difference * 60)

    rect_start = grid_margin_left + (start * true_grid_width)
    rect_end = grid_margin_left + (end * true_grid_width)

    rect = grid.create_rectangle(rect_start, gridlines[1][c], rect_end, gridlines[1][c+1], fill=fill)
    rectangles.append(rect)

def draw_pool_time(camp):
    pool_start = pd.to_datetime(camp['Pool Time'])
    pool_end = pool_start + np.timedelta64(POOL_DURATION, 'm')
    locker_start = pool_start - np.timedelta64(LOCKER_DURATION, 'm')
    locker_end = pool_end + np.timedelta64(LOCKER_DURATION, 'm')

    time_to_rect(locker_start, pool_start, fill='yellow')
    time_to_rect(pool_start, pool_end, fill='blue')
    time_to_rect(pool_end, locker_end, fill='yellow')

def draw_playground_time(camp, extra=False):
    pg_start = pd.to_datetime(camp['PG Time'])
    if extra:
        pg_start = pd.to_datetime(camp['PG+ Time'])
    pg_end = pg_start + np.timedelta64(PLAYGROUND_DURATION, 'm')

    time_to_rect(pg_start, pg_end, fill='orange')

for c in range(0, len(camps)):
    camp = matrix.iloc[c]
    if camp['Swim'] == True:
        draw_pool_time(camp)
    if camp['PG'] == True:
        draw_playground_time(camp)
    if camp['PG+'] == True:
        draw_playground_time(camp, True)


# for c in range(0, len(camps)):
#     camp = matrix.iloc[c]
#     schedule(camp)

for rect in rectangles:
    grid.tag_bind(rect, '<Button-1>', start_drag)
    grid.tag_bind(rect, '<B1-Motion>', drag)

root.mainloop()