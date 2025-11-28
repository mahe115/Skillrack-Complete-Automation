import tkinter as tk
import queue

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep on top
        self.root.configure(bg="black")

        # Set initial position (Top-Right Corner)
        screen_width = self.root.winfo_screenwidth()
        self.width, self.height = 350, 80  # Overlay size
        self.x_pos = screen_width - self.width - 20  # 20px margin from right
        self.y_pos = 20  # 20px margin from top
        self.root.geometry(f"{self.width}x{self.height}+{self.x_pos}+{self.y_pos}")

        # Main Frame with Rounded Corners
        self.frame = tk.Frame(self.root, bg="black", bd=2, relief="solid")
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Label to display the status
        self.label = tk.Label(
            self.frame, text="Monitoring...", fg="white", bg="black",
            font=("Arial", 14, "bold"), padx=10, pady=5
        )
        self.label.pack(expand=True, fill="both")

        # Blinking effect
        self.blink_status = True
        self.blink()

        # Queue for real-time updates
        self.queue = queue.Queue()
        self.running = True
        self.root.after(100, self.update_status)  # Check for updates

        # Slide-in animation from the right
        self.slide_in()

    def blink(self):
        """Toggle text color to create a blinking effect."""
        self.label.config(fg="red" if self.label.cget("fg") == "white" else "white")
        self.root.after(500, self.blink)

    def update_status(self):
        """Check for real-time status updates from the queue."""
        while not self.queue.empty():
            new_status = self.queue.get()
            self.label.config(text=new_status)
        if self.running:
            self.root.after(100, self.update_status)  # Keep checking for updates

    def set_status(self, text):
        """Update overlay status from the main program."""
        self.queue.put(text)

    def slide_in(self):
        """Creates a slide-in animation effect from the right."""
        start_x = self.root.winfo_screenwidth()
        for i in range(20):  # Smooth animation
            self.root.geometry(f"{self.width}x{self.height}+{start_x - i * 20}+{self.y_pos}")
            self.root.update()
            self.root.after(10)

    def start(self):
        """Run the overlay window in the main loop."""
        self.root.mainloop()

    def stop(self):
        """Stop the overlay window."""
        self.running = False
        self.root.quit()
