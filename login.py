import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def standard_navigation(driver):
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/faces/ui/profile.xhtml']"))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/faces/candidate/trackshome.xhtml']"))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/faces/candidate/lev1.xhtml']"))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/faces/candidate/codeprogramgroup.xhtml?gt=CODETUTOR']"))).click()

    print("✅ Navigated to Language successfully.")


def login(driver,overlay):
    LOGIN_ID = config.LOGIN_ID
    LOGIN_PASSWORD = config.LOGIN_PASSWORD


    """Logs into Skill Rack with provided credentials."""
    driver.get("https://www.skillrack.com/faces/candidate/tutorprogram.xhtml")
    overlay.set_status("⚡ Logging in Progress...")
    print("⚡ Logging in...")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "j_username")))

    driver.find_element(By.NAME, "j_username").send_keys(LOGIN_ID)
    driver.find_element(By.NAME, "j_password").send_keys(LOGIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input.ui.button.primary").click()
    print("🔥 Logged in successfully.")
    
    standard_navigation(driver)
    
