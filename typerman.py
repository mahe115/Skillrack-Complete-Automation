import tkinter as tk
import pyautogui
import time
import random

class TypermanOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        
        self.expanded = False  # Track state (collapsed/expanded)
        
        # Default size and position
        self.width, self.height = 400, 250
        self.x_pos, self.y_pos = 20, 20
        
        self.create_circle_overlay()
        
    def create_circle_overlay(self):
        """Creates the circular button overlay."""
        self.root.geometry("65x40+20+20")
        self.circle_button = tk.Button(
            self.root, text="Typerman", font=("Arial", 9 , "bold"),
            bg="red", fg="white", command=self.expand_overlay,
            width=4, height=3, relief="solid"
        )
        self.circle_button.pack(fill="both", expand=True)
    
    def expand_overlay(self):
        """Expands the overlay to show the text input and Type button."""
        self.circle_button.destroy()
        
        self.root.geometry(f"{self.width}x{self.height}+{self.x_pos}+{self.y_pos}")
        self.frame = tk.Frame(self.root, bg="black", bd=2, relief="solid")
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.title_label = tk.Label(self.frame, text="Paste the solution", fg="white", bg="black", font=("Arial", 12, "bold"))
        self.title_label.pack(fill="x", padx=10, pady=(5, 0))
        
        self.entry = tk.Text(self.frame, font=("Arial", 12), height=7.5)
        self.entry.pack(fill="x", padx=10, pady=5)
        
        self.button = tk.Button(self.frame, text="Type", command=self.auto_type_code, bg="red", fg="white", width=12)
        self.button.pack(pady=5)
        
        # Minimize Button (Top-right)
        self.minimize_button = tk.Button(self.frame, text="−", bg="gray", fg="white", font=("Arial", 10, "bold"),
                                         command=self.minimize_overlay, width=2)
        self.minimize_button.place(relx=0.93, rely=0.05)
        
    def minimize_overlay(self):
        """Minimizes the expanded overlay back to the circle button."""
        self.frame.destroy()
        self.create_circle_overlay()
    
    def auto_type_code(self):
        """Types the code with simulated human-like typing."""
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
        
        self.human_typing(code)
        print("✅ Code typed successfully.")
        
    def human_typing(self, text):
        """Simulates human-like typing."""
        text = "\n".join(line.lstrip() for line in text.splitlines())
        typo_chance = 0.05  # 5% chance of a typo
        for char in text:
            if random.random() < typo_chance and char.isalnum():
                pyautogui.write(random.choice("abcdefghijklmnopqrstuvwxyz0123456789"))
                time.sleep(random.uniform(0.15, 0.3))
                pyautogui.press("backspace")
                time.sleep(random.uniform(0.1, 0.2))
            pyautogui.write(char)
            time.sleep(random.uniform(0.05, 0.2))
        
    def start(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    typerman = TypermanOverlay()
    typerman.start()
