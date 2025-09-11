# Arquivo: tests/test_orangehrm_playwright.py

from playwright.sync_api import Page, expect

URL = "https://opensource-demo.orangehrmlive.com/"

def test_login_valido_e_logout(page: Page):
    page.goto(URL)
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(URL + "web/index.php/dashboard/index")
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
    page.locator(".oxd-userdropdown-tab").click()
    page.get_by_role("menuitem", name="Logout").click()
    expect(page).to_have_url(URL + "web/index.php/auth/login")
    expect(page.get_by_placeholder("Username")).to_be_visible()

def test_login_invalido(page: Page):
    page.goto(URL)
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("senhaerrada")
    page.get_by_role("button", name="Login").click()
    error_message = page.locator(".oxd-alert-content-text")
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text("Invalid credentials")
