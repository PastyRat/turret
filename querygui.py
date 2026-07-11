import tkinter as tk
from tkinter import simpledialog

def choicebetweenangles(angle1, angle2):
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # Create dialog window
    dialog = tk.Toplevel(root)
    dialog.title("Choose an angle")
    dialog.geometry("300x150")

    result = [None]

    tk.Label(dialog, text="Select an angle to fire at:").pack(pady=10)

    tk.Button(dialog, text=str(angle1), width=15, 
          command=lambda: [result.__setitem__(0, angle1), dialog.destroy()]).pack(pady=5)
    tk.Button(dialog, text=str(angle2), width=15, 
          command=lambda: [result.__setitem__(0, angle2), dialog.destroy()]).pack(pady=5)

    root.wait_window(dialog)

    root.destroy()
    return result[0]

if __name__ == "__main__": #tests
    angle1 = 0.44
    angle2 = 79.762
    print(choicebetweenangles(angle1, angle2))
