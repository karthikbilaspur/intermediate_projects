import tkinter as tk
from gui import SudokuGUI

def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()