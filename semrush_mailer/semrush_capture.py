import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def login_to_semrush(driver):
    """
    Log in to SEMRush using credentials from environment variables
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        bool: True if login successful, False otherwise
    """
    # Get credentials from environment variables
    email = os.getenv("SEMRUSH_EMAIL")
    password = os.getenv("SEMRUSH_PASSWORD")
    
    logger.debug(f"Environment variables loaded - Email available: {bool(email)}, Password available: {bool(password)}")
    
    if not email or not password:
        logger.error("SEMRUSH_EMAIL and SEMRUSH_PASSWORD environment variables are required")
        return False
    
    try:
        # Go to login page
        logger.info("Navigating to SEMRush login page")
        driver.get("https://www.semrush.com/login/")
        time.sleep(3)
        
        # Debug info about the current page
        logger.debug(f"Current URL: {driver.current_url}")
        logger.debug(f"Page title: {driver.title}")
        
        # Wait for the login form to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
            )
            logger.debug("Login form loaded successfully")
        except Exception as e:
            logger.debug(f"Error waiting for login form: {e}")
            # Take screenshot of current state
            driver.save_screenshot("login_page_error.png")
            logger.debug("Screenshot saved to login_page_error.png")
        
        # Fill in the login form
        logger.info(f"Logging in with email: {email}")
        
        # Find email field - try multiple possible selectors
        try:
            email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
            logger.debug("Found email field by type='email'")
        except:
            try:
                email_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
                logger.debug("Found email field by name='email'")
            except:
                try:
                    email_field = driver.find_element(By.ID, "email")
                    logger.debug("Found email field by id='email'")
                except:
                    # Take screenshot for debugging
                    driver.save_screenshot("email_field_not_found.png")
                    logger.error("Could not find email field, see screenshot: email_field_not_found.png")
                    return False
        
        email_field.clear()
        email_field.send_keys(email)
        logger.debug("Email entered")
        
        # Sometimes password field appears after email is entered
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            logger.debug("Found next button, clicking it")
            next_button.click()
            time.sleep(3)
        except:
            logger.info("No next button found, continuing to password")
        
        # Find password field - try multiple possible selectors
        try:
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            logger.debug("Found password field by type='password'")
        except:
            try:
                password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
                logger.debug("Found password field by name='password'")
            except:
                try:
                    password_field = driver.find_element(By.ID, "password")
                    logger.debug("Found password field by id='password'")
                except:
                    # Take screenshot for debugging
                    driver.save_screenshot("password_field_not_found.png")
                    logger.error("Could not find password field, see screenshot: password_field_not_found.png")
                    return False
        
        password_field.clear()
        password_field.send_keys(password)
        logger.debug("Password entered")
        
        # Click the login button
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            logger.debug("Found submit button, clicking it")
            submit_button.click()
        except Exception as e:
            logger.error(f"Could not find submit button: {e}")
            driver.save_screenshot("submit_button_not_found.png")
            return False
        
        # Wait for login to complete
        logger.info("Waiting for login to complete...")
        time.sleep(5)
        
        # Take screenshot of current state
        driver.save_screenshot("after_login_attempt.png")
        logger.debug("Screenshot saved to after_login_attempt.png")
        
        # Check if login was successful
        logger.debug(f"Current URL after login attempt: {driver.current_url}")
        
        # Check for login errors
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, ".auth-form__error")
            logger.error(f"Login error displayed: {error_element.text}")
            return False
        except:
            logger.debug("No login error messages found")
        
        # Check if login was successful (look for elements that appear after login)
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_any_element_located([
                    (By.CSS_SELECTOR, ".srf-header__user"),
                    (By.CSS_SELECTOR, ".srf-navbar__user"),
                    (By.CSS_SELECTOR, ".srf-user-menu")
                ])
            )
            logger.info("Login successful")
            return True
        except:
            # Check if we're on a different page that indicates success
            if "analytics" in driver.current_url or "projects" in driver.current_url:
                logger.info("Login seems successful based on URL")
                return True
            else:
                logger.error("Login failed or timed out")
                return False
            
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return False

