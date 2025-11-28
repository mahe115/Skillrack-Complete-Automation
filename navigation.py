import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from captcha_solver import monitor_Proceed_button_present
from type_code import auto_type_rough_code, auto_type_extracted_code, clicking_run_btn_twice,clicking_run_btn_once
from solution_extractor import solution_extraction,top_bottom_code_extraction,AI_response,description_extraction


first_container_button_class=None
solution_box_class=None
def navigate_code_editor(driver, navigate_choice, navigating_input_count):
    """Navigates based on the key pressed (0-9)."""
    print(f"🔄 Navigating to option {navigate_choice}...")
    global first_container_button_class
    global solution_box_class
    global Top_code_element_id
    global Bottom_code_element_id
    global description_text_id
    global AI_response_language

    try:
        if navigating_input_count == 1:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, f'pkglistform:cttbl:{navigate_choice}:j_id_3z'))).click()
            print(f"✅ Navigated to language option {navigate_choice}.")

            #Altering the solution box id for hands-On based on the language choose
            if navigate_choice==0:
                AI_response_language='C'
                solution_box_class='div#solnC'
            elif navigate_choice==1:
                AI_response_language='Java'
                solution_box_class='div#solnJava'
            elif navigate_choice==2:
                AI_response_language='Python'
                solution_box_class='div#solnPython'
            elif navigate_choice==3:
                AI_response_language='C++'
                solution_box_class='div#solnCPP'
            elif navigate_choice==4:
                AI_response_language='SQL'
                solution_box_class='div#solnSql'

        elif navigating_input_count == 2:
        
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, f'pkglistform:j_id_47:{navigate_choice}:j_id_4f'))).click()
            print(f"✅ Navigated to InnerTopic option {navigate_choice}.")

            if navigate_choice==0:
                Top_code_element_id='div#j_id_7a pre'
                Bottom_code_element_id='div#j_id_7g pre'
                description_text_id='div#j_id_58'#j_id_5a
            else:
                Top_code_element_id='div#j_id_8o pre'
                Bottom_code_element_id='div#j_id_8u pre'
                description_text_id='div#j_id_6m'#

        elif navigating_input_count == 3:
            if driver.find_elements('id','j_id_4i:cttbl:0:j_id_4q'):
                first_container_button_class=f'j_id_4i:cttbl:{navigate_choice}:j_id_4q'
            else:
                first_container_button_class=f'cttbl:{navigate_choice}:j_id_4u'
            print("first_container_button_class clicked:",first_container_button_class) 
            first_container_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, first_container_button_class)))
            driver.execute_script("arguments[0].click();", first_container_button)
            print("✅ First Container button Clicked.")
    except:
        print("❌ Invalid selection.")
    

        

def program_solution_algorithm(driver):
    """Handles the logic for extracting and running the solution."""

    print("🔍 Clicking the View Solution button...")
    view_solution_button = driver.find_elements(By.ID, 'showbtn')

    #checking if it is hands-On section by using run button id
    if driver.find_elements(By.ID, 'j_id_a3'): 
        run_button_id = 'j_id_a3'
        proceed_button_id = 'j_id_85'
    elif driver.find_elements(By.ID, 'j_id_bh'):
        run_button_id='j_id_bh'
        proceed_button_id='j_id_9j'
    else:
        run_button_id='j_id_bk'
    

    if view_solution_button:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "showbtn"))).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui button orange')]"))).click()

        clean_code = solution_extraction(driver, solution_box_class)

        #error handling for the case when the solution dialog box is not visible
        try:
            auto_type_extracted_code(clean_code, driver)

            clicking_run_btn_once(driver,run_button_id)

        except WebDriverException as e:
            print(f"❌ Typing interrupted! Restarting the program...")

        monitor_Proceed_button_present(driver,'showbtn','j_id_9j')

    else:
        auto_type_rough_code("print('hello world!')", driver)

        clicking_run_btn_twice(driver, run_button_id)

        
        print("🔍 Clicking the Solution button manually...")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_id_az")))
            print("👍 Solution button found! After Run twice")
        except TimeoutException:
            print("❌ Solution button not found! After Run twice")

        solution_button_check = driver.find_elements(By.ID, "j_id_az")
        if solution_button_check:
            try:
                solution_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "j_id_az")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", solution_button)
                time.sleep(1)
                solution_button.click()

                clean_code = solution_extraction(driver, 'div#solutionDialog_content')

                #checking if the Top or Bottom Section present
                if driver.find_elements(By.CSS_SELECTOR, Top_code_element_id) or driver.find_elements(By.CSS_SELECTOR, Bottom_code_element_id):
                    top,down=top_bottom_code_extraction(driver,Top_code_element_id,Bottom_code_element_id)
                    description=description_extraction(driver,description_text_id)

                    #Calculating the Total number of Request tokens to AI
                    #testing=top+down+description+clean_code
                    #Request_token=len(top.split())+len(down.split())+len(description.split())+len(clean_code.split())
                    #print(f"Total no.tokens:{Request_token}\n\n\n{testing}\n\n\n{testing.split()}\n\n\n{len(testing.split())}\n\n\n{len(testing)}")

                    Ai_solution=AI_response(description,top, down, clean_code,AI_response_language)
                    try:
                        auto_type_extracted_code(Ai_solution,driver)
                        clicking_run_btn_once(driver,run_button_id)
                    except WebDriverException as e:
                        print(f"❌ Typing interrupted! in AI Extraction with solution Restarting the program...")
                        
                else:
                    #error handling for the case when the solution dialog box is not visible
                    try:
                        auto_type_extracted_code(clean_code, driver)
                        clicking_run_btn_once(driver,run_button_id)
                    except WebDriverException as e:
                        print(f"❌ Typing interrupted! in Solution Extraction with solution Restarting the program...")
                    
            except Exception as e: #Exception Handling for solution button clicking
                print(f"❌ Failed to click Solution button: {e}")      

        elif not solution_button_check:
            try:
                if driver.find_elements(By.CSS_SELECTOR, Top_code_element_id) or driver.find_elements(By.CSS_SELECTOR, Bottom_code_element_id):
                    top,down=top_bottom_code_extraction(driver,Top_code_element_id,Bottom_code_element_id)
                else:
                    top,down = '',''

                clean_code = ''
                description=description_extraction(driver,description_text_id)

                #Calculating the Total number of Request tokens to AI
                Request_token=len(top.split())+len(down.split())+len(description.split())+len(clean_code.split())
                print(f"Total no.tokens:{Request_token}")
                
                Ai_solution=AI_response(description,top, down, clean_code,AI_response_language)
                try:
                    auto_type_extracted_code(Ai_solution,driver)
                    clicking_run_btn_once(driver,run_button_id)
                    
                except WebDriverException as e:
                    print(f"❌ Typing interrupted! in AI Extraction without solution Restarting the program...")
                    
            except Exception as e:
                print(f"❌ Failed to finish the solution-less problem: {e}")

        monitor_Proceed_button_present(driver,run_button_id,proceed_button_id)

   
