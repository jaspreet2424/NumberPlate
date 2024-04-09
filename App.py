import tkinter as tk
from tkinter import messagebox
import sys
import subprocess

def open_Camera_Function():
    try:
        subprocess.run(['python', 'number_plate.py'])
        sys.exit()
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def exit_gui():
    # Function to exit the GUI
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("AutoSecure Guardian")
root.geometry("640x380")

# Add a label for project heading
project_heading = tk.Label(root, text="AutoSecure Guardian", font=("Arial", 24, "bold"), fg="blue")
project_heading.pack(pady=20)

# Add subtitles
subtitle1 = tk.Label(root, text="Subtitle 1", font=("Arial", 16))
subtitle1.pack()
subtitle2 = tk.Label(root, text="Subtitle 2", font=("Arial", 16))
subtitle2.pack()

# Add buttons for further operations and exit
open_camera_button = tk.Button(root, text="Open Camera", command=open_Camera_Function, font=("Arial", 14), bg="green", fg="white", padx=10, pady=5)
open_camera_button.pack(pady=20)

exit_button = tk.Button(root, text="Exit", command=exit_gui, font=("Arial", 14), bg="red", fg="white", padx=10, pady=5)
exit_button.pack()

# Run the GUI
root.mainloop()