def capture_semrush_report(domain, output_dir="semrush_reports", headless=False):
    """
    Captures a screenshot of a website's SEMRush overview report.
    
    Args:
        domain (str): The domain to check (e.g., 'example.com')
        output_dir (str): Directory to save the screenshot
        headless (bool): Whether to run in headless mode or show browser window
    
    Returns:
        str: Path to the saved screenshot or None if failed
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean domain (remove http/https/www if present)
    if '://' in domain:
        domain = domain.split('://')[1]
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Remove any trailing path
    if '/' in domain:
        domain = domain.split('/')[0]
    
    output_path = os.path.join(output_dir, f"{domain.replace('.', '_')}_semrush.png")
    
    logger.info(f"Capturing SEMRush report for {domain}")
    
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # First, log in to SEMRush
        if not login_to_semrush(driver):
            logger.error("Could not log in to SEMRush, continuing without login")
            driver.save_screenshot("login_failed.png")
            logger.info("Login attempt screenshot saved to login_failed.png")
        
        # Use the correct URL format with query parameters
        semrush_url = f"https://www.semrush.com/analytics/overview/?q={domain}&protocol=https&searchType=domain"
        
        logger.info(f"Opening SEMRush URL: {semrush_url}")
        driver.get(semrush_url)
        
        # Save screenshot of initial page load
        driver.save_screenshot("initial_page_load.png")
        logger.debug("Initial page screenshot saved to initial_page_load.png")
        
        # Wait for page to load
        logger.info("Waiting for page to load...")
        time.sleep(5)  # Initial wait
        
        # Check if we need to input the domain manually (if we landed on the main search page)
        try:
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='domain'], input[placeholder*='URL']"))
            )
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.srf-search-button, button[type='submit']"))
            )
            
            # Input domain and click search if needed
            if search_input.get_attribute("value") == "":
                search_input.clear()
                search_input.send_keys(domain)
                search_button.click()
                logger.info(f"Manually entered domain: {domain}")
                time.sleep(5)  # Wait after search
        except Exception as e:
            logger.info(f"No manual domain entry needed or could not find search input: {e}")
        
        # Save screenshot after domain entry or search
        driver.save_screenshot("after_domain_search.png")
        logger.debug("Screenshot after domain search saved to after_domain_search.png")
        
        # Additional waits and checks to ensure page loads completely
        try:
            # Wait for any of these elements that might indicate data has loaded
            WebDriverWait(driver, 30).until(
                EC.presence_of_any_element_located([
                    (By.CSS_SELECTOR, ".sm-overview__block, .srf-overview__block, .sm-overview-block, .srf-overview-block"),
                    (By.CSS_SELECTOR, ".srf-domain-overview__title, .domain-overview"),
                    (By.CSS_SELECTOR, ".srf-overview__widget, .sm-overview__widget"),
                    (By.CSS_SELECTOR, ".srf-overview-widgets, .overview-widgets")
                ])
            )
            logger.info("Overview data loaded")
        except Exception as e:
            logger.warning(f"Timeout waiting for overview data: {e}")
            # Continue anyway, might still get useful screenshot
        
        # Give extra time for all charts to render
        time.sleep(10)
        
        # Scroll down to capture more of the page
        logger.info("Scrolling page to capture full report...")
        for i in range(5):
            driver.execute_script(f"window.scrollTo(0, {i * 400});")
            time.sleep(0.5)
        
        # Scroll back to top for the screenshot
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Capture the screenshot
        logger.info("Capturing screenshot...")
        driver.save_screenshot(output_path)
        logger.info(f"Screenshot saved to {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error capturing SEMRush report for {domain}: {e}")
        return None
    
    finally:
        if 'driver' in locals():
            driver.quit() 