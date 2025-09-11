# Arquivo: tests/test_orangehrm_selenium.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://opensource-demo.orangehrmlive.com/"

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valido_e_logout(driver):
    driver.get(URL)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h6.oxd-topbar-header-breadcrumb-module"))
    )
    assert "dashboard" in driver.current_url
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-tab").click()
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    )
    logout_link.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    assert "auth/login" in driver.current_url

def test_login_invalido(driver):
    driver.get(URL)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("senhaerrada")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text"))
    )
    assert "Invalid credentials" in error_message.text
