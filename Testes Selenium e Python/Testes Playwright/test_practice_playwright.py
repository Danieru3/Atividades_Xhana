# Arquivo: tests/test_practice_playwright.py

from playwright.sync_api import Page, expect

URL = "https://practicetestautomation.com/practice-test-login/"

def test_login_valido_e_logout(page: Page):
    page.goto(URL)
    page.locator("#username").fill("student")
    page.locator("#password").fill("Password123")
    page.locator("#submit").click()
    expect(page).to_have_url("https://practicetestautomation.com/logged-in-successfully/")
    expect(page.get_by_text("Congratulations student. You successfully logged in!")).to_be_visible()
    expect(page.get_by_role("link", name="Log out")).to_be_visible()
    page.get_by_role("link", name="Log out").click()
    expect(page.locator("#submit")).to_be_visible()

def test_login_invalido(page: Page):
    page.goto(URL)
    page.locator("#username").fill("wrongstudent")
    page.locator("#password").fill("Password123")
    page.locator("#submit").click()
    error_message = page.locator("#error")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Your username is invalid!")
