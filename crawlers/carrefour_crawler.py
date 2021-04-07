import time
from .base_crawler import BaseCrawler
from models.article import Article

class CarrefourCrawler(BaseCrawler):
    def __init__(self):
        super(CarrefourCrawler, self).__init__()

    def get_product_urls(self, urls):
        result = []
        for url in urls:
            self.get(url)
            for product in self.find_by_class("product-card__detail"):
                url_detail = product\
                    .find_element_by_class_name("product-card__title")\
                    .find_element_by_class_name("product-card__title-link")\
                    .get_attribute("href")
                if url_detail is not None:
                    result.append(url_detail)    
        return result

    def run(self):
        urls = [
            f'https://www.carrefour.es/supermercado/la-despensa/lacteos/leche/cat20093/c?offset={offset}'
            for offset in [0, 24, 48, 72, 96, 120]
        ]
        
        result = []

        product_urls = self.get_product_urls(urls)
        
        for url in product_urls:
            self.get(url)
            result.append(self.parse_detail())
            time.sleep(1)
        return result

    def get_info_dt(self, boxes):
        get_key = lambda box : self.try_get(box, "info-title", lambda x: x.strip())
        get_value = lambda box : self.try_get(box, "info-txt", lambda x: x.strip())
        return { get_key(box): get_value(box) for box in boxes}

    def parse_detail(self):
        box_prices = self.get_by_class("buybox__prices")
        description = self.get_by_class("product-header__name").text
        info_boxes = self.find_by_class("nutrition-more-info__container")
        offer_price = self.try_get(box_prices, "buybox__price-strikethrough", lambda x: float(x.replace("€","").replace(",",".")))
        price = self.try_get(box_prices, "buybox__price--current", lambda x: float(x.replace("€","").replace(",",".")))
        pum = self.try_get(box_prices, "buybox__price-per-unit", lambda x: float(x.split(" ")[0].replace(",",".")))
        info_dt = self.get_info_dt(info_boxes)
        meassure_raw = info_dt.get("Medidas", None)
        return Article(
            description=description,
            brand=info_dt.get("Marca", None),
            name=info_dt.get("Denominación legal", None),
            price=price,
            market="carrefour",
            offer_price=offer_price,
            meassure= meassure_raw[-1] if meassure_raw is not None else "",
            pum=pum,
            size=meassure_raw[-2] if meassure_raw is not None else "",
            meassure_description="")

    def try_get(self, content, className, process):
        try:
            return process(content.find_element_by_class_name(className).text)
        except Exception as ex:
            print(ex)
            print(className)
            return None

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