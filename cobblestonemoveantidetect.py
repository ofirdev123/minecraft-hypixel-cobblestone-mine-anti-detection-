import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import pyautogui
import numpy as np
import win32gui  # Make sure to install pywin32 for this

# Global variables for controlling the state
running = False
paused = False
selected_window = None
holding_mouse = False  # New variable for holding the mouse button

# Function to get all open windows
def get_open_windows():
    def enum_windows(hwnd, windows):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    windows = []
    win32gui.EnumWindows(enum_windows, windows)
    return windows

# Function to move mouse based on its current position within a small range
def move_mouse_based_on_position():
    global selected_window
    if selected_window is None:
        print("No window selected!")
        return

    # Get window rect of the selected Minecraft window
    window_rect = win32gui.GetWindowRect(selected_window)

    x, y = pyautogui.position()  # Get the current mouse position
    movement_range = movement_range_var.get()  # Movement range

    # Calculate new position while staying within the selected window's bounds
    new_x = max(window_rect[0], min(x + random.randint(-movement_range, movement_range), window_rect[2] - 1))
    new_y = max(window_rect[1], min(y + random.randint(-movement_range, movement_range), window_rect[3] - 1))

    # Get random duration between the specified min and max
    min_duration = min_duration_var.get()
    max_duration = max_duration_var.get()
    duration = random.uniform(min_duration, max_duration)  # Random float duration

    pyautogui.moveTo(new_x, new_y, duration=duration)  # Move to the new position smoothly

    # Hold left mouse button if enabled
    if holding_mouse:
        pyautogui.mouseDown()  # Press the mouse button down
    else:
        pyautogui.mouseUp()  # Release the mouse button

# Main function to run mouse movement
def run_program():
    global running, paused
    running = True

    while running:
        if not paused:
            move_mouse_based_on_position()  # Move based on current position
            
            # Get random delay between minimum and maximum
            min_delay = min_delay_var.get()
            max_delay = max_delay_var.get()
            random_delay = random.randint(min_delay, max_delay)  # Generate new random delay
            print(f"Moving in {random_delay} seconds")  # Optional: print the delay for debugging
            time.sleep(random_delay)  # Wait for the random delay before the next movement
        time.sleep(1)  # Run at 1-second intervals

# GUI functions
def start_program():
    global running
    if not running:
        threading.Thread(target=run_program, daemon=True).start()

def stop_program():
    global running
    running = False

def pause_program():
    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")

def toggle_mouse_hold():
    global holding_mouse
    holding_mouse = not holding_mouse
    mouse_hold_button.config(text="Hold Mouse: ON" if holding_mouse else "Hold Mouse: OFF")

def select_window(event):
    global selected_window
    selected_window = window_combobox.get()  # Get selected window name
    selected_window_hwnd = next((hwnd for hwnd, name in open_windows if name == selected_window), None)
    if selected_window_hwnd:
        selected_window = selected_window_hwnd

# Retrieve all open windows for the dropdown
open_windows = get_open_windows()
window_names = [name for hwnd, name in open_windows]

# Create GUI
root = tk.Tk()
root.title("Cobblestone Detection and Mouse Control")

# Window Selection
ttk.Label(root, text="Select Minecraft Window:").grid(row=0, column=0, padx=10, pady=10)
window_combobox = ttk.Combobox(root, values=window_names)
window_combobox.grid(row=0, column=1, padx=10, pady=10)
window_combobox.bind("<<ComboboxSelected>>", select_window)

# Start/Stop Buttons
start_button = ttk.Button(root, text="Start", command=start_program)
start_button.grid(row=1, column=0, padx=10, pady=10)

pause_button = ttk.Button(root, text="Pause", command=pause_program)
pause_button.grid(row=1, column=1, padx=10, pady=10)

stop_button = ttk.Button(root, text="Stop", command=stop_program)
stop_button.grid(row=1, column=2, padx=10, pady=10)

# Toggle Mouse Hold Button
mouse_hold_button = ttk.Button(root, text="Hold Mouse: OFF", command=toggle_mouse_hold)
mouse_hold_button.grid(row=1, column=3, padx=10, pady=10)

# Minimum and Maximum Delay Input
ttk.Label(root, text="Min Random Delay (s):").grid(row=2, column=0, padx=10, pady=10)
min_delay_var = tk.IntVar(value=1)  # Default min delay
min_delay_entry = ttk.Entry(root, textvariable=min_delay_var)
min_delay_entry.grid(row=2, column=1)

ttk.Label(root, text="Max Random Delay (s):").grid(row=3, column=0, padx=10, pady=10)
max_delay_var = tk.IntVar(value=5)  # Default max delay
max_delay_entry = ttk.Entry(root, textvariable=max_delay_var)
max_delay_entry.grid(row=3, column=1)

# Mouse Movement Range Input
ttk.Label(root, text="Mouse Movement Range:").grid(row=4, column=0, padx=10, pady=10)
movement_range_var = tk.IntVar(value=10)  # Default movement range
movement_range_entry = ttk.Entry(root, textvariable=movement_range_var)
movement_range_entry.grid(row=4, column=1)

# Minimum and Maximum Duration Input
ttk.Label(root, text="Min Movement Duration (s):").grid(row=5, column=0, padx=10, pady=10)
min_duration_var = tk.DoubleVar(value=0.05)  # Default min duration
min_duration_entry = ttk.Entry(root, textvariable=min_duration_var)
min_duration_entry.grid(row=5, column=1)

ttk.Label(root, text="Max Movement Duration (s):").grid(row=6, column=0, padx=10, pady=10)
max_duration_var = tk.DoubleVar(value=0.2)  # Default max duration
max_duration_entry = ttk.Entry(root, textvariable=max_duration_var)
max_duration_entry.grid(row=6, column=1)

# Start the GUI loop
root.mainloop()

# Clean up
cv2.destroyAllWindows()
