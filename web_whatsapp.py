import os
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright

USER_DATA_PATH = "C:\\Users\\Renan Rodrigues\\AppData\\Local\\Google\\Chrome\\User Data"


class Navigator:
    def __init__(self):
        self.browser = (
            sync_playwright()
            .start()
            .chromium.launch_persistent_context(
                user_data_dir=USER_DATA_PATH, headless=False, viewport=None
            )
        )
        self.page = (
            self.browser.pages[0] if self.browser.pages else self.browser.new_page()
        )
        self.page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
            }
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()

    def login(self):
        self.page.goto("https://web.whatsapp.com/")
        self.page.wait_for_load_state("networkidle")

    def find_contact(self, contact, content="Hello World"):
        content = urlencode({"text": content})
        self.page.goto(f"https://web.whatsapp.com/send?phone={contact}&{content}")
        self.page.wait_for_selector('span[dir="auto"]')
        self.page.wait_for_load_state("networkidle")
        self.page.click('span[data-icon="send"]')


if __name__ == "__main__":
    with Navigator() as navigator:
        # navigator.login()
        navigator.login()
        navigator.find_contact(os.getenv("PHONE"))
        input("Press any key to continue...")
