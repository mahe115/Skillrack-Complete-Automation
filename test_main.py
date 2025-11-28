import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pynput.keyboard import Listener
from overlay2 import Overlay
from login import login, standard_navigation
from navigation import navigate_code_editor, program_solution_algorithm
from captcha_solver import solve_captcha
from typerman import TypermanOverlay  # Import TypermanOverlay


class UCL:
    """Handles the automation process including Python execution, login, navigation, and solution execution."""

    def __init__(self):
        """Initialize WebDriver with clipboard events disabled and Overlay UI."""
        firefox_options = Options()
        firefox_options.set_preference("dom.event.clipboardevents.enabled", False)  # Disable clipboard events

        # Initialize WebDriver and Overlay UI
        self.driver = webdriver.Firefox(options=firefox_options)
        self.overlay = Overlay()

        # Step 1: Login automatically (only runs once)
        login(self.driver)

    def wait_for_user_input(self):
        """Wait for a key (0-9) to be pressed and return the key."""
        self.overlay.set_status("Press a key from (0-9) to navigate...")
        pressed_key = None

        def on_press(key):
            nonlocal pressed_key
            try:
                if key.char in ["0","1", "2", "3", "4", "5","6", "7", "8", "9","a","b","c","d","e","f","g"]:
                    pressed_key = key.char
                    return False  # Stop listener once key is pressed
            except AttributeError:
                pass    

        with Listener(on_press=on_press) as listener:
            listener.join()
            
        if pressed_key.isdigit():
            navigate_choice = int(pressed_key)
        else:
            navigate_choice = ord(pressed_key) - ord('a') + 10  # Convert 'a'-'g' to 10-16
            print("you clicked mmore than 9",navigate_choice)
        self.overlay.set_status(f"Key {pressed_key} pressed. Navigating...")
        return navigate_choice  # Convert string to integer


    def restart_program(self):
        """Runs `standard_navigation()` and restarts `main_program()`."""
        print("⚠ Restarting program...")
        standard_navigation(self.driver)
        self.main_program()

    def main_program(self):
        """Automates the entire process with key-based navigation, restarting if necessary."""
        while True:  # Keep running indefinitely
            try:
                for navigating_input_count in range(1, 4):
                    navigate_choice = self.wait_for_user_input()
                    navigate_code_editor(self.driver, navigate_choice, navigating_input_count)
                    time.sleep(0.3)

                def inner_container_program():
                    """Handles solving CAPTCHA and clicking the first program button."""
                    try:
                        from navigation import first_container_button_class
                        if first_container_button_class == f'j_id_4i:cttbl:{navigate_choice}:j_id_4q':
                            print("inside first container button class condition")
                            time.sleep(1)
                            solve_captcha(self.driver, 'j_id_5s')  # Captcha for hands-on programs
                        else:
                            first_program_button = self.driver.find_element(By.ID, 'pctbl:0:j_id_5w')
                            self.driver.execute_script("arguments[0].click();", first_program_button)
                            print("✅ First Program button Clicked.")
                            time.sleep(1)
                            solve_captcha(self.driver, 'j_id_76')  # Captcha for remaining programs

                        # Executing solution automation
                        program_solution_algorithm(self.driver)
                        print("✅ Program solution completed")

                    except Exception as e:
                        print(f"❌ Inner Container Error: {e}")
                        self.restart_program()  # Restart if error occurs

                inner_container_program()

                # **Post-proceed-button check (Loop Restart)**
                while True:
                    try:
                        first_program_button = self.driver.find_elements(By.ID, 'pctbl:0:j_id_5w')
                        ace_editor = self.driver.find_elements(By.CLASS_NAME, "ace_editor")

                        # Checking for the next program presence
                        if not first_program_button and not ace_editor:
                            print("⚠ First program button and ace_editor not found. Restarting...")
                            self.restart_program()
                        elif first_program_button and not ace_editor:
                            inner_container_program()
                        else:
                            program_solution_algorithm(self.driver)

                    except Exception as e:
                        print(f"❌ Main Loop Error: {e}")
                        self.restart_program()  # Restart if error occurs

            except Exception as e:
                print(f"❌ Fatal Error: {e}")
                self.restart_program()  # Reset the program if a fatal error occurs


# Create an instance of the UCL class
ucl_instance = UCL()
typerman_instance = TypermanOverlay()

# Start main program in a separate thread (UCL should be threaded)
main_thread = threading.Thread(target=ucl_instance.main_program, daemon=True)
main_thread.start()

# ✅ Run TypermanOverlay (Tkinter GUI) in the main thread
typerman_instance.start()  # No threading required
