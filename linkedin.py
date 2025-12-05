import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()


class Navigator:
    DATA_LOGIN = {"USERNAME": os.getenv("EMAIL"), "PASSWORD": os.getenv("PSW_LINKEDIN")}

    def __init__(self):
        self.base_url = "https://www.linkedin.com/"
        self.browser = sync_playwright().start().chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()

    def login(self):
        self.page.goto(self.base_url + "login")
        self.page.fill("#username", self.DATA_LOGIN["USERNAME"])
        self.page.fill("#password", self.DATA_LOGIN["PASSWORD"])
        self.page.click(
            "#organic-div > form > div.login__form_action_container > button"
        )
        self.page.goto(self.base_url + "jobs/collections/recommended")
        self.get_all_jobs()

    def get_all_jobs(self):
        jobs = self.page.query_selector_all("li.ember-view")
        print(len(jobs))
        return jobs


if __name__ == "__main__":
    with Navigator() as navigator:
        navigator.login()
