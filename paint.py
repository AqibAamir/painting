import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring
from tkinter import filedialog
import os

class SimpleDrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aqib's  Drawing App")
        self.root.geometry("1000x800")
        self.color = "black"
        self.brush_size = 5
        self.brush_type = "round"  # Default to a valid brush type
        self.tool = "brush"
        self.history = []
        self.redo_stack = []
        self.current_item = None
        self.create_widgets()
        self.setup_canvas()
        self.setup_status_bar()
        self.setup_keyboard_shortcuts()
        self.show_grid = False
        self.grid_size = 20

    def create_widgets(self):
        # Create and pack the toolbar
        self.toolbar = tk.Frame(self.root, bg="lightgray")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Color selection button
        self.color_button = tk.Button(self.toolbar, text="Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5)

        # Brush size controls
        self.size_label = tk.Label(self.toolbar, text="Size:")
        self.size_label.pack(side=tk.LEFT, padx=5)

        self.size_scale = tk.Scale(self.toolbar, from_=1, to=20, orient=tk.HORIZONTAL, command=self.change_size)
        self.size_scale.set(self.brush_size)
        self.size_scale.pack(side=tk.LEFT, padx=5)

        # Brush type controls
        self.type_label = tk.Label(self.toolbar, text="Brush:")
        self.type_label.pack(side=tk.LEFT, padx=5)

        self.brush_var = tk.StringVar(value=self.brush_type)
        self.round_radio = tk.Radiobutton(self.toolbar, text="Round", variable=self.brush_var, value="round", command=self.change_brush)
        self.round_radio.pack(side=tk.LEFT, padx=5)

        self.square_radio = tk.Radiobutton(self.toolbar, text="Square", variable=self.brush_var, value="square", command=self.change_brush)
        self.square_radio.pack(side=tk.LEFT, padx=5)

        # Tool controls
        self.tool_label = tk.Label(self.toolbar, text="Tool:")
        self.tool_label.pack(side=tk.LEFT, padx=5)

        self.tool_var = tk.StringVar(value=self.tool)
        self.brush_radio = tk.Radiobutton(self.toolbar, text="Brush", variable=self.tool_var, value="brush", command=self.change_tool)
        self.brush_radio.pack(side=tk.LEFT, padx=5)

        self.eraser_radio = tk.Radiobutton(self.toolbar, text="Eraser", variable=self.tool_var, value="eraser", command=self.change_tool)
        self.eraser_radio.pack(side=tk.LEFT, padx=5)

        self.line_radio = tk.Radiobutton(self.toolbar, text="Line", variable=self.tool_var, value="line", command=self.change_tool)
        self.line_radio.pack(side=tk.LEFT, padx=5)


        self.rect_radio = tk.Radiobutton(self.toolbar, text="Rectangle", variable=self.tool_var, value="rectangle", command=self.change_tool)
        self.rect_radio.pack(side=tk.LEFT, padx=5)

        self.oval_radio = tk.Radiobutton(self.toolbar, text="Oval", variable=self.tool_var, value="oval", command=self.change_tool)
        self.oval_radio.pack(side=tk.LEFT, padx=5)

        self.text_radio = tk.Radiobutton(self.toolbar, text="Text", variable=self.tool_var, value="text", command=self.change_tool)
        self.text_radio.pack(side=tk.LEFT, padx=5)

        self.polygon_radio = tk.Radiobutton(self.toolbar, text="Polygon", variable=self.tool_var, value="polygon", command=self.change_tool)
        self.polygon_radio.pack(side=tk.LEFT, padx=5)

        self.triangle_radio = tk.Radiobutton(self.toolbar, text="Triangle", variable=self.tool_var, value="triangle", command=self.change_tool)
        self.triangle_radio.pack(side=tk.LEFT, padx=5)

        self.pentagon_radio = tk.Radiobutton(self.toolbar, text="Pentagon", variable=self.tool_var, value="pentagon", command=self.change_tool)
        self.pentagon_radio.pack(side=tk.LEFT, padx=5)

        # Additional Buttons
        self.fill_button = tk.Button(self.toolbar, text="Fill", command=self.fill_color)
        self.fill_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.toolbar, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.toolbar, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.redo_button = tk.Button(self.toolbar, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_canvas)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(self.toolbar, text="Load", command=self.load_canvas)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.smooth_label = tk.Label(self.toolbar, text="Smooth:")
        self.smooth_label.pack(side=tk.LEFT, padx=5)

        self.smooth_var = tk.BooleanVar(value=True)
        self.smooth_check = tk.Checkbutton(self.toolbar, variable=self.smooth_var, command=self.toggle_smooth)
        self.smooth_check.pack(side=tk.LEFT, padx=5)

        self.grid_button = tk.Button(self.toolbar, text="Toggle Grid", command=self.toggle_grid)
        self.grid_button.pack(side=tk.LEFT, padx=5)

        # Initialize grid settings
        self.grid_size = 20
        self.show_grid = False


    def setup_canvas(self):
        # Set up the drawing canvas
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.old_x = None
        self.old_y = None

    def setup_status_bar(self):
        # Create and pack the status bar
        self.status_bar = tk.Label(self.root, text="Brush: black", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_keyboard_shortcuts(self):
        # Define keyboard shortcuts
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Control-s>", lambda event: self.save_canvas())
        self.root.bind("<Control-o>", lambda event: self.load_canvas())
        self.root.bind("<Control-q>", lambda event: self.root.quit())

    def choose_color(self):
        # Open a color chooser dialog and set the selected color
        self.color = askcolor(color=self.color)[1]
        self.update_status_bar()

    def change_size(self, value):
        # Change the brush size based on slider input
        self.brush_size = int(value)

    def change_brush(self):
        # Update the brush type
        self.brush_type = self.brush_var.get()
        if self.brush_type not in {"butt", "projecting", "round"}:
            self.brush_type = "round"  # Default to a valid brush type
        self.update_status_bar()

    def change_tool(self):
        # Update the current drawing tool
        self.tool = self.tool_var.get()
        self.update_status_bar()

    def clear_canvas(self):
        # Clear the canvas and reset history
        self.canvas.delete("all")
        self.history = []
        self.redo_stack = []

    def undo(self):
        # Undo the last action
        if self.history:
            last_item = self.history.pop()
            self.redo_stack.append(last_item)
            self.canvas.delete(last_item)

    def redo(self):
        # Redo the last undone action
        if self.redo_stack:
            item = self.redo_stack.pop()
            self.history.append(item)
            self.canvas.itemconfig(item, state="normal")


    def save_canvas(self):
        # Save the canvas content as a PostScript file
        file_path = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps")])
        if file_path:
            self.canvas.postscript(file=file_path, colormode="color")

    def load_canvas(self):
        # Load the canvas content from a PostScript file
        file_path = filedialog.askopenfilename(filetypes=[("PostScript files", "*.ps")])
        if file_path:
            os.system(f"gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -sOutputFile=temp.png {file_path}")
            self.canvas.delete("all")
            self.image = tk.PhotoImage(file="temp.png")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
            os.remove("temp.png")

    def toggle_smooth(self):
        # Toggle smooth drawing
        self.update_status_bar()

    def toggle_grid(self):
        # Toggle grid visibility
        self.show_grid = not self.show_grid
        self.draw_grid()

    def draw_grid(self):
        # Draw or remove grid lines based on current state
        if self.show_grid:
            for i in range(0, self.canvas.winfo_width(), self.grid_size):
                self.canvas.create_line(i, 0, i, self.canvas.winfo_height(), fill="lightgray", tags="grid_line")
            for i in range(0, self.canvas.winfo_height(), self.grid_size):
                self.canvas.create_line(0, i, self.canvas.winfo_width(), i, fill="lightgray", tags="grid_line")
        else:
            self.canvas.delete("grid_line")

    def start_draw(self, event):
        # Start drawing based on selected tool
        if self.tool == "polygon":
            if self.old_x and self.old_y:
                item = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, fill=self.color, width=self.brush_size)
                self.history.append(item)
                self.old_x, self.old_y = event.x, event.y
            else:
                self.old_x, self.old_y = event.x, event.y

    def paint(self, event):
        # Paint or draw shapes based on selected tool
        if self.tool == "brush":
            self.draw_brush(event)
        elif self.tool == "eraser":
            self.erase(event)
        elif self.tool in {"line", "rectangle", "oval", "triangle", "pentagon"}:
            self.draw_shape(event)
        elif self.tool == "text":
            self.draw_text(event)
        elif self.tool == "fill":
            self.fill_color(event)


    def draw_brush(self, event):
        # Draw brush strokes
        if self.old_x and self.old_y:
            item = self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.brush_size, fill=self.color,
                capstyle=self.brush_type, smooth=self.smooth_var.get()
            )
            self.history.append(item)
        self.old_x = event.x
        self.old_y = event.y

    def erase(self, event):
        # Draw eraser strokes
        if self.old_x and self.old_y:
            item = self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.brush_size, fill="white",
                capstyle=self.brush_type, smooth=self.smooth_var.get()
            )
            self.history.append(item)
        self.old_x = event.x
        self.old_y = event.y

    def draw_shape(self, event):
        # Draw various shapes
        if self.old_x and self.old_y:
            if self.current_item:
                self.canvas.delete(self.current_item)
            if self.tool == "line":
                self.current_item = self.canvas.create_line(
                    self.old_x, self.old_y, event.x, event.y,
                    width=self.brush_size, fill=self.color
                )
            elif self.tool == "rectangle":
                self.current_item = self.canvas.create_rectangle(
                    self.old_x, self.old_y, event.x, event.y,
                    outline=self.color, width=self.brush_size
                )
            elif self.tool == "oval":
                self.current_item = self.canvas.create_oval(
                    self.old_x, self.old_y, event.x, event.y,
                    outline=self.color, width=self.brush_size
                )
            elif self.tool == "triangle":
                self.current_item = self.canvas.create_polygon(
                    self.old_x, self.old_y, event.x, event.y,
                    self.old_x - (event.x - self.old_x), event.y,
                    outline=self.color, width=self.brush_size, fill=''
                )
            elif self.tool == "pentagon":
                    self.current_item = self.canvas.create_polygon(
                    self.old_x, self.old_y,
                    self.old_x + (event.x - self.old_x) // 2, event.y,
                    self.old_x - (event.x - self.old_x) // 2, event.y,
                    self.old_x - (event.x - self.old_x), self.old_y + (event.y - self.old_y) // 2,
                    self.old_x + (event.x - self.old_x), self.old_y + (event.y - self.old_y) // 2,
                    outline=self.color, width=self.brush_size, fill=''
                )

    def draw_text(self, event):
        # Draw text at the specified location
        text = askstring("Text", "Enter text:")
        if text:
            item = self.canvas.create_text(
                event.x, event.y, text=text, fill=self.color,
                font=("Arial", self.brush_size * 2)
            )
            self.history.append(item)

    def fill_color(self, event=None):
        # Fill color in shapes
        if event:
            item = self.canvas.find_closest(event.x, event.y)
            self.canvas.itemconfig(item, fill=self.color)

    def reset(self, event):
        # Reset drawing state
        self.old_x = None
        self.old_y = None
        if self.current_item:
            self.history.append(self.current_item)
            self.current_item = None

    def update_status_bar(self):
        # Update status bar with current tool and color
        self.status_bar.config(text=f"Tool: {self.tool.capitalize()}, Color: {self.color}")

    def update_status_bar(self):
        # Update status bar with current tool, color, and brush size
        self.status_bar.config(text=f"Tool: {self.tool.capitalize()}, Color: {self.color}, Size: {self.brush_size}")

    def draw_shape(self, event):
        # Draw various shapes
        if self.old_x and self.old_y:
            if self.current_item:
                self.canvas.delete(self.current_item)
            if self.tool == "line":
                self.current_item = self.canvas.create_line(
                    self.old_x, self.old_y, event.x, event.y,
                    width=self.brush_size, fill=self.color
                )
            elif self.tool == "rectangle":
                self.current_item = self.canvas.create_rectangle(
                    self.old_x, self.old_y, event.x, event.y,
                    outline=self.color, width=self.brush_size, fill=self.color
                )
            elif self.tool == "oval":
                self.current_item = self.canvas.create_oval(
                    self.old_x, self.old_y, event.x, event.y,
                    outline=self.color, width=self.brush_size, fill=self.color
                )
            elif self.tool == "triangle":
                self.current_item = self.canvas.create_polygon(
                    self.old_x, self.old_y, event.x, event.y,
                    self.old_x - (event.x - self.old_x), event.y,
                    outline=self.color, width=self.brush_size, fill=self.color
                )
            elif self.tool == "pentagon":
                self.current_item = self.canvas.create_polygon(
                    self.old_x, self.old_y,
                    self.old_x + (event.x - self.old_x) // 2, event.y,
                    self.old_x - (event.x - self.old_x) // 2, event.y,
                    self.old_x - (event.x - self.old_x), self.old_y + (event.y - self.old_y) // 2,
                    self.old_x + (event.x - self.old_x), self.old_y + (event.y - self.old_y) // 2,
                    outline=self.color, width=self.brush_size, fill=self.color
                )

    def fill_color(self, event=None):
        # Fill color in shapes
        if event:
            item = self.canvas.find_closest(event.x, event.y)
            if self.canvas.type(item) in ("rectangle", "oval", "polygon"):
                self.canvas.itemconfig(item, fill=self.color)

    def draw_grid(self):
        # Draw or remove grid lines based on current state
        if self.show_grid:
            self.canvas.delete("grid_line")
            for i in range(0, self.canvas.winfo_width(), self.grid_size):
                self.canvas.create_line(i, 0, i, self.canvas.winfo_height(), fill="lightgray", tags="grid_line")
            for i in range(0, self.canvas.winfo_height(), self.grid_size):
                self.canvas.create_line(0, i, self.canvas.winfo_width(), i, fill="lightgray", tags="grid_line")
        else:
            self.canvas.delete("grid_line")

    def toggle_smooth(self):
        # Toggle smooth drawing
        self.update_status_bar()

    def update_status_bar(self):
        # Update status bar with current tool, color, and brush size
        self.status_bar.config(text=f"Tool: {self.tool.capitalize()}, Color: {self.color}, Size: {self.brush_size}")


    def start_draw(self, event):
        # Start drawing based on selected tool
        if self.tool in {"line", "rectangle", "oval", "triangle", "pentagon"}:
            self.old_x, self.old_y = event.x, event.y
            self.current_item = None
        elif self.tool == "text":
            self.draw_text(event)
        elif self.tool == "fill":
            self.fill_color(event)

    def draw_text(self, event):
        # Draw text at the specified location
        text = askstring("Text", "Enter text:")
        if text:
            item = self.canvas.create_text(
                event.x, event.y, text=text, fill=self.color,
                font=("Arial", self.brush_size * 2)
            )
            self.history.append(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDrawApp(root)
    root.mainloop()
