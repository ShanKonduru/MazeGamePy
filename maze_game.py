import tkinter as tk

class MazeGame(tk.Tk):
    def __init__(self, maze_size=10):
        super().__init__()
        
        self.title("Maze Game")
        
        # Maze parameters
        self.maze_size = maze_size
        self.maze = [
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
        self.start_pos = (0, 0)
        self.end_pos = (9, 9)
        self.current_pos = self.start_pos
        
        # Create maze canvas
        self.maze_canvas = tk.Canvas(self, width=400, height=400)
        self.maze_canvas.pack(side=tk.LEFT)
        self.draw_maze()
        
        # Create control panels
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.direction_frame = tk.Frame(self.control_frame)
        self.direction_frame.pack(pady=20)
        
        self.instruction_frame = tk.Frame(self.control_frame)
        self.instruction_frame.pack()
        
        # Direction buttons
        directions = [("Up", 0, -1), ("Down", 0, 1), ("Left", -1, 0), ("Right", 1, 0)]
        for direction, dx, dy in directions:
            tk.Button(self.direction_frame, text=direction, command=lambda dx=dx, dy=dy: self.move(dx, dy)).pack(side=tk.LEFT, padx=10)
        
        # Instruction grid
        tk.Label(self.instruction_frame, text="Instructions:").pack()
        self.instruction_entry = tk.Entry(self.instruction_frame)
        self.instruction_entry.pack(pady=10)
        tk.Button(self.instruction_frame, text="Execute", command=self.execute_instruction).pack()
        
    def draw_maze(self):
        cell_size = 40
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                if self.maze[y][x] == 1:
                    self.maze_canvas.create_rectangle(x*cell_size, y*cell_size, (x+1)*cell_size, (y+1)*cell_size, fill="white")
        
        self.maze_canvas.create_rectangle(self.start_pos[0]*cell_size, self.start_pos[1]*cell_size,
                                          (self.start_pos[0]+1)*cell_size, (self.start_pos[1]+1)*cell_size, fill="green")
        self.maze_canvas.create_rectangle(self.end_pos[0]*cell_size, self.end_pos[1]*cell_size,
                                          (self.end_pos[0]+1)*cell_size, (self.end_pos[1]+1)*cell_size, fill="red")
        
        self.object_id = self.maze_canvas.create_oval(self.start_pos[0]*cell_size+5, self.start_pos[1]*cell_size+5,
                                                      (self.start_pos[0]+1)*cell_size-5, (self.start_pos[1]+1)*cell_size-5, fill="blue")
        
    def move(self, dx, dy):
        new_x = self.current_pos[0] + dx
        new_y = self.current_pos[1] + dy
        
        if 0 <= new_x < self.maze_size and 0 <= new_y < self.maze_size and self.maze[new_y][new_x] == 1:
            cell_size = 40
            self.maze_canvas.move(self.object_id, dx*cell_size, dy*cell_size)
            self.current_pos = (new_x, new_y)
            
            if self.current_pos == self.end_pos:
                tk.messagebox.showinfo("Congratulations!", "You've reached the end of the maze!")
                self.current_pos = self.start_pos
                self.maze_canvas.coords(self.object_id, self.start_pos[0]*cell_size+5, self.start_pos[1]*cell_size+5,
                                        (self.start_pos[0]+1)*cell_size-5, (self.start_pos[1]+1)*cell_size-5)
    
    def execute_instruction(self):
        instruction = self.instruction_entry.get()
        parts = instruction.split()
        if len(parts) == 2:
            direction, steps = parts
            dx, dy = 0, 0
            if direction == "MoveLeft":
                dx = -int(steps)
            elif direction == "MoveRight":
                dx = int(steps)
            elif direction == "MoveUp":
                dy = -int(steps)
            elif direction == "MoveDown":
                dy = int(steps)
            
            self.move(dx, dy)
        else:
            tk.messagebox.showerror("Error", "Invalid instruction format. Use 'MoveLeft', 'MoveRight', 'MoveUp', or 'MoveDown' followed by a number.")
        
        self.instruction_entry.delete(0, tk.END)

if __name__ == "__main__":
    game = MazeGame()
    game.mainloop()
