#!/usr/bin/env python3
"""
Multi-Algorithm Rush Hour Solver Test Interface
Supports BFS, DFS, UCS, and A* search algorithms
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import sys
import os
import time
import threading
import tracemalloc

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.utils import import_map
from utils.state import State

from solver.bfs_solver import bfs_solver
from solver.dfs_solver import dfs_solver
from solver.ucs_solver import ucs
from solver.aStar_solver import aStar_solver

class MultiAlgorithmTestGUI:
    
    CELL_SIZE = 75  # tile size in pixels
    NUM_OF_MAPS = 15 # total testing maps
    
    def __init__(self, root):
        self.root = root
        self.root.title("Rush Hour Multi-Algorithm Solver - Test Interface")
        self.root.geometry("1200x800")
        
        # Variables
        self.current_state = None
        self.original_state = None
        self.solution_path = []
        self.current_step = 0
        self.is_running_test = False
        self.is_auto_playing = False
        
        # Available algorithms
        self.algorithms = {}
        if dfs_solver:
            self.algorithms['DFS'] = {'func': dfs_solver, 'name': 'Depth-First Search'}
        if bfs_solver:
            self.algorithms['BFS'] = {'func': bfs_solver, 'name': 'Breadth-First Search'}
        if ucs:
            self.algorithms['UCS'] = {'func': ucs, 'name': 'Uniform Cost Search'}
        if aStar_solver:
            self.algorithms['A*'] = {'func': aStar_solver, 'name': 'A* Search'}
        
        if not self.algorithms:
            messagebox.showerror("Error", "No solver algorithms found!")
            return
        
        self.image_refs = []
        
        # Colors for vehicles
        self.vehicle_colors = {
            'A': '#FF0000',  # Pure Red
            'B': '#0000FF',  # Pure Blue
            'C': '#00FF00',  # Pure Green
            'D': '#FFFF00',  # Pure Yellow
            'E': '#FF00FF',  # Pure Magenta
            'F': '#00FFFF',  # Pure Cyan
            'G': '#FF8000',  # Orange
            'H': '#8000FF',  # Purple
            'I': '#80FF00',  # Lime Green
            'J': '#FF0080',  # Hot Pink
            'K': '#0080FF',  # Azure
            'L': '#FF8080',  # Light Red
            'M': '#80FF80',  # Light Green
            'N': '#8080FF',  # Light Blue
            'O': '#FFFF80',  # Light Yellow
            'P': '#FF80FF',  # Light Magenta
            'Q': '#80FFFF',  # Light Cyan
            'R': '#FFA500',  # Gold
            'S': '#800080',  # Dark Purple
            'T': '#008000',  # Dark Green
            'U': '#800000',  # Maroon
            'V': '#000080',  # Navy
            'W': '#808000',  # Olive
            'X': '#DC143C',  # Crimson (Target vehicle)
            'Y': '#4B0082',  # Indigo
            'Z': '#2F4F4F',  # Dark Slate Gray
        }        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1) # thay đổi khi window resize
        main_frame.rowconfigure(2, weight=1) # sao lại là 2?
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Test Controls", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10)) # 0px padding trên và 10px dưới
        
        # First row of controls
        first_row = ttk.Frame(control_frame)
        first_row.grid(row=0, column=0, sticky="ew", pady=(0, 5)) # ???
        
        # Algorithm selection
        ttk.Label(first_row, text="Algorithm:").grid(row=0, column=0, padx=(0, 5))
        self.algorithm_var = tk.StringVar(value=list(self.algorithms.keys())[0] if self.algorithms else "") # lưu trữ tên thuật toán đã chọn
        self.algorithm_combo = ttk.Combobox(first_row, textvariable=self.algorithm_var, 
                                     values=list(self.algorithms.keys()), width=10, state="readonly")
        self.algorithm_combo.grid(row=0, column=1, padx=(0, 10))
        
        # Map selection
        ttk.Label(first_row, text="Map:").grid(row=0, column=2, padx=(0, 5))
        
        # Decrease button
        self.decrease_map_button = ttk.Button(first_row, text="←", width=2, command=self.decrease_map)
        self.decrease_map_button.grid(row=0, column=3, padx=(0, 2))

        # Map combobox
        self.map_var = tk.StringVar(value="")
        self.map_combo = ttk.Combobox(first_row, textvariable=self.map_var, values=[str(i) for i in range(1, self.NUM_OF_MAPS + 1)], width=5, state="readonly")
        self.map_combo.grid(row=0, column=4, padx=(0, 2))
        self.map_combo.bind("<<ComboboxSelected>>", lambda e: self.load_map())

        # Increase button
        self.increase_map_button = ttk.Button(first_row, text="→", width=2, command=self.increase_map)
        self.increase_map_button.grid(row=0, column=5, padx=(0, 10))
        
        # Test button
        self.test_button = ttk.Button(first_row, text="Solve Puzzle", command=self.test_map)
        self.test_button.grid(row=0, column=6, padx=(0, 10))
        
        # Clear results button
        self.clear_button = ttk.Button(first_row, text="Clear", command=self.clear_results)
        self.clear_button.grid(row=0, column=7, padx=(0, 10))
        
        # Second row of controls - Interactive Solution Controls
        second_row = ttk.Frame(control_frame)
        second_row.grid(row=1, column=0, sticky="ew", pady=(5, 5))
        
        ttk.Label(second_row, text="Solution Playback:").grid(row=0, column=0, padx=(0, 5))
        
        self.reset_button = ttk.Button(second_row, text="⏮ Reset", command=self.reset_to_start, state=tk.DISABLED)
        self.reset_button.grid(row=0, column=1, padx=(0, 5))
        
        self.prev_button = ttk.Button(second_row, text="⏪ Previous", command=self.previous_step, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=2, padx=(0, 5))
        
        self.play_button = ttk.Button(second_row, text="▶ Play", command=self.auto_play, state=tk.DISABLED)
        self.play_button.grid(row=0, column=3, padx=(0, 5))
        
        self.next_button = ttk.Button(second_row, text="⏩ Next", command=self.next_step, state=tk.DISABLED)
        self.next_button.grid(row=0, column=4, padx=(0, 5))
        
        self.end_button = ttk.Button(second_row, text="⏭ End", command=self.go_to_end, state=tk.DISABLED)
        self.end_button.grid(row=0, column=5, padx=(0, 5))
        
        # Step info
        self.step_label = ttk.Label(second_row, text="Step: 0/0", font=('Arial', 10))
        self.step_label.grid(row=0, column=6, padx=(20, 0))
        
        # Left Panel - Game Board
        board_frame = ttk.LabelFrame(main_frame, text="Rush Hour Board", padding="10")
        board_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Game grid
        self.canvas = tk.Canvas(board_frame, width=(6 + 2) * self.CELL_SIZE, height=(6 + 2) * self.CELL_SIZE)
        self.canvas.grid(row=0, column=0)
        
        ground = Image.open(os.path.join(current_dir,"images","ground.jpg")).resize((self.CELL_SIZE, self.CELL_SIZE))
        ground = ImageTk.PhotoImage(ground)
        self.image_refs.append(ground)
        
        road = Image.open(os.path.join(current_dir, "images","road.png")).resize((self.CELL_SIZE, self.CELL_SIZE))
        road = ImageTk.PhotoImage(road)
        self.image_refs.append(road)
        
        # Background
        for i in range(8):
            for j in range(8):
                self.canvas.create_image(self.CELL_SIZE * i, self.CELL_SIZE * j, anchor="nw", image=ground)
        
        # Top
        for i in range(1, 7):
            self.canvas.create_image(self.CELL_SIZE * i, 0, anchor="nw", image=road)
        
        # Left
        for i in range(8):
            self.canvas.create_image(0, self.CELL_SIZE * i, anchor="nw", image=road)
        self.canvas.create_image(0, self.CELL_SIZE * 3, anchor="nw", image=ground)
        
        # Right
        for i in range(8):
            self.canvas.create_image(self.CELL_SIZE * 7, self.CELL_SIZE * i, anchor="nw", image=road)
        self.canvas.create_image(self.CELL_SIZE * 7, self.CELL_SIZE * 3, anchor="nw", image=ground)
        
        # Bottom
        for i in range(1, 7):
            self.canvas.create_image(self.CELL_SIZE * i, self.CELL_SIZE * 7, anchor="nw", image=road)
        
        # Enter indicator
        enter_x = 0 * self.CELL_SIZE + self.CELL_SIZE // 2
        enter_y = 3 * self.CELL_SIZE + self.CELL_SIZE // 2
        self.canvas.create_text(enter_x, enter_y, text="→", font=('Arial', 24, 'bold'), fill='white', tags="static")
        
        # Exit indicator
        exit_x = 7 * self.CELL_SIZE + self.CELL_SIZE // 2
        exit_y = 3 * self.CELL_SIZE + self.CELL_SIZE // 2
        self.canvas.create_text(exit_x, exit_y, text="→", font=('Arial', 24, 'bold'), fill='white', tags="static")
        
        # Board info
        self.board_info_frame = ttk.Frame(board_frame)
        self.board_info_frame.grid(row=7, column=0, columnspan=7, sticky="ew", pady=(10, 0))
        
        self.status_label = ttk.Label(self.board_info_frame, text="Select a map to test", font=('Arial', 10))
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Right Panel - Test Results
        results_frame = ttk.LabelFrame(main_frame, text="Test Results", padding="10")
        results_frame.grid(row=1, column=1, sticky="nsew")
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, width=50, height=25, font=('Courier', 9))
        self.results_text.grid(row=0, column=0, sticky="nsew")
        
        # Configure results frame grid
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
    def increase_map(self):
        current = self.map_var.get()
        if not current.isdigit():
            self.map_var.set("1")
        else:
            num = int(current)
            if num < self.NUM_OF_MAPS:
                self.map_var.set(str(num + 1))
        self.load_map()

    def decrease_map(self):
        current = self.map_var.get()
        if not current.isdigit():
            self.map_var.set(str(self.NUM_OF_MAPS))
        else:
            num = int(current)
            if num > 1:
                self.map_var.set(str(num - 1))
        self.load_map()
       
    def update_board_display(self, state):
        """Update the visual display of the board"""
        
        # Clear previous vehicles
        self.canvas.delete("vehicle") # có nhãn để dễ delete
        
        if not state:
            return
        
        # Draw vehicles
        for vehicle in state.vehicles:
            color = self.vehicle_colors.get(vehicle.id, '#AAAAAA')
            positions = vehicle.get_occupied_possitions()
            if not positions:
                continue

            x0 = (positions[0][1] + 1) * self.CELL_SIZE
            y0 = (positions[0][0] + 1) * self.CELL_SIZE

            img = self.get_resized_car_image(vehicle)
            if img:
                self.canvas.create_image(x0, y0, anchor="nw", image=img, tags="vehicle")
                self.image_refs.append(img) # Prevent garbage collection 
            else:
                # fallback to rectangle if image missing
                if vehicle.orientation == 'H':
                    x1 = x0 + vehicle.length * self.CELL_SIZE
                    y1 = y0 + self.CELL_SIZE
                else:
                    x1 = x0 + self.CELL_SIZE
                    y1 = y0 + vehicle.length * self.CELL_SIZE
                
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black', tags="vehicle")
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=vehicle.id, font=("Arial", 16, "bold"), tags="vehicle")
                
    def get_resized_car_image(self, vehicle): # lấy ảnh xe và cả resize
        path = os.path.join(current_dir,"images",f"{vehicle.id}_{vehicle.length}_{vehicle.orientation}.png")
        try:
            image = Image.open(path)
            width = self.CELL_SIZE * vehicle.length if vehicle.orientation == 'H' else self.CELL_SIZE
            height = self.CELL_SIZE * vehicle.length if vehicle.orientation == 'V' else self.CELL_SIZE
            image = image.resize((width, height))
            return ImageTk.PhotoImage(image)
        except:
            print("Error loading image:", path)
            return None
    
    def log_result(self, message):
        """Add a message to the results text area"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def clear_results(self):
        # Clear the results text area
        self.results_text.delete(1.0, tk.END)
        
        # Reset to initial state
        self.current_state = self.original_state
        self.current_step = 0
        self.solution_path = []
        
        # Update GUI
        self.map_var.set("")
        self.status_label.config(text="Select a map to test")
        self.update_board_display(None)
        self._update_playback_controls()
        
    def cancel_solving(self):
        self.cancel_flag.set()
        self.clear_button.config(text="Cancelling...")
    
    def test_map(self):
        """Solve a map with the chosen algorithm"""
        if self.is_running_test:
            return
        
        map_id = int(self.map_var.get())
        self.is_running_test = True
        # self.test_button.config(state=tk.DISABLED)
        self._update_playback_controls()
        
        # Set up cancel flag and change Clear button to Cancel
        self.cancel_flag = threading.Event()
        self.clear_button.config(text="Cancel", command=self.cancel_solving, state=tk.NORMAL)
        
        # Run test in separate thread
        thread = threading.Thread(target=self._test_map_thread, args=(map_id,))
        thread.daemon = True
        thread.start()
    
    def _test_map_thread(self, map_id):
        """Thread function for testing the chosen map"""
        try:
            algorithm_name = self.algorithm_var.get()
            algorithm_info = self.algorithms.get(algorithm_name)
            
            if not algorithm_info:
                self.log_result(f" Algorithm '{algorithm_name}' not available")
                return
            
            self.log_result(f"{'='*60}")
            self.log_result(f"Testing Map {map_id} with {algorithm_info['name']}")
            
            # Load vehicles
            vehicles = import_map(map_id)
            if not vehicles:
                self.log_result(f" Failed to load map{map_id}.txt")
                return
            
            self.log_result(f"Loaded {len(vehicles)} vehicles:")
            for vehicle in vehicles:
                target_str = " (TARGET)" if vehicle.is_target else ""
                self.log_result(f"  {vehicle.id}: pos=({vehicle.row},{vehicle.col}), len={vehicle.length}, ori={vehicle.orientation}{target_str}")
            
            # Create initial state
            initial_state = State(vehicles)
            self.current_state = initial_state
            self.original_state = initial_state
            
            # Update GUI
            self.root.after(0, lambda: self.update_board_display(initial_state))
            self.root.after(0, lambda: self.status_label.config(text=f"Testing Map {map_id} with {algorithm_name}..."))
            
            # Check if already solved
            if initial_state.is_solved():
                self.log_result(" Puzzle is already solved!")
                self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: Already solved"))
                return
            
            # Run solver
            self.log_result(f" Running {algorithm_info['name']} solver...")
            
            tracemalloc.start()
            start_time = time.time()
            
            result = algorithm_info['func'](initial_state, cancel_flag=self.cancel_flag)
            end_time = time.time()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            solve_time = end_time - start_time
            
            if self.cancel_flag.is_set():
                self.log_result(" SOLVING CANCELED!")
                self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: Solving canceled"))
                return
            
            elif result and result[0] is not None:
                
                cost, nodes_expanded, path = result
                steps = len(path)
                
                # Store solution for interactive playback
                self.solution_path = path
                self.current_step = 0
                
                self.log_result(f" SOLUTION FOUND!")
                self.log_result(f"   Cost: {cost}")
                self.log_result(f"   Steps: {steps}")
                self.log_result(f"   Time: {solve_time:.3f} seconds")
                self.log_result(f"   Memory (peak): {peak / 1024:.2f} KB")
                
                if nodes_expanded is not None:
                    self.log_result(f"   Nodes expanded: {nodes_expanded}")
                
                # Create final state by applying all moves
                final_state = self._apply_solution_to_state(initial_state, path)
                
                self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: SOLVED with {algorithm_name} (Cost: {cost})"))
                
                # Enable interactive controls
                self.root.after(0, self._update_playback_controls)
                self.root.after(0, self._update_step_display)
                
                # Show solution path
                if steps <= 20:  # Show path for reasonable length solutions
                    self.log_result(f"\n Solution Path:")
                    for i, move in enumerate(path, 1):
                        if isinstance(move, tuple) and len(move) == 2:
                            vehicle_id, direction = move
                            self.log_result(f"   {i:2d}. Move '{vehicle_id}' {direction}")
                        else:
                            self.log_result(f"   {i:2d}. {move}")
                else:
                    self.log_result(f"\n Solution path has {steps} steps (too long to display)")
                
            else:
                self.log_result(f" NO SOLUTION FOUND")
                self.log_result(f"   Time: {solve_time:.3f} seconds")
                self.log_result(f"   Memory (peak): {peak / 1024:.2f} KB")
                self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: No solution with {algorithm_name}"))
            
        except Exception as e:
            self.log_result(f" ERROR: {str(e)}")
            self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: Error with {algorithm_name}"))
        
        finally:
            self.log_result(f"{'='*60}")
            self.root.after(0, self._test_complete)
    
    def _test_complete(self):
        """Called when testing is complete"""
        self.is_running_test = False
        self._update_playback_controls()
        
        # Restore the clear button
        self.clear_button.config(text="Clear", command=self.clear_results, state=tk.NORMAL)
    
    def load_map(self):
        """Load a map without solving it"""
        try:
            map_id = int(self.map_var.get())
            vehicles = import_map(map_id)
            
            if not vehicles:
                messagebox.showerror("Error", f"Could not load map{map_id}.txt")
                return
            
            # Create initial state
            initial_state = State(vehicles)
            self.current_state = initial_state
            self.original_state = initial_state
            self.solution_path = []
            self.current_step = 0
            
            # Update display
            self.update_board_display(initial_state)
            self.status_label.config(text=f"Map {map_id} loaded")
            self.step_label.config(text="Step: 0/0")
            self._update_playback_controls()
            
            current = int(self.map_var.get())
            self.decrease_map_button.config(state=tk.NORMAL if current > 1 else tk.DISABLED)
            self.increase_map_button.config(state=tk.NORMAL if current < self.NUM_OF_MAPS else tk.DISABLED)
            
            self.log_result(f"Map {map_id} loaded with {len(vehicles)} vehicles")
            
        except ValueError:
            messagebox.showerror("Error", "Please select a valid map number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {str(e)}")
    
    def reset_to_start(self):
        """Reset to the original state"""
        if self.original_state:
            self.current_state = self.original_state
            self.current_step = 0
            self.update_board_display(self.current_state)
            self._update_step_display()
            self._update_playback_controls()
            self.status_label.config(text="Reset to start")
    
    def previous_step(self):
        """Go to the previous step in the solution"""
        if self.solution_path and self.current_step > 0:
            self.current_step -= 1
            self._apply_solution_up_to_step()
            self._update_step_display()
            self._update_playback_controls()
    
    def next_step(self):
        """Go to the next step in the solution"""
        if self.solution_path and self.current_step < len(self.solution_path):
            self.current_step += 1
            self._apply_solution_up_to_step()
            self._update_step_display()
            self._update_playback_controls()
    
    def go_to_end(self):
        """Jump to the final state"""
        if self.solution_path:
            self.current_step = len(self.solution_path)
            self._apply_solution_up_to_step()
            self._update_step_display()
            self._update_playback_controls()
    
    def auto_play(self):
        """Auto-play through the solution"""
        if not self.solution_path or self.is_auto_playing:
            return
        
        if self.current_step >= len(self.solution_path):
            self.reset_to_start()
        
        self.is_auto_playing = True
        self._update_playback_controls()
        self.play_button.config(text="⏸ Pause", command=self.pause_auto_play)
        
        self._auto_play_step()
    
    def pause_auto_play(self):
        """Pause auto-play"""
        self.is_auto_playing = False
        self._update_playback_controls()
        
        self.play_button.config(text="▶ Play", command=self.auto_play)
    
    def _auto_play_step(self):
        """Execute one step of auto-play"""
        if not self.is_auto_playing or self.current_step >= len(self.solution_path):
            self.pause_auto_play()
            return
        
        self.next_step()
        self.root.after(1000, self._auto_play_step)  # 1 second delay
    
    def _apply_solution_up_to_step(self):
        """Apply solution moves up to the current step"""
        if not self.solution_path or not self.original_state:
            return
        
        current_state = self.original_state
        
        for i in range(self.current_step):
            if i < len(self.solution_path):
                vehicle_id, direction = self.solution_path[i]
                current_state = self._apply_move(current_state, vehicle_id, direction)
        
        self.current_state = current_state
        self.update_board_display(current_state)
    
    def _apply_move(self, state, vehicle_id, direction):
        """Apply a single move to a state and return the new state"""
        new_vehicles = []
        for vehicle in state.vehicles:
            if vehicle.id == vehicle_id:
                new_vehicle = vehicle.copy()
                if direction in ['up', 'UP']:
                    new_vehicle.row -= 1
                elif direction in ['down', 'DOWN']:
                    new_vehicle.row += 1
                elif direction in ['left', 'LEFT']:
                    new_vehicle.col -= 1
                elif direction in ['right', 'RIGHT']:
                    new_vehicle.col += 1
                new_vehicles.append(new_vehicle)
            else:
                new_vehicles.append(vehicle)
        
        return State(new_vehicles)
    
    def _apply_solution_to_state(self, initial_state, path):
        """Apply a solution path to get the final state"""
        current_state = initial_state
        for move in path:
            if isinstance(move, tuple) and len(move) == 2:
                vehicle_id, direction = move
                current_state = self._apply_move(current_state, vehicle_id, direction)
        return current_state
    
    def _update_step_display(self):
        """Update the step display label"""
        total_steps = len(self.solution_path)
        self.step_label.config(text=f"Step: {self.current_step}/{total_steps}")
    
    def _update_playback_controls(self):
        """Update the state of playback controls"""
        has_solution = bool(self.solution_path)
        at_start = self.current_step == 0
        at_end = self.current_step >= len(self.solution_path)
        current_map = int(self.map_var.get())
        
        # Enable/disable buttons based on state
        if self.is_running_test or self.is_auto_playing:
            self.algorithm_combo.config(state='disabled')
            self.increase_map_button.config(state=tk.DISABLED)
            self.map_combo.config(state='disabled')
            self.decrease_map_button.config(state=tk.DISABLED)
            self.test_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED if self.is_auto_playing else tk.NORMAL)
            self.reset_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
            self.play_button.config(state=tk.DISABLED if self.is_running_test else tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
            self.end_button.config(state=tk.DISABLED)
            
        else:
            self.algorithm_combo.config(state='readonly')
            self.increase_map_button.config(state=tk.NORMAL if current_map < self.NUM_OF_MAPS else tk.DISABLED)
            self.map_combo.config(state='readonly')
            self.decrease_map_button.config(state=tk.NORMAL if current_map > 1 else tk.DISABLED)
            self.test_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL if has_solution and not at_start else tk.DISABLED)
            self.prev_button.config(state=tk.NORMAL if has_solution and not at_start else tk.DISABLED)
            self.play_button.config(state=tk.NORMAL if has_solution and not at_end else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if has_solution and not at_end else tk.DISABLED)
            self.end_button.config(state=tk.NORMAL if has_solution and not at_end else tk.DISABLED)
