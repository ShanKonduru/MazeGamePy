import time
import tkinter as tk
from tkinter import messagebox
import pygame

class MazeGame(tk.Tk):
    def __init__(self, maze_size=10):
        super().__init__()

        self.dx, self.dy = 0, 0  # Initialize dx and dy

        self.root = tk.Tk()  # Initialize root window

        self.title("Maze Game")

        # Initialize pygame mixer
        pygame.mixer.init()

        # self.jackpot_sound = pygame.mixer.Sound("jackpot.wav")  # You can replace "jackpot.wav" with the path to your jackpot winning sound file

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
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        ]

        self.start_pos = (1, 0)
        self.end_pos = (8, 9)
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

        # Instruction grid
        tk.Label(self.instruction_frame, text="Instructions:").pack()
        self.instruction_entry = tk.Text(
            self.instruction_frame, width=50, height=10
        )  # Set width and height
        self.instruction_entry.pack(pady=10)

        execute_button = tk.Button(
            self.instruction_frame, text="Execute", command=self.execute_instruction
        )
        execute_button.pack(side=tk.LEFT, padx=5, pady=5)

        reset_button = tk.Button(
            self.instruction_frame, text="Reset", command=self.reset_game
        )
        reset_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Bind keyboard controls
        self.bind("<Up>", lambda event: self.move(0, -1))
        self.bind("<Down>", lambda event: self.move(0, 1))
        self.bind("<Left>", lambda event: self.move(-1, 0))
        self.bind("<Right>", lambda event: self.move(1, 0))

    def draw_maze(self):
        cell_size = 40
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                if self.maze[y][x] == 1:
                    self.maze_canvas.create_rectangle(
                        x * cell_size,
                        y * cell_size,
                        (x + 1) * cell_size,
                        (y + 1) * cell_size,
                        fill="white",
                    )

        self.maze_canvas.create_rectangle(
            self.start_pos[0] * cell_size,
            self.start_pos[1] * cell_size,
            (self.start_pos[0] + 1) * cell_size,
            (self.start_pos[1] + 1) * cell_size,
            fill="green",
        )
        self.maze_canvas.create_rectangle(
            self.end_pos[0] * cell_size,
            self.end_pos[1] * cell_size,
            (self.end_pos[0] + 1) * cell_size,
            (self.end_pos[1] + 1) * cell_size,
            fill="red",
        )

        self.object_id = self.maze_canvas.create_oval(
            self.start_pos[0] * cell_size + 5,
            self.start_pos[1] * cell_size + 5,
            (self.start_pos[0] + 1) * cell_size - 5,
            (self.start_pos[1] + 1) * cell_size - 5,
            fill="blue",
        )

    def move(self, dx, dy):
        new_x = self.current_pos[0] + dx
        new_y = self.current_pos[1] + dy

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
        self.destroy()  # Close the game window

    def execute_instruction(self):
        instructions = self.instruction_entry.get(
            "1.0", "end-1c"
        ).splitlines()  # Retrieve all text from Text widget and split by lines
        print(instructions)

        dx, dy = 0, 0

        for instruction in instructions:
            parts = instruction.split(" ")
            print(parts)

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
                    time.sleep(0.5)  # Sleep for 0.5 seconds

                    # Update the Tkinter main loop to refresh the canvas
                    self.root.update()

            else:
                print(f"Error with {instruction}")
                break  # Stop executing further instructions on error

        # self.instruction_entry.delete("1.0", "end")  # Clear the Text widget

    def reset_game(self):
        # Delete the object from the canvas
        self.maze_canvas.delete(self.object_id)

        # Reset the object position to the initial position
        self.current_pos = self.start_pos
        x, y = self.start_pos
        cell_size = 40
        self.object_id = self.maze_canvas.create_oval(
            x * cell_size,
            y * cell_size,
            (x + 1) * cell_size,
            (y + 1) * cell_size,
            fill="blue",
        )

        # Clear the instruction entry
        self.instruction_entry.delete("1.0", "end")

        # Reset dx, dy
        self.dx, self.dy = 0, 0

    def is_valid_position(self, x, y):
        # Check if the new position is within the maze boundaries and is a valid path (i.e., maze walls)
        if 0 <= x < self.maze_size and 0 <= y < self.maze_size and self.maze[y][x] == 1:
            return True
        else:
            return False


if __name__ == "__main__":
    game = MazeGame()
    game.mainloop()
