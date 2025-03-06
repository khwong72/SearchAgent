#screenshot_capture.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def capture_screenshot(url, output_path="screenshot.png"):
    """
    Launches a headless Chrome browser to navigate to the given URL and takes a screenshot.
    
    :param url: The URL of the website to capture.
    :param output_path: The filename where the screenshot will be saved.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode.
    options.add_argument("--window-size=1280,800")  # Set a fixed window size.
    
    # Initialize the Chrome driver.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        # Wait for body to be present instead of arbitrary sleep
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        driver.save_screenshot(output_path)
    finally:
        driver.quit()

# For standalone testing (optional)
if __name__ == "__main__":
    test_url = "https://example.com"
    capture_screenshot(test_url)
    print(f"Screenshot captured and saved as screenshot.png")
