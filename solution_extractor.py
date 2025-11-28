import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apicall import generate_code

#solution extraction
from bs4 import BeautifulSoup



def solution_extraction(driver,solution_extraction_class):
    
     # **Wait for the solution box to load**
    print("⏳ Waiting for solution to appear...")
    time.sleep(3)  # Increase if necessary

    """Extracts the solution code, closes the solution dialog, and types it into the editor."""
    print("📋 Extracting solution code...")
    try:
        solution_code_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, solution_extraction_class))
        )
        solution_code_raw_html = solution_code_element.get_attribute("outerHTML")

        # **Parse and Clean Code Using BeautifulSoup**
        solution_code_soup = BeautifulSoup(solution_code_raw_html, "html.parser")

        # **Extract text from `<pre>` tags while preserving formatting**
        all_class_in_solution_extraction = solution_code_soup.select(f"{solution_extraction_class} pre")
        
        all_text_in_solution_extraction = [element.get_text(strip=False) for element in all_class_in_solution_extraction]
        
        clean_code = "\n".join(all_text_in_solution_extraction).replace("&amp;", "&")  # Clean extracted code

        # **Remove leading indentation from each line**
        clean_code = "\n".join(line.lstrip() for line in clean_code.split("\n"))

        print(f"\n✅ Solution Code Extracted:\n{clean_code}")
  
    except Exception as e:
        print(f"❌ Failed to extract solution code: {e}")
        
        
    def solution_close_button(driver):
        # **Close Solution Section**
        try:
            solution_dialog = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "solutionDialog")))
            print("✅ Solution section is open.")

            close_button = driver.find_element(By.CLASS_NAME, "ui-dialog-titlebar-close")
            try:
                close_button.click()
                WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, "solutionDialog")))
            except:
                driver.execute_script("arguments[0].style.display = 'none';", solution_dialog)

            print("✅ Solution section closed successfully!")

        except:
            print("❌ Solution section is not open or already closed.")
    
    if solution_extraction_class == 'div#solutionDialog_content':
        print("🔍Clicking solution close button..")
        solution_close_button(driver)

    return clean_code


def top_bottom_code_extraction(driver,Top_code_element_id,Bottom_code_element_id):
    Top_clean_code=None
    Bottom_clean_code=None

    if driver.find_elements(By.ID, 'j_id_7a') or driver.find_elements(By.ID, 'j_id_8o'):
        #Extract Top Code
        try:
            Top_code_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Top_code_element_id)))
            Top_raw_html = Top_code_element.get_attribute("outerHTML")

            # **Parse and Clean Code Using BeautifulSoup**
            Top_soup = BeautifulSoup(Top_raw_html, "html.parser")
            Top_clean_code = Top_soup.get_text().replace("&amp;", "&")  # Clean extracted code

            print(f"\n✅ Top Section Code Extracted:\n{Top_clean_code}")

        except Exception as e:
            print(f"❌ Failed to extract Top Section code: {e}")
    else:
        print("\nTop section was Not Found\n")
        
        
    if driver.find_elements(By.ID, 'j_id_7g') or driver.find_elements(By.ID, 'j_id_8u'):
        #Extract Bottom Code
        try:
            Bottom_code_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Bottom_code_element_id)))
            Bottom_raw_html = Bottom_code_element.get_attribute("outerHTML")

            # **Parse and Clean Code Using BeautifulSoup**
            Bottom_soup = BeautifulSoup(Bottom_raw_html, "html.parser")
            Bottom_clean_code = Bottom_soup.get_text().replace("&amp;", "&")  # Clean extracted code

            print(f"\n✅ Bottom Section Code Extracted:\n{Bottom_clean_code}")

        except Exception as e:
            print(f"❌ Failed to extract Bottom Section code: {e}")
    else:
        print("Bottom Section was Not Found\n")

    return Top_clean_code,Bottom_clean_code
        
        
    
def description_extraction(driver,description_text_id):

    try:
        description_text=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, description_text_id)))
        description_text_raw_html = description_text.get_attribute("outerHTML")
        description_text_soup = BeautifulSoup(description_text_raw_html, "html.parser")

        # Extract all <div> and <p> elements inside div#j_id_58
        if description_text_id=='div#j_id_58':
            all_text_elements = description_text_soup.select(f"{description_text_id} #j_id_5a div, {description_text_id} #j_id_5a pre,{description_text_id} #j_id_5a p, {description_text_id} .ui-card-content p, {description_text_id} ul")
        else:
            all_text_elements = description_text_soup.select(f"{description_text_id} p")

        # Get text content from each <div> and <p>, removing extra spaces   
        all_texts = [element.get_text(strip=True) for element in all_text_elements]

        # Join all extracted text with a newline for readability
        description_text_clean_code = "\n".join(all_texts).replace("&amp;", "&")

        # Print the final cleaned text
        print(f"\n✅ Description Extracted:\n{description_text_clean_code}")
        
    except Exception as e:
        print(f"❌ Failed to extract Description code: {e}")
    
    return description_text_clean_code
     
          

def AI_response(description_text_clean_code,Top_clean_code, Bottom_clean_code, solution,AI_response_language):
    try:
      AI_generated_output=generate_code(description_text_clean_code,Top_clean_code, Bottom_clean_code, solution,AI_response_language)
      print(f"\nAI Response:\n{AI_generated_output}\n")
      return AI_generated_output
    except:
       print("❌ Failed to Generate solution by AI")
