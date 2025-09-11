
from playwright.sync_api import Page, expect


def test_login_valido_e_logout(page: Page):
    """
    Testa o fluxo completo de login com um usuário válido,
    verifica o acesso à página de produtos e faz o logout.
    """
    page.goto("https://www.saucedemo.com/")

    page.locator('[data-test="username"]').fill("standard_user")

    page.locator('[data-test="password"]').fill("secret_sauce")

    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    page.get_by_role("button", name="Open Menu").click()

    page.get_by_role("link", name="Logout").click()

    expect(page.locator('[data-test="username"]')).to_be_visible()


def test_login_invalido(page: Page):
    """
    Testa a tentativa de login com credenciais inválidas e
    verifica se a mensagem de erro correta é exibida.
    """
    page.goto("https://www.saucedemo.com/")

    page.locator('[data-test="username"]').fill("usuario_invalido")

    page.locator('[data-test="password"]').fill("senha_errada")

    page.locator('[data-test="login-button"]').click()

    error_message = page.locator('[data-test="error"]')
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text("Epic sadface: Username and password do not match any user in this service")