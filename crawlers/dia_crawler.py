import time
from .base_crawler import BaseCrawler
from models.article import Article
import re
from selenium.common.exceptions import NoSuchElementException


class DiaCrawler(BaseCrawler):
    def __init__(self):
        super(DiaCrawler, self).__init__()

    def get_product_urls(self):
        result = []
        links = self.find_by_class('productMainLink')
        for link in links:
            result.append(link.get_attribute("href"))

        return result

    def run(self):
        url = 'https://www.dia.es/compra-online/productos/lacteos-y-huevos/leche/c/WEB.005.046.00000?show=All'
        result = []

        self.get(url)
        time.sleep(1)
        product_urls = self.get_product_urls()

        for url in product_urls:
            print(url)
            self.get(url)
            self.scroll_bottom(steps=5, sleep=1)
            result.append(self.parse_detail())
            time.sleep(1)
        print(f"link number: {len(result)}")

        return result

    def parse_detail(self):
        description = self.find_element_by_xpath("//h1[@itemprop='name']").text

        try:
            product_name = self.find_by_id("nutritionalinformation")\
                .find_elements_by_class_name("form_field-label")[0]\
                .get_attribute("innerHTML").strip()
        except NoSuchElementException:
            product_name = ""

        brand = re.sub('[^A-Z]', '', description)

        prices = self.find_by_class("big-price")
        price = float(prices[0].text.strip().replace("€", "").replace(",", "."))

        if len(prices) == 2:
            offer_price = float(prices[1].text.strip().replace("€", "").replace(",", "."))
        else:
            offer_price = None

        pum = float(re.sub('[^0-9 | ^","]', '', self.get_by_class("average-price").text.replace(",", ".")))

        raw_description = description.split()
        meassure_description = ' '.join(raw_description[-3:])

        meassure_raw = raw_description[-2:]

        size = float(re.sub('[^0-9 | ^"."]', '', meassure_raw[-2])) if meassure_raw is not None else ""
        
        return Article(
            description=description,
            brand=brand,
            name=product_name,
            price=price,
            market="dia",
            offer_price=offer_price,
            meassure=meassure_raw[-1] if meassure_raw is not None else "",
            pum=pum,
            size=size,
            meassure_description=meassure_description,
            identifier=self.browser.current_url.split("/")[-1],
            timestamp=time.time())


""" legacy, parsing desde la lista
    def parse(self, product) -> Article:
        description = self.try_get(product, "product-card__title-link", str)
        description_split = description.replace(".", "").split(" ")
        price = self.try_get(product, "product-card__price", lambda x: float(x.replace("€", "").replace(",", ".")))
        pum =  self.try_get(product, "product-card__price-per-unit", lambda x: float(x.split(" ")[0].replace(",", ".")))
        return Article(
            description=description,
            brand="",
            name="",
            price=price,
            market="carrefour",
            offer_price=0.0,
            meassure=description_split[-1],
            pum=pum,
            size=0.0,
            meassure_description="")
"""