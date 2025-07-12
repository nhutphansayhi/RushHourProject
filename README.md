# Rush Hour Puzzle Solver

An interactive GUI application for solving the classic Rush Hour puzzle game with AI algorithms and step-by-step visualization.

## What is Rush Hour?

Rush Hour is a sliding puzzle game where you need to move vehicles on a 6x6 grid to help the targeted car escape through the exit. 

### Game Rules:
- Targeted car (X) must reach the exit on the right side of the grid (row 2)
- Vehicles can only move forward or backward in their orientation
- Horizontal vehicles move left/right, vertical vehicles move up/down
- Vehicles cannot overlap or move through each other
- Find the solution in the fewest moves possible

## How to Play

### Using the GUI:

1. **Select a Map**: Choose from 15 different puzzles using the dropdown or arrow buttons
2. **Pick an Algorithm**: Select your preferred solving method from the dropdown
3. **Solve the Puzzle**: Click "Solve Puzzle" to find the solution automatically
4. **Watch the Solution**: Use playback controls to see how the puzzle is solved step by step

### Playback Controls:
- **Reset**: Go back to the starting position
- **Previous**: Move one step backward
- **Play/Pause**: Automatically play through the solution
- **Next**: Move one step forward  
- **End**: Jump to the final solved state


## System Requirements

### Software Requirements:
- Python 3.7 or higher
- pip (Python package installer)

## Installation Guide

### Step 1: Install Python

#### Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and **check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### macOS:
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian):
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-tkinter

# Verify installation
python3 --version
pip3 --version
```

#### Linux (CentOS/RHEL):
```bash
# Install Python and pip
sudo yum install python3 python3-pip tkinter

# Or for newer versions
sudo dnf install python3 python3-pip python3-tkinter
```

### Step 2: Download the Project

#### Option A: Download ZIP
1. Go to the project repository on GitHub
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to your desired location

#### Option B: Use Git (if installed)
```bash
git clone https://github.com/nhutphansayhi/RushHourProject.git
cd RushHourProject
```

### Step 3: Install Dependencies

```bash
# Navigate to project directory
cd RushHourProject

# Install required packages
pip install Pillow

# For Linux users, you might need:
pip3 install Pillow
```

**Note**: `tkinter` is included with Python on Windows and macOS. Linux users should install it via their package manager (done in Step 1).

### Step 4: Verify Installation

Test if everything is working:

```bash
# Test Python and tkinter
python -c "import tkinter; print('Tkinter OK')"

# Test Pillow
python -c "import PIL; print('Pillow OK')"

# On Linux/Mac, you might need python3 instead of python
python3 -c "import tkinter; print('Tkinter OK')"
```

## Running the Application


### Windows:
```cmd
python main.py
```

### macOS/Linux:
```bash
python3 main.py
```


## Project Files

```
RushHourProject/
├── main.py              # Start the application
├── gui/                 # User interface files
├── solver/              # Algorithm files  
├── utils/               # Helper functions
├── map/                # Puzzle files (map1.txt to map15.txt)
├── images/              # Vehicle images (optional)
└── README.md            # This guide
```

## Getting Help

If you encounter problems:

1. **Check this README** for common solutions
2. **Restart the application** 
3. **Verify your Python installation**
4. **Check system requirements**
5. **Report issues** on the project repository

---
