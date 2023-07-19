import tkinter as tk

class Schedule(tk.Tk):
    MARGIN_SIZE = 5
    def __init__(self):
        # Create root window
        super().__init__()

        # Window size
        self.state('zoomed')
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.bind('<Configure>', self.on_resize)

        # Add elements
        self.title = self.create_title()
        self.schedule = self.create_schedule()
        self.option_menu = self.create_option_menu()
    
    ### Title and date selector
    def create_title(self):
        return
    
    ### Grid containing camp names, times, and respective scheduled activities
    def create_schedule(self):
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

if __name__ == '__main__':
    # Create main window
    root = Schedule()

    # Open window
    root.mainloop()