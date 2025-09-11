# Arquivo: tests/test_herokuapp_playwright.py

from playwright.sync_api import Page, expect

URL_LOGIN = "https://the-internet.herokuapp.com/login"

def test_login_valido_e_logout(page: Page):
    page.goto(URL_LOGIN)
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("https://the-internet.herokuapp.com/secure")
    success_message = page.locator("#flash")
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("You logged into a secure area!")
    page.get_by_role("link", name="Logout").click()
    expect(page).to_have_url(URL_LOGIN)
    logout_message = page.locator("#flash")
    expect(logout_message).to_contain_text("You logged out of the secure area!")

def test_login_invalido(page: Page):
    page.goto(URL_LOGIN)
    page.locator("#username").fill("usuario_errado")
    page.locator("#password").fill("senha_errada")
    page.get_by_role("button", name="Login").click()
    error_message = page.locator("#flash")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Your username is invalid!")
