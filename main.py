import time
import environ
from selenium.webdriver.common.by import By
from OpenAI.OpenAI import OpenAI
from SeleniumBrowsers.AnswereeBrowser import Browser

env = environ.Env()
environ.Env.read_env()


OPEN_AI_API_KEY = env('OPEN_AI_API_KEY')
ANSWEREE_EMAIL = env('ANSWEREE_EMAIL')
ANSWEREE_PASSWORD = env('ANSWEREE_PASSWORD')


if __name__ == '__main__':
    openAI = OpenAI(OPEN_AI_API_KEY)
    browser = Browser('drivers/chromedriver')
    browser.open_page('https://www.answeree.com/')

    if not browser.load_cookies():
        browser.login(ANSWEREE_EMAIL, ANSWEREE_PASSWORD)

    for page in range(25, 525, 25):

        browser.open_page(f'https://www.answeree.com/questions?start={page}')
        elements = browser.find_elements(
            By.CLASS_NAME, 'qa-q-item-title')
        links = [x.find_element(by=By.TAG_NAME, value='a').get_attribute(
            'href') for x in elements]

        for l in links:
            browser.submit_answer(l, openAI=openAI)
        time.sleep(3)
    time.sleep(20)
    browser.close_browser()
