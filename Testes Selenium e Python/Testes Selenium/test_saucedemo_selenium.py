# Arquivo: tests/test_saucedemo_selenium.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valido_e_logout(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "/inventory.html" in driver.current_url
    page_title = driver.find_element(By.CLASS_NAME, "title").text
    assert "Products" == page_title
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    logout_link.click()
    assert driver.find_element(By.ID, "user-name").is_displayed()

def test_login_invalido(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("usuario_invalido")
    driver.find_element(By.ID, "password").send_keys("senha_errada")
    driver.find_element(By.ID, "login-button").click()
    error_message = driver.find_element(By.CSS_SELECTOR, '[data-test="error"]').text
    assert "Epic sadface: Username and password do not match any user in this service" in error_message
