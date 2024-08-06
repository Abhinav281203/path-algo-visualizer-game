import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import A_star
import Bfs
import Dfs

class App:
    def __init__(self, root, n):
        self.root = root
        self.n = n
        self.size = self.calculate_cell_size()  # Size of each box in the grid
        self.grid = []
        self.grid_colors = []
        self.start_node = None
        self.end_node = None
        self.dragging = False
        self.create_widgets()
        self.create_grid()

    def calculate_cell_size(self):
        width = self.root.winfo_screenwidth() * 0.8
        height = self.root.winfo_screenheight() * 0.8
        size = min(width, height) // self.n
        # print("Grid size: ", size)
        return int(size)

    def create_widgets(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.dfs = tk.Button(self.button_frame, text="DFS", command=lambda: Dfs.DFS(self)).pack(side=tk.LEFT)
        self.bfs = tk.Button(self.button_frame, text="BFS", command=lambda: Bfs.BFS(self)).pack(side=tk.LEFT)
        self.a_star = tk.Button(self.button_frame, text="A*", command=lambda: A_star.A_star(self)).pack(side=tk.LEFT)
        self.reset = tk.Button(self.button_frame, text="Remove path", command=self.reset_canvas).pack(side=tk.RIGHT)
        self.reset = tk.Button(self.button_frame, text="Remove walls", command=self.reformat).pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self.root, width = self.n * self.size, height=self.n * self.size)
        self.canvas.pack(pady=(self.button_frame.winfo_height(), 0))

        self.canvas.bind("<Button-1>", self.start_drawing_wall)        # Left click
        self.canvas.bind("<B1-Motion>", self.place_wall)               # Dragging
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing_wall)  # Release to stop drawing
        self.canvas.bind("<Button-3>", self.remove_wall)               # Right click
        self.root.bind("<Control-s>", self.set_start_node)
        self.root.bind("<Control-e>", self.set_end_node)

    def reformat(self):
        for i in range(self.n):
            for j in range(self.n):
                self.canvas.itemconfig(self.grid[i][j], fill="#EEE7E5")

    def reset_canvas(self):
        for i in range(self.n):
            for j in range(self.n):
                self.canvas.itemconfig(self.grid[i][j], fill=self.grid_colors[i][j])
    
    def create_grid(self):
        for i in range(self.n):
            row = []
            
            for j in range(self.n):
                x1 = i * self.size
                y1 = j * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size
                # print((x1, y1), (x2, y2))
                cell = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#EEE7E5",
                    outline="black"
                )
                row.append(cell)
            self.grid.append(row)
            self.grid_colors.append(['#EEE7E5'] * len(row))

    def start_drawing_wall(self, e):
        self.dragging = True
        self.place_wall(e)
    
    def stop_drawing_wall(self, e):
        self.dragging = False

    def place_wall(self, e):
        if not self.dragging:
            return
        x, y = e.x, e.y
        row, col = self.get_grid_coordinates(x, y)
        # print(row, col)
        if 0 <= row < self.n and 0 <= col < self.n:
            self.canvas.itemconfig(self.grid[row][col], fill="black")
            self.grid_colors[row][col] = "black"

    def remove_wall(self, e):
        x, y = e.x, e.y
        row, col = self.get_grid_coordinates(x, y)
        if 0 <= row < self.n and 0 <= col < self.n:
            self.canvas.itemconfig(self.grid[row][col], fill="#EEE7E5")
            self.grid_colors[row][col] = "#EEE7E5"
    
    def set_start_node(self, e):
        if self.start_node is not None:
            s = self.start_node
            self.canvas.itemconfig(self.grid[s[0]][s[1]], fill="#EEE7E5")
            self.grid_colors[s[0]][s[1]] = "#EEE7E5"
        x, y = e.x, e.y
        row, col = self.get_grid_coordinates(x, y)
        if 0 <= row < self.n and 0 <= col < self.n:
            self.canvas.itemconfig(self.grid[row][col], fill="green")
            self.start_node = (row, col)
            self.grid_colors[row][col] = "green"
    
    def set_end_node(self, e):
        if self.end_node is not None:
            ed = self.end_node
            self.canvas.itemconfig(self.grid[ed[0]][ed[1]], fill="#EEE7E5")
            self.grid_colors[ed[0]][ed[1]] = "#EEE7E5"
        x, y = e.x, e.y
        row, col = self.get_grid_coordinates(x, y)
        if 0 <= row < self.n and 0 <= col < self.n:
            self.canvas.itemconfig(self.grid[row][col], fill="red")
            self.end_node = (row, col)
            self.grid_colors[row][col] = "red"
    
    def get_grid_coordinates(self, x, y):
        row = x // self.size
        col = y // self.size
        return int(row), int(col)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    n = simpledialog.askinteger("Input", "Enter grid size (n x n):")
    if n:
        root.deiconify()
        game = App(root, n)
        root.mainloop()
    else:
        messagebox.showinfo("Info", "Grid size is required to start the game.")