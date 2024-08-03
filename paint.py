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
