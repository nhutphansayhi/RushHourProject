#!/usr/bin/env python3
"""
Rush Hour GUI Launcher - Choose between Game and Test Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def launch_game_gui():
    """Launch the main Rush Hour game GUI"""
    try:
        from rushhour_gui import main
        selector.destroy()
        main()
    except ImportError as e:
        messagebox.showerror("Error", f"Failed to import game GUI: {e}")

def launch_test_gui():
    """Launch the UCS test interface"""
    try:
        from test_interface import main
        selector.destroy()
        main()
    except ImportError as e:
        messagebox.showerror("Error", f"Failed to import test GUI: {e}")

# Create selector window
selector = tk.Tk()
selector.title("Rush Hour - Select Interface")
selector.geometry("400x200")
selector.resizable(False, False)

# Center the window
selector.update_idletasks()
x = (selector.winfo_screenwidth() // 2) - (400 // 2)
y = (selector.winfo_screenheight() // 2) - (200 // 2)
selector.geometry(f"400x200+{x}+{y}")

# Main frame
main_frame = ttk.Frame(selector, padding="20")
main_frame.grid(row=0, column=0, sticky="nsew")

# Configure grid
selector.columnconfigure(0, weight=1)
selector.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)

# Title
title_label = ttk.Label(main_frame, text="Rush Hour Puzzle", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, pady=(0, 10))

subtitle_label = ttk.Label(main_frame, text="Choose an interface:", font=("Arial", 10))
subtitle_label.grid(row=1, column=0, pady=(0, 20))

# Buttons frame
buttons_frame = ttk.Frame(main_frame)
buttons_frame.grid(row=2, column=0, pady=10)

# Game GUI button
game_button = ttk.Button(
    buttons_frame, 
    text="🎮 Game Interface\n(Play Rush Hour)", 
    command=launch_game_gui,
    width=20
)
game_button.grid(row=0, column=0, padx=(0, 10))

# Test GUI button
test_button = ttk.Button(
    buttons_frame, 
    text="🧪 Test Interface\n(Test UCS Solver)", 
    command=launch_test_gui,
    width=20
)
test_button.grid(row=0, column=1, padx=(10, 0))

# Info label
info_label = ttk.Label(
    main_frame, 
    text="Game Interface: Interactive puzzle solving\nTest Interface: Automated UCS solver testing", 
    font=("Arial", 8),
    foreground="gray"
)
info_label.grid(row=3, column=0, pady=(20, 0))

if __name__ == "__main__":
    selector.mainloop()
