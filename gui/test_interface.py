#!/usr/bin/env python3
"""
GUI Test Interface for UCS Rush Hour Solver
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import time
import threading

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.utils import import_map
from utils.state import State
from solver.ucs_solver import ucs

class UCSTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UCS Rush Hour Solver - Interactive Test Interface")
        self.root.geometry("1200x800")
        
        # Variables
        self.current_state = None
        self.original_state = None
        self.solution_path = []
        self.current_step = 0
        self.test_results = []
        self.is_running_test = False
        self.is_auto_playing = False
        self.selected_vehicle = None
        
        # Colors for vehicles
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
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Test Controls", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # First row of controls
        first_row = ttk.Frame(control_frame)
        first_row.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Map selection
        ttk.Label(first_row, text="Select Map:").grid(row=0, column=0, padx=(0, 5))
        self.map_var = tk.StringVar(value="1")
        map_combo = ttk.Combobox(first_row, textvariable=self.map_var, values=[str(i) for i in range(1, 13)], width=5)
        map_combo.grid(row=0, column=1, padx=(0, 10))
        
        # Load map button
        self.load_button = ttk.Button(first_row, text="Load Map", command=self.load_map)
        self.load_button.grid(row=0, column=2, padx=(0, 10))
        
        # Single test button
        self.test_button = ttk.Button(first_row, text="Solve with UCS", command=self.test_single_map)
        self.test_button.grid(row=0, column=3, padx=(0, 10))
        
        # Comprehensive test button
        self.comp_test_button = ttk.Button(first_row, text="Run All Tests", command=self.run_comprehensive_tests)
        self.comp_test_button.grid(row=0, column=4, padx=(0, 10))
        
        # Clear results button
        ttk.Button(first_row, text="Clear Results", command=self.clear_results).grid(row=0, column=5, padx=(0, 10))
        
        # Second row of controls - Interactive Solution Controls
        second_row = ttk.Frame(control_frame)
        second_row.grid(row=1, column=0, sticky="ew", pady=(5, 5))
        
        ttk.Label(second_row, text="Solution Playback:").grid(row=0, column=0, padx=(0, 5))
        
        self.reset_button = ttk.Button(second_row, text="⏮ Reset", command=self.reset_to_start, state=tk.DISABLED)
        self.reset_button.grid(row=0, column=1, padx=(0, 5))
        
        self.prev_button = ttk.Button(second_row, text="⏪ Previous", command=self.previous_step, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=2, padx=(0, 5))
        
        self.play_button = ttk.Button(second_row, text="▶ Auto Play", command=self.auto_play, state=tk.DISABLED)
        self.play_button.grid(row=0, column=3, padx=(0, 5))
        
        self.next_button = ttk.Button(second_row, text="⏩ Next", command=self.next_step, state=tk.DISABLED)
        self.next_button.grid(row=0, column=4, padx=(0, 5))
        
        self.end_button = ttk.Button(second_row, text="⏭ End", command=self.go_to_end, state=tk.DISABLED)
        self.end_button.grid(row=0, column=5, padx=(0, 5))
        
        # Step info
        self.step_label = ttk.Label(second_row, text="Step: 0/0", font=('Arial', 10))
        self.step_label.grid(row=0, column=6, padx=(20, 0))
        
        # Third row - Manual controls
        third_row = ttk.Frame(control_frame)
        third_row.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        
        ttk.Label(third_row, text="Manual Control:").grid(row=0, column=0, padx=(0, 5))
        
        self.manual_up = ttk.Button(third_row, text="↑", command=lambda: self.manual_move('up'), state=tk.DISABLED, width=3)
        self.manual_up.grid(row=0, column=1, padx=2)
        
        self.manual_down = ttk.Button(third_row, text="↓", command=lambda: self.manual_move('down'), state=tk.DISABLED, width=3)
        self.manual_down.grid(row=0, column=2, padx=2)
        
        self.manual_left = ttk.Button(third_row, text="←", command=lambda: self.manual_move('left'), state=tk.DISABLED, width=3)
        self.manual_left.grid(row=0, column=3, padx=2)
        
        self.manual_right = ttk.Button(third_row, text="→", command=lambda: self.manual_move('right'), state=tk.DISABLED, width=3)
        self.manual_right.grid(row=0, column=4, padx=2)
        
        self.manual_reset = ttk.Button(third_row, text="Reset Manual", command=self.reset_manual, state=tk.DISABLED)
        self.manual_reset.grid(row=0, column=5, padx=(10, 0))
        
        self.selected_label = ttk.Label(third_row, text="Click a vehicle to select", font=('Arial', 9), foreground="gray")
        self.selected_label.grid(row=0, column=6, padx=(20, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, mode='indeterminate')
        self.progress_bar.grid(row=3, column=0, columnspan=6, sticky="ew", pady=(10, 0))
        
        # Left Panel - Game Board
        board_frame = ttk.LabelFrame(main_frame, text="Rush Hour Board", padding="10")
        board_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Game grid
        self.grid_buttons = []
        for row in range(6):
            button_row = []
            for col in range(6):
                btn = tk.Button(board_frame, width=4, height=2, font=('Arial', 12, 'bold'))
                btn.grid(row=row, column=col, padx=1, pady=1)
                button_row.append(btn)
            self.grid_buttons.append(button_row)
        
        # Exit indicator
        exit_label = tk.Label(board_frame, text="EXIT →", font=('Arial', 10, 'bold'), fg='red')
        exit_label.grid(row=2, column=6, padx=5)
        
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
        
        # Summary frame
        summary_frame = ttk.LabelFrame(results_frame, text="Summary", padding="5")
        summary_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        self.summary_label = ttk.Label(summary_frame, text="No tests run yet", font=('Arial', 9))
        self.summary_label.grid(row=0, column=0, sticky="w")
    
    def update_board_display(self, state):
        """Update the visual display of the board"""
        # Clear all buttons
        for row in range(6):
            for col in range(6):
                self.grid_buttons[row][col].config(
                    text='',
                    bg='lightgray',
                    relief=tk.RAISED
                )
        
        # Draw vehicles
        if state:
            for vehicle in state.vehicles:
                color = self.vehicle_colors.get(vehicle.id, '#CCCCCC')
                positions = vehicle.get_occupied_possitions()
                for row, col in positions:
                    if 0 <= row < 6 and 0 <= col < 6:
                        self.grid_buttons[row][col].config(
                            text=vehicle.id,
                            bg=color,
                            relief=tk.SOLID
                        )
    
    def log_result(self, message):
        """Add a message to the results text area"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.delete(1.0, tk.END)
        self.test_results = []
        self.summary_label.config(text="No tests run yet")
        self.status_label.config(text="Select a map to test")
        self.update_board_display(None)
    
    def test_single_map(self):
        """Test a single map"""
        if self.is_running_test:
            return
        
        map_id = int(self.map_var.get())
        self.is_running_test = True
        self.test_button.config(state=tk.DISABLED)
        self.comp_test_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        
        # Run test in separate thread
        thread = threading.Thread(target=self._test_single_map_thread, args=(map_id,))
        thread.daemon = True
        thread.start()
    
    def _test_single_map_thread(self, map_id):
        """Thread function for testing a single map"""
        try:
            self.log_result(f"{'='*60}")
            self.log_result(f"Testing Map {map_id}")
            self.log_result(f"{'='*60}")
            
            # Load vehicles
            vehicles = import_map(map_id)
            if not vehicles:
                self.log_result(f"❌ Failed to load map{map_id}.txt")
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
            self.root.after(0, lambda: self.status_label.config(text=f"Testing Map {map_id}..."))
            
            # Check if already solved
            if initial_state.is_solved():
                self.log_result("✅ Puzzle is already solved!")
                self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: Already solved"))
                return
            
            # Run solver
            self.log_result("🚀 Running UCS solver...")
            start_time = time.time()
            
            result = ucs(initial_state)
            end_time = time.time()
            solve_time = end_time - start_time
            
            if result[0] is not None:
                cost, final_state, path = result
                steps = len(path)
                
                # Store solution for interactive playback
                self.solution_path = path
                self.current_step = 0
                
                self.log_result(f"✅ SOLUTION FOUND!")
                self.log_result(f"   Cost: {cost}")
                self.log_result(f"   Steps: {steps}")
                self.log_result(f"   Time: {solve_time:.3f} seconds")
                
                # Update board to show final state
                self.root.after(0, lambda: self.update_board_display(final_state))
                self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: SOLVED (Cost: {cost}, Steps: {steps})"))
                
                # Enable interactive controls
                self.root.after(0, self._update_playback_controls)
                self.root.after(0, self._update_step_display)
                self.root.after(0, self._make_vehicles_clickable)
                
                # Show solution path
                if steps <= 20:  # Show path for reasonable length solutions
                    self.log_result(f"\n📋 Solution Path:")
                    for i, (vehicle_id, direction) in enumerate(path, 1):
                        self.log_result(f"   {i:2d}. Move '{vehicle_id}' {direction}")
                else:
                    self.log_result(f"\n📋 Solution path has {steps} steps (too long to display)")
                
                # Store result
                self.test_results.append({
                    'map_id': map_id,
                    'success': True,
                    'cost': cost,
                    'steps': steps,
                    'time': solve_time
                })
                
            else:
                self.log_result(f"❌ NO SOLUTION FOUND")
                self.log_result(f"   Time: {solve_time:.3f} seconds")
                self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: No solution"))
                
                self.test_results.append({
                    'map_id': map_id,
                    'success': False,
                    'time': solve_time
                })
            
        except Exception as e:
            self.log_result(f"💥 ERROR: {str(e)}")
            self.root.after(0, lambda: self.status_label.config(text=f"Map {map_id}: Error"))
        
        finally:
            # Re-enable buttons
            self.root.after(0, self._test_complete)
    
    def run_comprehensive_tests(self):
        """Run tests on multiple maps"""
        if self.is_running_test:
            return
        
        self.is_running_test = True
        self.test_button.config(state=tk.DISABLED)
        self.comp_test_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        
        # Run tests in separate thread
        thread = threading.Thread(target=self._comprehensive_tests_thread)
        thread.daemon = True
        thread.start()
    
    def _comprehensive_tests_thread(self):
        """Thread function for comprehensive testing"""
        try:
            self.log_result(f"🚀 Starting Comprehensive UCS Tests")
            self.log_result(f"{'='*80}")
            
            test_maps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Test maps 1-10
            successful_tests = 0
            total_cost = 0
            total_steps = 0
            total_time = 0
            
            for map_id in test_maps:
                # Check if map file exists
                vehicles = import_map(map_id)
                if not vehicles:
                    self.log_result(f"Map {map_id}: ⚠️  File not found")
                    continue
                
                self.log_result(f"\nTesting Map {map_id}...")
                self.root.after(0, lambda mid=map_id: self.status_label.config(text=f"Testing Map {mid}..."))
                
                try:
                    # Create state and solve
                    initial_state = State(vehicles)
                    self.root.after(0, lambda: self.update_board_display(initial_state))
                    
                    start_time = time.time()
                    result = ucs(initial_state)
                    end_time = time.time()
                    solve_time = end_time - start_time
                    total_time += solve_time
                    
                    if result[0] is not None:
                        cost, final_state, path = result
                        steps = len(path)
                        successful_tests += 1
                        total_cost += cost
                        total_steps += steps
                        
                        self.log_result(f"Map {map_id}: ✅ SOLVED (Cost: {cost}, Steps: {steps}, Time: {solve_time:.3f}s)")
                        
                        self.test_results.append({
                            'map_id': map_id,
                            'success': True,
                            'cost': cost,
                            'steps': steps,
                            'time': solve_time
                        })
                    else:
                        self.log_result(f"Map {map_id}: ❌ NO SOLUTION (Time: {solve_time:.3f}s)")
                        self.test_results.append({
                            'map_id': map_id,
                            'success': False,
                            'time': solve_time
                        })
                
                except Exception as e:
                    self.log_result(f"Map {map_id}: 💥 ERROR - {str(e)}")
            
            # Summary
            self.log_result(f"\n{'='*80}")
            self.log_result(f"🏁 TEST SUMMARY")
            self.log_result(f"{'='*80}")
            self.log_result(f"Maps tested: {len([r for r in self.test_results if r.get('map_id') in test_maps])}")
            self.log_result(f"Successful solutions: {successful_tests}")
            self.log_result(f"Total time: {total_time:.3f} seconds")
            
            if successful_tests > 0:
                avg_cost = total_cost / successful_tests
                avg_steps = total_steps / successful_tests
                avg_time = total_time / len(test_maps)
                self.log_result(f"Average cost: {avg_cost:.2f}")
                self.log_result(f"Average steps: {avg_steps:.2f}")
                self.log_result(f"Average time per map: {avg_time:.3f}s")
                
                summary_text = f"Tested {len(test_maps)} maps, {successful_tests} solved successfully"
                self.root.after(0, lambda: self.summary_label.config(text=summary_text))
            
        except Exception as e:
            self.log_result(f"💥 Comprehensive test error: {str(e)}")
        
        finally:
            self.root.after(0, self._test_complete)
    
    def _test_complete(self):
        """Called when testing is complete"""
        self.is_running_test = False
        self.test_button.config(state=tk.NORMAL)
        self.comp_test_button.config(state=tk.NORMAL)
        self.progress_bar.stop()
    
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
            
            # Make vehicle buttons clickable for selection
            self._make_vehicles_clickable()
            
            # Enable manual controls
            self._update_manual_controls()
            
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
        self.play_button.config(text="⏸ Pause", command=self.pause_auto_play)
        self._auto_play_step()
    
    def pause_auto_play(self):
        """Pause auto-play"""
        self.is_auto_playing = False
        self.play_button.config(text="▶ Auto Play", command=self.auto_play)
    
    def _auto_play_step(self):
        """Execute one step of auto-play"""
        if not self.is_auto_playing or self.current_step >= len(self.solution_path):
            self.pause_auto_play()
            return
        
        self.next_step()
        self.root.after(1000, self._auto_play_step)  # 1 second delay
    
    def manual_move(self, direction):
        """Move the selected vehicle manually"""
        if not self.selected_vehicle or not self.current_state:
            return
        
        try:
            # Find the selected vehicle in current state
            vehicle_to_move = None
            for vehicle in self.current_state.vehicles:
                if vehicle.id == self.selected_vehicle:
                    vehicle_to_move = vehicle
                    break
            
            if not vehicle_to_move:
                return
            
            # Create a new state with the moved vehicle
            new_vehicles = []
            for vehicle in self.current_state.vehicles:
                if vehicle.id == self.selected_vehicle:
                    # Try to move this vehicle
                    new_vehicle = vehicle.copy()
                    if direction == 'up':
                        new_vehicle.row -= 1
                    elif direction == 'down':
                        new_vehicle.row += 1
                    elif direction == 'left':
                        new_vehicle.col -= 1
                    elif direction == 'right':
                        new_vehicle.col += 1
                    
                    # Check if move is valid
                    if self._is_valid_vehicle_position(new_vehicle, new_vehicles):
                        new_vehicles.append(new_vehicle)
                    else:
                        self.status_label.config(text="Invalid move!")
                        return
                else:
                    new_vehicles.append(vehicle)
            
            # Update current state
            new_state = State(new_vehicles)
            self.current_state = new_state
            self.update_board_display(new_state)
            
            # Check if solved
            if new_state.is_solved():
                self.status_label.config(text="🎉 SOLVED! Well done!")
                messagebox.showinfo("Congratulations!", "You solved the puzzle manually!")
            else:
                self.status_label.config(text=f"Moved {self.selected_vehicle} {direction}")
                
        except Exception as e:
            self.status_label.config(text=f"Move failed: {str(e)}")
    
    def reset_manual(self):
        """Reset manual changes"""
        if self.original_state:
            self.current_state = self.original_state
            self.selected_vehicle = None
            self.update_board_display(self.current_state)
            self.selected_label.config(text="Click a vehicle to select", foreground="gray")
            self.status_label.config(text="Manual changes reset")
            self._update_manual_controls()
    
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
    
    def _update_step_display(self):
        """Update the step display label"""
        total_steps = len(self.solution_path)
        self.step_label.config(text=f"Step: {self.current_step}/{total_steps}")
    
    def _update_playback_controls(self):
        """Update the state of playback controls"""
        has_solution = bool(self.solution_path)
        at_start = self.current_step == 0
        at_end = self.current_step >= len(self.solution_path)
        
        # Enable/disable buttons based on state
        self.reset_button.config(state=tk.NORMAL if has_solution and not at_start else tk.DISABLED)
        self.prev_button.config(state=tk.NORMAL if has_solution and not at_start else tk.DISABLED)
        self.play_button.config(state=tk.NORMAL if has_solution and not at_end else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if has_solution and not at_end else tk.DISABLED)
        self.end_button.config(state=tk.NORMAL if has_solution and not at_end else tk.DISABLED)
    
    def _make_vehicles_clickable(self):
        """Make vehicle buttons clickable for selection"""
        if not self.current_state:
            return
        
        # Add click handlers to grid buttons
        for row in range(6):
            for col in range(6):
                self.grid_buttons[row][col].config(
                    command=lambda r=row, c=col: self._on_vehicle_click(r, c)
                )
    
    def _on_vehicle_click(self, row, col):
        """Handle vehicle selection"""
        if not self.current_state:
            return
        
        # Find vehicle at this position
        for vehicle in self.current_state.vehicles:
            positions = vehicle.get_occupied_possitions()
            if (row, col) in positions:
                self.selected_vehicle = vehicle.id
                self.selected_label.config(
                    text=f"Selected: {vehicle.id}",
                    foreground="blue"
                )
                self._update_manual_controls()
                return
        
        # No vehicle at this position
        self.selected_vehicle = None
        self.selected_label.config(text="Click a vehicle to select", foreground="gray")
        self._update_manual_controls()
    
    def _update_manual_controls(self):
        """Update the state of manual control buttons"""
        has_selection = bool(self.selected_vehicle)
        state = tk.NORMAL if has_selection else tk.DISABLED
        
        self.manual_up.config(state=state)
        self.manual_down.config(state=state)
        self.manual_left.config(state=state)
        self.manual_right.config(state=state)
        self.manual_reset.config(state=tk.NORMAL if self.current_state and self.original_state else tk.DISABLED)
    
    def _is_valid_vehicle_position(self, vehicle, other_vehicles):
        """Check if a vehicle position is valid"""
        positions = vehicle.get_occupied_possitions()
        
        # Check bounds
        for row, col in positions:
            if row < 0 or row >= 6 or col < 0 or col >= 6:
                return False
        
        # Check collision with other vehicles  
        other_occupied_positions = set()
        for other_vehicle in other_vehicles:
            if other_vehicle.id != vehicle.id:
                other_positions = other_vehicle.get_occupied_possitions()
                for pos in other_positions:
                    other_occupied_positions.add(pos)
        
        # Check if any position conflicts
        for pos in positions:
            if pos in other_occupied_positions:
                return False
        
        return True

def main():
    root = tk.Tk()
    app = UCSTestGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
