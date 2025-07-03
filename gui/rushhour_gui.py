import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import ast
from threading import Thread
import time

# Add the solver directory to the path and import functions
current_dir = os.path.dirname(os.path.abspath(__file__))
solver_dir = os.path.join(os.path.dirname(current_dir), 'solver')
if solver_dir not in sys.path:
    sys.path.insert(0, solver_dir)

# Import solver functions
ucs = None
display_map = None
load_map_from_file = None

def import_solver_functions():
    """Import solver functions at runtime"""
    global ucs, display_map, load_map_from_file
    try:
        import ucs_solver
        ucs = ucs_solver.ucs
        display_map = ucs_solver.display_map
        load_map_from_file = ucs_solver.load_map_from_file
        return True
    except ImportError as e:
        print(f"Error importing ucs_solver: {e}")
        return False

class RushHourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rush Hour Puzzle Solver")
        self.root.geometry("800x600")
        
        # Import solver functions
        if not import_solver_functions():
            messagebox.showerror("Error", "Failed to import solver functions. Please check that ucs_solver.py exists in the solver directory.")
            root.destroy()
            return
        
        # Game state
        self.current_state = None
        self.solution_path = []
        self.solution_index = 0
        self.is_solving = False
        
        # Colors for different vehicles
        self.vehicle_colors = {
            'A': '#FF4444',  # Red for target car
            'B': '#4444FF',  # Blue
            'C': '#44FF44',  # Green
            'D': '#FFFF44',  # Yellow
            'E': '#FF44FF',  # Magenta
            'F': '#44FFFF',  # Cyan
            'G': '#FF8844',  # Orange
            'H': '#8844FF',  # Purple
            'I': '#44FF88',  # Light Green
            'J': '#88FF44',  # Lime
        }
        
        self.create_widgets()
        self.load_default_map()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Load map button
        ttk.Button(control_frame, text="Load Map", command=self.load_map).grid(row=0, column=0, padx=(0, 5))
        
        # Solve button
        self.solve_button = ttk.Button(control_frame, text="Solve Puzzle", command=self.solve_puzzle)
        self.solve_button.grid(row=0, column=1, padx=5)
        
        # Reset button
        ttk.Button(control_frame, text="Reset", command=self.reset_puzzle).grid(row=0, column=2, padx=5)
        
        # Solution navigation buttons
        self.prev_button = ttk.Button(control_frame, text="← Previous", command=self.prev_step, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=3, padx=5)
        
        self.next_button = ttk.Button(control_frame, text="Next →", command=self.next_step, state=tk.DISABLED)
        self.next_button.grid(row=0, column=4, padx=5)
        
        # Auto play button
        self.auto_button = ttk.Button(control_frame, text="Auto Play", command=self.auto_play, state=tk.DISABLED)
        self.auto_button.grid(row=0, column=5, padx=5)
        
        # Game grid frame
        grid_frame = ttk.LabelFrame(main_frame, text="Rush Hour Grid", padding="10")
        grid_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Create 6x6 grid of buttons
        self.grid_buttons = []
        for row in range(6):
            button_row = []
            for col in range(6):
                btn = tk.Button(grid_frame, width=4, height=2, font=('Arial', 12, 'bold'))
                btn.grid(row=row, column=col, padx=1, pady=1)
                button_row.append(btn)
            self.grid_buttons.append(button_row)
        
        # Add exit indicator
        exit_label = tk.Label(grid_frame, text="EXIT →", font=('Arial', 10, 'bold'), fg='red')
        exit_label.grid(row=2, column=6, padx=5)
        
        # Info panel
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.grid(row=1, column=1, sticky="nsew")
        
        # Status label
        self.status_label = ttk.Label(info_frame, text="Ready to solve!", font=('Arial', 12))
        self.status_label.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Cost label
        self.cost_label = ttk.Label(info_frame, text="Cost: -", font=('Arial', 10))
        self.cost_label.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Step label
        self.step_label = ttk.Label(info_frame, text="Step: 0/0", font=('Arial', 10))
        self.step_label.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Vehicle info
        vehicle_info_frame = ttk.LabelFrame(info_frame, text="Vehicles", padding="5")
        vehicle_info_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        # Configure vehicle info frame grid weights
        vehicle_info_frame.columnconfigure(0, weight=1)
        vehicle_info_frame.rowconfigure(0, weight=1)
        
        self.vehicle_info_text = tk.Text(vehicle_info_frame, height=8, width=25, font=('Courier', 9))
        scrollbar = ttk.Scrollbar(vehicle_info_frame, orient=tk.VERTICAL, command=self.vehicle_info_text.yview)
        self.vehicle_info_text.configure(yscrollcommand=scrollbar.set)
        
        self.vehicle_info_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(info_frame, variable=self.progress_var, mode='indeterminate')
        self.progress_bar.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
    def load_default_map(self):
        """Load the default test map"""
        default_state = {
            'A': [(2, 1), (2, 2)],
            'B': [(0, 0), (0, 1), (0, 2)],
            'C': [(3, 0), (4, 0), (5, 0)]
        }
        self.current_state = default_state
        self.original_state = default_state.copy()
        self.update_display()
        
    def load_map(self):
        """Load a map from file"""
        map_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'map')
        filename = filedialog.askopenfilename(
            title="Select Map File",
            initialdir=map_dir,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                state = {}
                with open(filename, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            vehicle_id, positions_str = line.split(': ')
                            positions = ast.literal_eval(positions_str)
                            state[vehicle_id] = positions
                
                self.current_state = state
                self.original_state = state.copy()
                self.reset_solution()
                self.update_display()
                self.status_label.config(text=f"Loaded: {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load map: {str(e)}")
    
    def solve_puzzle(self):
        """Solve the current puzzle using UCS"""
        if self.is_solving:
            return
            
        self.is_solving = True
        self.solve_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.status_label.config(text="Solving puzzle...")
        
        # Run solver in separate thread
        Thread(target=self._solve_thread, daemon=True).start()
    
    def _solve_thread(self):
        """Thread function for solving"""
        try:
            if ucs is None:
                raise ImportError("UCS solver not available")
            result = ucs(self.current_state)
            
            # Update GUI in main thread
            self.root.after(0, self._solve_complete, result)
            
        except Exception as e:
            self.root.after(0, self._solve_error, str(e))
    
    def _solve_complete(self, result):
        """Handle solve completion"""
        self.is_solving = False
        self.solve_button.config(state=tk.NORMAL)
        self.progress_bar.stop()
        
        if len(result) == 3 and result[0] is not None:
            cost, final_state, path = result
            self.solution_path = [self.current_state] + path
            self.solution_index = 0
            self.cost_label.config(text=f"Cost: {cost}")
            self.step_label.config(text=f"Step: 1/{len(self.solution_path)}")
            self.status_label.config(text=f"Solution found! {len(path)} moves, cost: {cost}")
            
            # Enable navigation buttons
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
            self.auto_button.config(state=tk.NORMAL)
            
        else:
            self.status_label.config(text="No solution found!")
            messagebox.showinfo("No Solution", "This puzzle has no solution!")
    
    def _solve_error(self, error_msg):
        """Handle solve error"""
        self.is_solving = False
        self.solve_button.config(state=tk.NORMAL)
        self.progress_bar.stop()
        self.status_label.config(text="Error occurred while solving!")
        messagebox.showerror("Error", f"Failed to solve puzzle: {error_msg}")
    
    def reset_puzzle(self):
        """Reset puzzle to original state"""
        if hasattr(self, 'original_state'):
            self.current_state = self.original_state.copy()
            self.reset_solution()
            self.update_display()
            self.status_label.config(text="Puzzle reset!")
    
    def reset_solution(self):
        """Reset solution-related state"""
        self.solution_path = []
        self.solution_index = 0
        self.cost_label.config(text="Cost: -")
        self.step_label.config(text="Step: 0/0")
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.auto_button.config(state=tk.DISABLED)
    
    def prev_step(self):
        """Show previous step in solution"""
        if self.solution_path and self.solution_index > 0:
            self.solution_index -= 1
            self.current_state = self.solution_path[self.solution_index]
            self.update_display()
            self.step_label.config(text=f"Step: {self.solution_index + 1}/{len(self.solution_path)}")
    
    def next_step(self):
        """Show next step in solution"""
        if self.solution_path and self.solution_index < len(self.solution_path) - 1:
            self.solution_index += 1
            self.current_state = self.solution_path[self.solution_index]
            self.update_display()
            self.step_label.config(text=f"Step: {self.solution_index + 1}/{len(self.solution_path)}")
    
    def auto_play(self):
        """Automatically play through the solution"""
        if not self.solution_path:
            return
            
        self.auto_button.config(state=tk.DISABLED)
        self._auto_play_step()
    
    def _auto_play_step(self):
        """Single step of auto play"""
        if self.solution_index < len(self.solution_path) - 1:
            self.next_step()
            self.root.after(1000, self._auto_play_step)  # 1 second delay
        else:
            self.auto_button.config(state=tk.NORMAL)
            self.status_label.config(text="Auto play completed!")
    
    def update_display(self):
        """Update the visual display of the puzzle"""
        # Clear all buttons
        for row in range(6):
            for col in range(6):
                self.grid_buttons[row][col].config(
                    text='', 
                    bg='lightgray',
                    relief=tk.RAISED
                )
        
        # Draw vehicles
        if self.current_state:
            for vehicle_id, positions in self.current_state.items():
                color = self.vehicle_colors.get(vehicle_id, '#CCCCCC')
                for row, col in positions:
                    if 0 <= row < 6 and 0 <= col < 6:
                        self.grid_buttons[row][col].config(
                            text=vehicle_id,
                            bg=color,
                            relief=tk.SOLID
                        )
        
        # Update vehicle info
        self.update_vehicle_info()
    
    def update_vehicle_info(self):
        """Update vehicle information display"""
        self.vehicle_info_text.delete(1.0, tk.END)
        
        if self.current_state:
            info_text = ""
            for vehicle_id in sorted(self.current_state.keys()):
                positions = self.current_state[vehicle_id]
                length = len(positions)
                vehicle_type = "Car" if length == 2 else "Truck"
                orientation = "Horizontal" if positions[0][0] == positions[1][0] else "Vertical"
                
                info_text += f"{vehicle_id}: {vehicle_type} ({orientation})\n"
                info_text += f"   Positions: {positions}\n"
                info_text += f"   Length: {length}\n\n"
            
            # Add target car info
            if 'A' in self.current_state:
                target_pos = self.current_state['A']
                rightmost_col = max(pos[1] for pos in target_pos)
                info_text += f"Target Car 'A':\n"
                info_text += f"   Rightmost column: {rightmost_col}\n"
                info_text += f"   Needs to reach column ≥ 4\n"
                if rightmost_col >= 4:
                    info_text += "   ✓ GOAL REACHED!\n"
            
            self.vehicle_info_text.insert(1.0, info_text)

def main():
    root = tk.Tk()
    app = RushHourGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
