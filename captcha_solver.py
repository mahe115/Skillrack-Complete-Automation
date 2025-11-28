import time
import re
import numpy as np
import easyocr
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


reader = easyocr.Reader(['en'], gpu=False)

def solve_captcha(driver,img_element_id):
    """Solves the CAPTCHA automatically using EasyOCR."""
    
    time.sleep(2)
    img_element = driver.find_element(By.ID, img_element_id)
    img_bytes = img_element.screenshot_as_png
    image = Image.open(BytesIO(img_bytes))

    image_np = np.array(image)
    extracted_text = ' '.join(reader.readtext(image_np, detail=0)).strip()
    print("Extracted Text:", extracted_text)

    match = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', extracted_text)
    if match:
        num1, operator, num2 = map(str.strip, match.groups())
        result = eval(f"{int(num1)} {operator} {int(num2)}")
        
        input_field = driver.find_element(By.ID, "capval")
        input_field.clear()
        input_field.send_keys(str(result))
        driver.find_element(By.ID, "proceedbtn").click()
        print("✅ CAPTCHA solved successfully.")
    else:
        print("❌ Could not extract a valid equation.")
        driver.quit()
        exit()


def monitor_Proceed_button_present(driver, element_checking_id, proceed_button_id):
    """Continuously checks if a specific div (element_id) exists every 5 seconds.
    - If present, waits for `proceed_button_id`.
    - If suddenly disappears, throws an error.
    """

    print("⏳Waiting for proceed button appear...")
    while True:
        try:
            # **Check if the element is present**
            element_checking = driver.find_elements(By.ID, element_checking_id)

            if element_checking:
                try:
                    # **Wait for the proceed button to appear**
                    proceed_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, proceed_button_id)))
                    print("✅ Proceed button found, clicking...")
                    proceed_button.click()
                    break

                except TimeoutException:
                    continue
                
            else:
                print(f"❌ Element '{element_checking_id}' disappeared unexpectedly. Exiting...")
                raise RuntimeError(f"Element '{element_checking_id}' was expected but is no longer found.")

        except NoSuchElementException:
            print(f"❌ Element '{element_checking_id}' not found. Retrying in 5 seconds...")


