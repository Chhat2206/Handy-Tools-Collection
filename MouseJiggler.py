import pyautogui
import tkinter as tk
import threading
import time

# Function to jiggle the mouse
def jiggle_mouse():
    while running_event.is_set():
        pyautogui.move(10, 0)  # Move mouse slightly to the right
        time.sleep(0.1)  # Small delay to avoid too many moves
        pyautogui.move(-10, 0)  # Move back to the original position
        time.sleep(0.1)

# Function to start the jiggler
def start_jiggler():
    global running_event
    running_event.set()  # Start the jiggler
    threading.Thread(target=jiggle_mouse, daemon=True).start()
    start_button.config(state=tk.DISABLED)  # Disable the start button while jiggling
    stop_button.config(state=tk.NORMAL)  # Enable the stop button

# Function to stop the jiggler
def stop_jiggler():
    running_event.clear()  # Stop the jiggler
    start_button.config(state=tk.NORMAL)  # Enable the start button
    stop_button.config(state=tk.DISABLED)  # Disable the stop button

# Setup the Tkinter window
window = tk.Tk()
window.title("Mouse Jiggler")

# Running event flag to control the jiggler thread
running_event = threading.Event()

# Create the start and stop buttons
start_button = tk.Button(window, text="Start Jiggler", command=start_jiggler)
start_button.pack(pady=10)

stop_button = tk.Button(window, text="Stop Jiggler", command=stop_jiggler, state=tk.DISABLED)
stop_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
