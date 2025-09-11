# Arquivo: tests/test_practice_selenium.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://practicetestautomation.com/practice-test-login/"

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_login_valido_e_logout(driver):
    driver.get(URL)
    driver.find_element(By.ID, "username").send_keys("student")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "post-title"))
    )
    assert "logged-in-successfully" in driver.current_url
    assert driver.find_element(By.TAG_NAME, "strong").text == "Congratulations student. You successfully logged in!"
    driver.find_element(By.LINK_TEXT, "Log out").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "submit"))
    )
    assert "practice-test-login" in driver.current_url

def test_login_invalido(driver):
    driver.get(URL)
    driver.find_element(By.ID, "username").send_keys("wrongstudent")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()
    error_message = driver.find_element(By.ID, "error")
    assert error_message.is_displayed()
    assert "Your username is invalid!" in error_message.text
