import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from pynput.keyboard import Listener
from overlay2 import Overlay
from login import login, standard_navigation
from navigation import navigate_code_editor, program_solution_algorithm
from captcha_solver import solve_captcha
from typerman import TypermanOverlay  # Import TypermanOverlay




class UCL:
    """Handles the automation process include python exe login, navigation, and solution execution."""
    
    def __init__(self):
        """Initialize WebDriver with clipboard events disabled and Overlay UI."""
        firefox_options = Options()
        firefox_options.set_preference("dom.event.clipboardevents.enabled", False)  # Disable clipboard events

        """Initialize WebDriver and Overlay UI."""
        self.driver = webdriver.Firefox(options=firefox_options)
        self.overlay = Overlay()

        # Step 1: Login automatically (only runs once)
        login(self.driver,self.overlay)
         


    def wait_for_user_input(self,navigating_input_count):
        """Wait for a key (0-9) to be pressed and return the key."""

        match navigating_input_count:
            case 1:
                self.overlay.set_status("Keyboard-Options:\n0.C, 1.Java, 2.Python, 3.C++, 4.SQL")
            case 2:
                self.overlay.set_status("Select Track by Keyboard key\nFrom 0-9 Continue with A-P as 10-25")
            case 3:
                self.overlay.set_status("Press a key from (0-9) to navigate...")

        pressed_key = None
        def on_press(key):
            nonlocal pressed_key
            try:
                if key.char in ["0","1", "2", "3", "4", "5","6", "7", "8", "9"]:
                    pressed_key = int(key.char) # Convert string to integer
                    
                if navigating_input_count==2:
                    if key.char.lower() in "abcdefghijklmnop":  # **A-P Keys**
                        pressed_key = ord(key.char.lower()) - ord('a') + 10  # **Convert A=10, B=11, ..., P=25**
            
                if pressed_key is not None:
                    return False  # Stop listener once valid key is pressed

            except AttributeError:
                pass    

        with Listener(on_press=on_press) as listener:
            listener.join()

        self.overlay.set_status(f"Key {pressed_key} pressed. Navigating...")
        return pressed_key  


    def restart_program(self):
        """Runs `standard_navigation()` and restarts `main_program()`."""
        self.overlay.set_status("🚨 Restarting program...")
        print("🚨 Restarting program...")
        standard_navigation(self.driver)
        self.main_program()

    
    def main_program(self):
        """Automates the entire process with key-based navigation, restarting if necessary."""
        while True:  # Keep running indefinitely
            try:
                # Step 2: Continuously ask for navigation choices
                for navigating_input_count in range(1, 4):
                    try:
                        navigate_choice = self.wait_for_user_input(navigating_input_count)
                        navigate_error = navigate_code_editor(self.driver, navigate_choice, navigating_input_count)
                        if navigate_error:
                            self.restart_program()
                            break
                        time.sleep(0.3)
                        
                    except Exception:
                        self.restart_program()
                        break
                

                def inner_container_program():
                    """Handles solving CAPTCHA and clicking the first program button."""
                    try:
                        #checking if the first container present or not 
                        from navigation import first_container_button_class
                        if first_container_button_class == f'j_id_4i:cttbl:{navigate_choice}:j_id_4q':
                            print("✔️ First Module button Clicked.")
                            self.overlay.set_status("🔄 Solving CAPTCHA...")
                            solve_captcha(self.driver, 'j_id_5s')#captcha for hands-on programs
                        else:
                            first_program_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'pctbl:0:j_id_5w')))
                            self.driver.execute_script("arguments[0].click();", first_program_button)
                            print("✔️ First Program button Clicked.")
                            self.overlay.set_status("🔄 Solving CAPTCHA...")
                            solve_captcha(self.driver, 'j_id_76')#captcha for remaining programs

                        #Executing solution automation
                        program_solution_algorithm(self.driver,self.overlay)

                    except Exception as e:
                        print(f"❌ Inner Container Error: {e}")
                        self.restart_program()  # Restart if error occurs

                inner_container_program()

                # **Post-proceed-button check (Loop Restart)**
                while True:
                    try:
                        first_program_button = self.driver.find_elements(By.ID, 'pctbl:0:j_id_5w')
                        ace_editor = self.driver.find_elements(By.CLASS_NAME, "ace_editor")

                        #checking for next program is present or not
                        if not first_program_button and not ace_editor:
                            print("⚠️ First program button and ace_editor not found. Restarting...")
                            self.restart_program()
                        elif first_program_button and not ace_editor:
                            inner_container_program()
                        else:
                            program_solution_algorithm(self.driver,self.overlay)

                    except Exception as e:
                        print(f"❌ Main Loop Error: {e}")
                        self.restart_program() # Restart if error occurs main function

            except Exception as e:
                print(f"❌ Fatal Error: {e}")
                self.restart_program() #Reset the program if fatal error occurs
    

# Create an instance of the UCL class
ucl_instance = UCL()
typerman_instance = TypermanOverlay()


# Start main program in a separate thread
main_thread = threading.Thread(target=ucl_instance.main_program, daemon=True)
main_thread.start()
# Start `TypermanOverlay` in a separate thread
typerman_thread = threading.Thread(target=typerman_instance.start, daemon=True)
typerman_thread.start()

# Start overlay in the main thread
ucl_instance.overlay.start()

# Wait for both threads to finish
main_thread.join()
typerman_thread.join()
