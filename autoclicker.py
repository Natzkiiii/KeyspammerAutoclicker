import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import threading
import keyboard  # Import the keyboard library

class AutoClicker:
    def __init__(self, root):

        hotkey = ""  # leave this blank.

        self.root = root
        self.root.title("Auto Clicker - 1.0.0.0")
        
        self.interval_label = ttk.Label(root, text="Interval (seconds):")
        self.interval_label.grid(column=0, row=0, padx=10, pady=10)
        
        self.interval_entry = ttk.Entry(root)
        self.interval_entry.grid(column=1, row=0, padx=10, pady=10)
        self.interval_entry.insert(0, '1')
        
        self.faster_mode_var = tk.BooleanVar()
        self.faster_mode_check = ttk.Checkbutton(root, text="Faster Mode", variable=self.faster_mode_var)
        self.faster_mode_check.grid(column=0, row=1, padx=10, pady=10)
        
        self.start_button = ttk.Button(root, text="Start", command=self.start_clicking)
        self.start_button.grid(column=0, row=2, padx=10, pady=10)
        
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_clicking)
        self.stop_button.grid(column=1, row=2, padx=10, pady=10)
        
        self.hotkey_label = ttk.Label(root, text="Hotkey:")
        self.hotkey_label.grid(column=0, row=3, padx=10, pady=10)
        
        self.hotkey_entry = ttk.Entry(root)
        self.hotkey_entry.grid(column=1, row=3, padx=10, pady=10)
        self.hotkey_entry.insert(0, hotkey)  # Default hotkey

        self.update_hotkey_button = ttk.Button(root, text="Update Hotkey", command=self.setup_hotkey)
        self.update_hotkey_button.grid(column=0, row=4, padx=10, pady=10)
        
        self.help_button = ttk.Button(root, text="Help", command=self.show_help)
        self.help_button.grid(column=1, row=4, padx=10, pady=10)
        
        self.footer_label = ttk.Label(root, text="from Natzki, with love", anchor='e')
        self.footer_label.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky='e')

        self.clicking = False
        self.thread = None

        self.setup_hotkey()

    def setup_hotkey(self):
        hotkey = self.hotkey_entry.get()
        if hotkey:  # Check if hotkey is not empty
            keyboard.add_hotkey(hotkey, self.start_clicking)

    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            self.thread = threading.Thread(target=self.click_mouse)
            self.thread.start()

    def stop_clicking(self):
        self.clicking = False
        if self.thread:
            self.thread.join()

    def click_mouse(self):
        try:
            while self.clicking:
                interval = float(self.interval_entry.get())
                if self.faster_mode_var.get():
                    interval = 1 / 60  # Assuming 60 FPS, so 1/60 seconds per frame
                pyautogui.click()
                time.sleep(interval)
        except Exception as e:
            print(f"Error: {e}")

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_text = (
            "Auto Clicker - 1.0.0.0\n\n"
            "Instructions:\n"
            "1. Set the interval between clicks in the 'Interval' field.\n"
            "   - If 'Faster Mode' is checked, the interval is set to 1/60 seconds.\n"
            "2. Enter a hotkey to start the clicking in the 'Hotkey' field. eg: 'f6', it works.\n"
            "3. Click 'Update Hotkey' to update the hotkey.\n"
            "4. Click 'Start' to begin clicking.\n"
            "5. Click 'Stop' to stop clicking.\n"
            "6. Click 'Help' to view this help window.\n"
        )
        help_label = ttk.Label(help_window, text=help_text, justify=tk.LEFT)
        help_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
