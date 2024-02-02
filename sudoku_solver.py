import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.grid_size = 9
        self.grid = [[tk.StringVar() for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                entry = tk.Entry(self.root, textvariable=self.grid[i][j], width=3, font=('Arial', 14, 'bold'), bd=1, relief="solid")
                entry.grid(row=i, column=j, padx=1, pady=1)
                entry.insert(0, '0')
                entry.config(fg="black")

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve Sudoku", command=self.solve_sudoku, bg="#4CAF50", fg="white", bd=1, padx=10, pady=5, font=('Arial', 12, 'bold'))
        solve_button.grid(row=self.grid_size + 1, column=0, columnspan=self.grid_size // 2, pady=10, sticky="ew")

        clear_button = tk.Button(self.root, text="Clear Grid", command=self.clear_grid, bg="#F44336", fg="white", bd=1, padx=10, pady=5, font=('Arial', 12, 'bold'))
        clear_button.grid(row=self.grid_size + 1, column=self.grid_size // 2, columnspan=self.grid_size // 2, pady=10, sticky="ew")

    def solve_sudoku(self):
        sudoku_solver = SudokuSolver(self.grid_size)

        # Populate the grid with user input
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                try:
                    value = int(self.grid[i][j].get())
                    if value < 0 or value > 9:
                        raise ValueError
                    sudoku_solver.grid[i][j] = value
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter integers between 0 and 9.")
                    return

        # Solve the Sudoku puzzle
        if not sudoku_solver.solve_sudoku():
            messagebox.showinfo("Info", "No solution exists for the provided Sudoku puzzle.")
            return

        # Display the solution in the GUI
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j].set(str(sudoku_solver.grid[i][j]))
                if sudoku_solver.initial_grid[i][j] == 0:
                    self.root.nametowidget(self.root.grid_slaves(row=i, column=j)[0]).config(fg="blue")

    def clear_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j].set('')
                self.root.nametowidget(self.root.grid_slaves(row=i, column=j)[0]).config(fg="black")

class SudokuSolver:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.initial_grid = None

    def solve_sudoku(self):
        self.initial_grid = [row[:] for row in self.grid]
        return self.solve()

    def solve(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True
        row, col = empty_cell
        for num in range(1, self.grid_size + 1):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0
        return False

    def is_safe(self, row, col, num):
        return (
            self.is_num_unique_in_row(row, num)
            and self.is_num_unique_in_col(col, num)
            and self.is_num_unique_in_box(row - row % int(self.grid_size ** 0.5), col - col % int(self.grid_size ** 0.5), num)
        )

    def is_num_unique_in_row(self, row, num):
        return num not in self.grid[row]

    def is_num_unique_in_col(self, col, num):
        return num not in [self.grid[row][col] for row in range(self.grid_size)]

    def is_num_unique_in_box(self, start_row, start_col, num):
        for i in range(int(self.grid_size ** 0.5)):
            for j in range(int(self.grid_size ** 0.5)):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty_cell(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return i, j
        return None

if __name__ == "__main__":
    root = tk.Tk()
    sudoku_gui = SudokuSolverGUI(root)
    root.mainloop()
