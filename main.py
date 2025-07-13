from gui.interface import MultiAlgorithmTestGUI
import tkinter as tk

def main():
    root = tk.Tk() # môt TK object đại diện cho cửa sổ chính của ứng dụng
    MultiAlgorithmTestGUI(root)
    root.mainloop()
  
if __name__ == "__main__":
    main()