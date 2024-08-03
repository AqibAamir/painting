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
