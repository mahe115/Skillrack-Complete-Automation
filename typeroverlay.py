import tkinter as tk
import pyautogui
import time
import random

def select_until_end(repeats=30):
    """Clears auto-created braces and brackets by selecting and deleting text."""
    pyautogui.hotkey("ctrl", "shift", "right")
    time.sleep(0.05)
    for _ in range(repeats - 1):
        pyautogui.press("right")
        time.sleep(0.05)
    pyautogui.press("delete")
    print("✅ The auto-created braces and brackets have been cleared.")

def human_typing(text):
    """Simulates human-like typing with typos and corrections."""
    typo_chance = 0.05  # 5% chance of a typo
    backspace_delay = random.uniform(0.15, 0.3)
    
    for char in text:
        if random.random() < typo_chance and char.isalnum():
            wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
            pyautogui.write(wrong_char)
            time.sleep(backspace_delay)
            pyautogui.press("backspace")
            time.sleep(random.uniform(0.1, 0.2))
        
        pyautogui.write(char)
        time.sleep(random.uniform(0.05, 0.2))
        
    select_until_end()

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg="black")
        
        
        # **Set overlay size**
        self.width, self.height = 400, 250  

        # **Top-Left Alignment (Fix)**
        self.x_pos = 20  # **Position it at the absolute left**
        self.y_pos = 20  # **Position it at the absolute top**
        
        self.root.geometry(f"{self.width}x{self.height}+{self.x_pos}+{self.y_pos}")
        
        self.frame = tk.Frame(self.root, bg="black", bd=2, relief="solid")
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.title_label = tk.Label(self.frame, text="Paste the solution", fg="white", bg="black", font=("Arial", 12, "bold"))
        self.title_label.pack(fill="x", padx=10, pady=(5, 0))
        
        self.entry = tk.Text(self.frame, font=("Arial", 12), height=7.5)
        self.entry.pack(fill="x", padx=10, pady=5)
        
        self.button = tk.Button(self.frame, text="Type", command=self.auto_type_code, bg="red", fg="white", width=12)
        self.button.pack(pady=5)
        
        
    def auto_type_code(self):
        """Clears unwanted characters and types the new code."""
        code = self.entry.get("1.0", "end-1c")
        if not code.strip():
            print("⚠️ No code to type!")
            return
        
        print("🔄 Auto-typing the code...")
        time.sleep(1)
        pyautogui.click()
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.2)
        pyautogui.press("backspace")
        time.sleep(0.5)
        
        human_typing(code)
        print("✅ Code typed successfully.")
    
    
    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    overlay = Overlay()
    overlay.start()
