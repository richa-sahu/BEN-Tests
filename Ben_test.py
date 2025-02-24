from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get("http://13.209.85.69/")

def is_form_cleared():
    return (
        driver.find_element(By.NAME, "username").get_attribute("value") == "" and
        driver.find_element(By.NAME, "password").get_attribute("value") == "" and
        driver.find_element(By.NAME, "email").get_attribute("value") == ""
    )

def handle_alert():
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text
    except:
        return None

def test_valid_registration():
    driver.find_element(By.NAME, "username").send_keys("TestUser123")
    driver.find_element(By.NAME, "password").send_keys("StrongPass@123")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "newsletter").click()
    driver.find_element(By.XPATH, "//input[@value='Register']").click()
    time.sleep(2)
    assert is_form_cleared(), "Form was not cleared after successful registration"

def test_missing_username():
    driver.refresh()
    driver.find_element(By.NAME, "password").send_keys("StrongPass@123")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.XPATH, "//input[@value='Register']").click()
    time.sleep(2)
    assert handle_alert() == "Username must be at least 5 characters.", "Unexpected alert message"

def test_invalid_email():
    driver.refresh()
    driver.find_element(By.NAME, "username").send_keys("TestUser123")
    driver.find_element(By.NAME, "password").send_keys("StrongPass@123")
    driver.find_element(By.NAME, "email").send_keys("invalidemail")
    driver.find_element(By.XPATH, "//input[@value='Register']").click()
    time.sleep(2)
    assert handle_alert() == "Please enter a valid email.", "Unexpected alert message"

def test_password_constraints():
    driver.refresh()
    driver.find_element(By.NAME, "username").send_keys("TestUser123")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
    driver.find_element(By.XPATH, "//input[@value='Register']").click()
    time.sleep(2)
    assert handle_alert() == "Password must be at least 8 characters", "Unexpected alert message"

def test_checkbox_functionality():
    driver.refresh()
    checkbox = driver.find_element(By.NAME, "newsletter")
    checkbox.click()
    assert checkbox.is_selected() == True

# Run tests
test_valid_registration()
test_missing_username()
test_invalid_email()
test_password_constraints()
test_checkbox_functionality()

driver.quit()
