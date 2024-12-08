import ctypes
import tkinter as tk
import atexit

# Constants for the "SetThreadExecutionState" function
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

class KeepAwakeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keep Awake Toggle")
        self.keep_awake = False

        # Button to toggle keep awake
        self.toggle_button = tk.Button(root, text="Enable Keep Awake", command=self.toggle_keep_awake)
        self.toggle_button.pack(pady=20, padx=20)

        # Label to show the status
        self.status_label = tk.Label(root, text="Status: Disabled", fg="red")
        self.status_label.pack()

        # Ensure the system reverts to normal when the program exits or crashes
        atexit.register(self.disable_keep_awake)

    def toggle_keep_awake(self):
        if not self.keep_awake:
            self.enable_keep_awake()
        else:
            self.disable_keep_awake()

    def enable_keep_awake(self):
        """Enable keep awake mode."""
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
        self.keep_awake = True
        self.toggle_button.config(text="Disable Keep Awake")
        self.status_label.config(text="Status: Enabled", fg="green")

    def disable_keep_awake(self):
        """Disable keep awake mode."""
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        self.keep_awake = False
        self.toggle_button.config(text="Enable Keep Awake")
        self.status_label.config(text="Status: Disabled", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = KeepAwakeApp(root)
    root.mainloop()
