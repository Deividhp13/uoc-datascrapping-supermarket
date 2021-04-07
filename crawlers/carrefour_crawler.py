from .base_crawler import BaseCrawler
from models.article import Article

class CarrefourCrawler(BaseCrawler):
    def __init__(self):
        super(CarrefourCrawler, self).__init__()

    def run(self):
        urls = [
            f'https://www.carrefour.es/supermercado/la-despensa/lacteos/leche/cat20093/c?offset={offset}'
            for offset in [0, 24, 48, 72, 96, 120]
        ]
        
        result = []
        for url in urls:
            self.get(url)
            for product in self.find_by_class("product-card__detail"):
                element = self.parse(product)
                result.append(element)
        print(result[1:10])

    def try_get(self, content, className, process):
        try:
            return process(content.find_element_by_class_name(className).text)
        except Exception as ex:
            print(ex)
            print(className)
            return None

    def parse(self, product) -> Article:
        description = self.try_get(product, "product-card__title", str)
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