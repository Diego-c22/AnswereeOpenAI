import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from OpenAI.OpenAI import OpenAI


class Browser:
    browser, service, cookies = None, None, None

    def __init__(self, driver: str, cookies: str = None) -> None:
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)
        self.cookies = cookies

    def open_page(self, url: str) -> None:
        self.browser.get(url)
        time.sleep(5)

    def close_browser(self):
        self.browser.close()

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    def click_button(self, by: By, value: str) -> bool:
        try:
            button = self.browser.find_element(by=by, value=value)
        except:
            return False
        self.browser.execute_script('arguments[0].click();', button)
        time.sleep(1)
        return True

    def find_elements(self, by: By, value: str) -> list:
        elements = self.browser.find_elements(
            by, value=value)
        return elements

    def find_element(self, by: By, value: str) -> list:
        element = self.browser.find_element(
            by, value=value)
        return element

    def load_cookies(self) -> bool:
        try:
            cookies = pickle.load(open('cookies.pkl', 'rb'))
        except:
            return False
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        time.sleep(5)
        return True

    def login(self, username: str, password: str):
        self.click_button(by=By.CLASS_NAME, value='navbar-login-button')
        self.add_input(by=By.ID, value='qa-userid', text=username)
        self.add_input(by=By.ID, value='qa-password', text=password)
        self.click_button(by=By.ID, value='login')
        time.sleep(5)
        self.cookies = self.browser.get_cookies()
        pickle.dump(self.cookies, open("cookies.pkl", 'wb'))
        time.sleep(5)

    def submit_answer(self, link: str, openAI: OpenAI) -> None:
        self.open_page(link)

        question = self.find_element(
            by=By.CSS_SELECTOR, value='.qa-q-view-content > div').text
        print("QUESTION:", question)

        if not self.click_button(By.ID, 'q_doanswer'):
            return

        answer = openAI.make_request(
            question, 300, 0, OpenAI.Models.DAVINCI)
        print('ANSWER:', answer)
        time.sleep(2)
        iframe = self.find_element(
            By.CSS_SELECTOR, '.sceditor-container > iframe')
        self.browser.switch_to.frame(iframe)
        self.find_element(By.CSS_SELECTOR, 'body > p').send_keys(answer)
        time.sleep(5)
        self.browser.switch_to.default_content()
        time.sleep(3)
        self.click_button(By.CLASS_NAME, 'qa-form-tall-button-answer')
        error_text = self.find_element(
            By.CLASS_NAME, 'qa-form-tall-error').text
        if error_text and len(error_text) > 0:
            print(error_text)
