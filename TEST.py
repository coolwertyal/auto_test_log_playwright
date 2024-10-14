import os
import pytest
from playwright.sync_api import sync_playwright
import time

SESSION_DIR = 'session'

@pytest.mark.asyncio
def test_open_telegram(page):
    assert page.title() == "Telegram Web"
@pytest.fixture(scope="session")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--start-maximized'], headless=False)
        if not os.path.exists(SESSION_DIR):
            os.makedirs(SESSION_DIR)
        if os.path.exists(os.path.join(SESSION_DIR, 'context.json')):
            context = browser.new_context(storage_state=os.path.join(SESSION_DIR, 'context.json'))
        else:
            context = browser.new_context()

        page = context.new_page()
        url = 'https://web.telegram.org/k/'
        page.goto(url)
        page.wait_for_load_state('networkidle')

        page.goto("https://web.telegram.org/k/#@chatsgpts_bot")
        time.sleep(10)
        second_time_button = page.get_by_text("/start", exact=True).last
        first_time_button = page.get_by_text("START", exact=True).last
        first_f = first_time_button.is_visible()
        if first_f:
            actual_button = first_time_button
        else:
            actual_button = second_time_button
        try:
            actual_button.click()
        except Exception as e:
            print(e)
        time.sleep(3)
        bot_message = page.locator("div.message").last.inner_text()
        yield page

        context.storage_state(path=os.path.join(SESSION_DIR, 'context.json'))
        print("Сообщение от бота:", bot_message)
        browser.close()

    pytest.main(["-s", "-v"])