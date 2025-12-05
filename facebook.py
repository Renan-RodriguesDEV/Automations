import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()
USER_DATA_PATH = "C:\\Users\\Renan Rodrigues\\AppData\\Local\\Google\\Chrome\\User Data"


class Navigator:
    def __init__(self):
        self.browser = (
            sync_playwright()
            .start()
            .chromium.launch_persistent_context(
                user_data_dir=USER_DATA_PATH,
                headless=False,
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
        self.page.goto("https://www.facebook.com/")
        if self.page.query_selector("#email"):
            self.page.fill("#email", os.getenv("EMAIL"))
        if self.page.query_selector("#pass"):
            self.page.fill("#pass", os.getenv("PSW_FACE"))
        if self.page.query_selector("button[name='login']"):
            self.page.click("button[name='login']")
        self.page.wait_for_load_state("networkidle")

    def switch_profile(self):
        XPATH_PROFILE = '//*[@id="mount_0_0_ra"]/div/div/div[1]/div/div[2]/div[5]/div[1]/span/div/div[1]/div/svg/g/image'
        XPATH_SWITCH = '//*[@id="mount_0_0_ra"]/div/div/div[1]/div/div[2]/div[5]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div/div[1]/div/span/div/div/div/div/div[1]/div/div[1]/div/div/div[2]/div/svg/g/circle'
        if self.page.query_selector(XPATH_PROFILE):
            self.page.click(XPATH_PROFILE)
            if self.page.query_selector(XPATH_SWITCH):
                self.page.click(XPATH_SWITCH)
                self.page.wait_for_load_state("networkidle")

    def access_facebook_feed(self):
        self.login()
        self.page.goto("https://www.facebook.com/?filter=favorites&sk=h_chr")
        self.switch_profile()
        input("Press any key to continue...")


if __name__ == "__main__":
    with Navigator() as navigator:
        # navigator.login()
        navigator.access_facebook_feed()
