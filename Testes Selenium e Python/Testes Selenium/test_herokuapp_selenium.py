# Arquivo: tests/test_herokuapp_selenium.py

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

URL_LOGIN = "https://the-internet.herokuapp.com/login"

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_valido_e_logout(driver):
    driver.get(URL_LOGIN)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    WebDriverWait(driver, 10).until(EC.url_contains("/secure"))
    assert "/secure" in driver.current_url
    success_message = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in success_message
    driver.find_element(By.CSS_SELECTOR, 'a.button[href="/logout"]').click()
    assert URL_LOGIN in driver.current_url
    logout_message = driver.find_element(By.ID, "flash").text
    assert "You logged out of the secure area!" in logout_message

def test_login_invalido(driver):
    driver.get(URL_LOGIN)
    driver.find_element(By.ID, "username").send_keys("usuario_errado")
    driver.find_element(By.ID, "password").send_keys("senha_errada")
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    error_message = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in error_message
