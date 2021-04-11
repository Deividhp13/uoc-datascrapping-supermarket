import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class BaseCrawler(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def get(self, url):
        self.browser.get(url)

    def find_by_id(self, identifier):
        return self.browser.find_element_by_id(identifier)

    def find_by_class(self, class_name):
        return self.browser.find_elements_by_class_name(class_name)

    def get_by_class(self, class_name):
        return self.browser.find_element_by_class_name(class_name)

    def find_elements_by_css_selector(self, css_selector):
        return self.browser.find_elements_by_css_selector(css_selector)

    def find_element_by_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath)

    def scroll_bottom(self, steps=1, sleep=1):
        try:
            for _ in range(steps):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(sleep)
        except Exception as ex:
            print(ex)
            print("Error haciendo scroll")

    def run(self):
        raise NotImplementedError()
