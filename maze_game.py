import time
import tkinter as tk
from tkinter import messagebox
import pygame
import MazeGenerator
class MazeGame(tk.Tk):
    def __init__(self, maze_size=10):
        super().__init__()
        self.ManualMode = True
        self.AutomaticMode=False
        self.paused = False
        self.index = 0
        self.dx, self.dy = 0, 0  # Initialize dx and dy
        self.cell_size = 40
        self.instructions = []  # Initialize instructions list

        self.title("CodeQuest: Maze Adventures")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Maze parameters
        self.maze_size = maze_size
        maze_generator = MazeGenerator.MazeGenerator()
        self.maze  = maze_generator.get_random_maze()

        self.start_pos = self.find_position('B')
        print ( f"B position :{self.start_pos}")
        self.end_pos = self.find_position('E')
        print ( f"E position :{self.end_pos}")
        self.current_pos = self.start_pos

        # Create maze canvas
        self.maze_canvas = tk.Canvas(self, width=400, height=400)
        self.maze_canvas.pack(side=tk.LEFT)
        self.draw_maze()

        # Create control panels
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side=tk.RIGHT, padx=20, pady=20)
            
        self.instruction_frame = tk.Frame(self.control_frame)
        self.instruction_frame.pack()
    
        # Checkboxes for Manual and Automatic Modes
        self.manual_mode_var = tk.BooleanVar()
        self.manual_mode_checkbox = tk.Checkbutton(
            self.control_frame, text="Manual Mode", variable=self.manual_mode_var, font=("Arial", 14),
            command=self.checkbox_callback  # Bind callback function
        )
        self.manual_mode_checkbox.pack(pady=5)

        self.automatic_mode_var = tk.BooleanVar()
        self.automatic_mode_checkbox = tk.Checkbutton(
            self.control_frame, text="Automatic Mode", variable=self.automatic_mode_var, font=("Arial", 14),
            command=self.checkbox_callback  # Bind callback function
        )
        self.automatic_mode_checkbox.pack(pady=5)

        # Buttons
        self.execute_button = tk.Button(
            self.control_frame, text="Execute", command=self.execute_instruction, font=("Arial", 14)
        )
        self.execute_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.reset_button = tk.Button(
            self.control_frame, text="Reset", command=self.reset_game, font=("Arial", 14)
        )
        self.reset_button.pack(side=tk.RIGHT, padx=5, pady=5)

        tk.Label(self.instruction_frame, text="CodeQuest: Maze Adventures", font=("Arial", 14)).pack()
        # Instruction label and Text widget
        tk.Label(self.instruction_frame, text="Instructions:", font=("Arial", 14)).pack()
        self.instruction_entry = tk.Text(self.instruction_frame, width=50, height=15, font=("Arial", 14))
        self.instruction_entry.pack(pady=10)

        # Create a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.instruction_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Attach scrollbar to the Text widget
        self.scrollbar.config(command=self.instruction_entry.yview)

        # Bind the MouseWheel event to the Text widget
        self.instruction_entry.bind("<MouseWheel>", self.on_mousewheel)

        # Bind keyboard controls
        self.bind("<Up>", lambda event: self.move(0, -1))
        self.bind("<Down>", lambda event: self.move(0, 1))
        self.bind("<Left>", lambda event: self.move(-1, 0))
        self.bind("<Right>", lambda event: self.move(1, 0))

    def checkbox_callback(self):
        # Execute some code when any checkbox is checked
        if self.manual_mode_var.get():
            print("Manual Mode checked!")
            self.ManualMode = True
            self.AutomaticMode=False
            self.automatic_mode_var.set(False)
            self.create_oval()
        elif self.automatic_mode_var.get():
            print("Automatic Mode checked!")
            # Add your code for Automatic Mode here
            self.ManualMode = False
            self.AutomaticMode = True
            self.manual_mode_var.set(False)
            self.create_rectangle()

    def on_mousewheel(self, event):
        # Scroll the Text widget with the mouse wheel
        self.instruction_entry.yview_scroll(-1 * int(event.delta/120), "units")

    def find_position(self, marker):
        # Find the position of the given marker in the maze.
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == marker:
                    return x, y
        return None

    def move_left(self):
        self.instructions.append("Move Left 1")
        self.instruction_entry.insert(tk.END, "Move Left 1" + "\n")

    def move_right(self):
        self.instructions.append("Move Right 1")
        self.instruction_entry.insert(tk.END, "Move Right 1" + "\n")

    def move_up(self):
        self.instructions.append("Move Up 1")
        self.instruction_entry.insert(tk.END, "Move Up 1" + "\n")

    def move_down(self):
        self.instructions.append("Move Down 1")
        self.instruction_entry.insert(tk.END, "Move Down 1" + "\n")

    def draw_maze(self):
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                if self.maze[y][x] == 1:
                    self.maze_canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill="white",
                    )
                elif self.maze[y][x] == 'B':
                    self.maze_canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill="green",
                    )
                elif self.maze[y][x] == 'E':
                    self.maze_canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill="red",
                    )
        # Set background color of the canvas to pitch black
        self.maze_canvas.configure(bg="black")

        # self.create_oval(self, color="blue")
        # self.create_rectangle("pink")

    def create_rectangle(self, color="pink"):
        self.object_id = self.maze_canvas.create_rectangle(
            self.start_pos[0] * self.cell_size + 5,
            self.start_pos[1] * self.cell_size + 5,
            (self.start_pos[0] + 1) * self.cell_size - 5,
            (self.start_pos[1] + 1) * self.cell_size - 5,
            fill=color,
        )

    def create_oval(self, color ="blue"):
        self.object_id = self.maze_canvas.create_oval(
            self.start_pos[0] * self.cell_size + 5,
            self.start_pos[1] * self.cell_size + 5,
            (self.start_pos[0] + 1) * self.cell_size - 5,
            (self.start_pos[1] + 1) * self.cell_size - 5,
            fill=color,
        )

    def move(self, dx, dy):
        new_x = self.current_pos[0] + dx
        new_y = self.current_pos[1] + dy

        if(self.ManualMode):
            if(dx == 0 ):
                if(dy == -1 ):
                    self.move_up()
                elif (dy == 1 ):
                    self.move_down()
            elif(dx == -1 ):
                if(dy == 0 ):
                    self.move_left()
            elif (dx == 1 ):
                if(dy == 0 ):
                    self.move_right()

        if (
            0 <= new_x < self.maze_size
            and 0 <= new_y < self.maze_size
            and self.maze[new_y][new_x] == 1
        ):
            cell_size = 40
            self.maze_canvas.move(self.object_id, dx * cell_size, dy * cell_size)
            self.current_pos = (new_x, new_y)

            if self.current_pos == self.end_pos:
                self.end_game()  # Call end_game method to display message box and close the window

        elif self.current_pos != self.end_pos:  # Check if not at the end position
            print("Invalid move! @ " + f"New Position: ({new_x}, {new_y})")

    def end_game(self):
        tk.messagebox.showinfo("Congratulations!", "You WON!!!")
        self.enable_disable_buttons()
        # Clear the instruction entry
        self.instruction_entry.delete("1.0", "end")
        self.reset_game()

    def pause_game(self):
        self.paused = True
        self.execute_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)

    def enable_disable_buttons(self):
        if self.instructions.count == 0:
            self.execute_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
        else:
            self.execute_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def execute_instruction(self):
        self.instructions = self.instruction_entry.get("1.0", "end-1c").splitlines()
        self.execute_button.config(state=tk.DISABLED)
        self.paused = False
        self.execute_next_instruction()

    def continue_game(self):
        self.paused = False
        self.pause_button.config(state=tk.NORMAL)
        self.continue_button.config(state=tk.DISABLED)
        self.execute_next_instruction()

    def execute_next_instruction(self):
        dx, dy = 0, 0

        for index, instruction in enumerate(
            self.instructions
        ):  # Using enumerate to get index
            self.index = index  # Set index to the current iteration index

            if self.paused:
                return

            parts = instruction.split(" ")

            if len(parts) == 3 and (parts[0].lower() == "move"):
                direction = parts[
                    1
                ].lower()  # Convert direction to lowercase for consistent comparison
                steps = int(parts[2])

                for _ in range(steps):
                    if direction == "left":
                        self.move(-1, 0)
                    elif direction == "right":
                        self.move(1, 0)
                    elif direction == "up":
                        self.move(0, -1)
                    elif direction == "down":
                        self.move(0, 1)

                    # Add a delay between each move (e.g., 0.5 seconds)
                    time.sleep(0.25)  # Sleep for 0.5 seconds

                    # Update the Tkinter main loop to refresh the canvas
                    self.update()

                    # Highlight the executed instruction by changing the background color to green
                    self.highlight_instruction(index)
            elif (parts[0].lower() == "change"):
                if(parts[1].lower() == "shape"):
                    if(parts[2].lower() == "rectangle"):
                        self.create_rectangle(parts[3].lower())
                    elif (parts[2].lower() == "ovel"):
                        self.create_oval(parts[3].lower())
            else:
                print(f"Error with {instruction}")
                break  # Stop executing further instructions on error

    def reset_game(self):
        # Delete the object from the canvas
        self.maze_canvas.delete(self.object_id)

        # Reset the object position to the initial position
        self.current_pos = self.start_pos
        x, y = self.start_pos

        self.object_id = self.maze_canvas.create_oval(
            self.start_pos[0] * self.cell_size + 5,
            self.start_pos[1] * self.cell_size + 5,
            (self.start_pos[0] + 1) * self.cell_size - 5,
            (self.start_pos[1] + 1) * self.cell_size - 5,
            fill="blue",
        )

        # Clear the instruction entry
        self.instruction_entry.delete("1.0", "end")

        # Reset dx, dy
        self.dx, self.dy = 0, 0
        self.enable_disable_buttons()

    def highlight_instruction(self, index):
        # Get the start and end positions of the line to highlight
        start_index = f"{index + 1}.0"
        end_index = f"{index + 1}.end"

        # Change the background color of the line to green
        self.instruction_entry.tag_add("highlight", start_index, end_index)
        self.instruction_entry.tag_configure("highlight", background="green")

    def is_valid_position(self, x, y):
        # Check if the new position is within the maze boundaries and is a valid path (i.e., maze walls)
        if 0 <= x < self.maze_size and 0 <= y < self.maze_size and self.maze[y][x] == 1:
            return True
        else:
            return False

if __name__ == "__main__":
    game = MazeGame()
    game.mainloop()
