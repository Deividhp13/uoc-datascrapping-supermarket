from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
class BaseCrawler(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

    def get(self, url):
        self.browser.get(url)

    def find_by_id(self, identifier):
        return self.browser.find_element_by_id(identifier)

    def find_by_class(self, class_name):
        return self.browser.find_elements_by_class_name(class_name)
    
    def get_by_class(self, class_name):
        return self.browser.find_element_by_class_name(class_name)
    
    def run(self):
        raise NotImplementedError()