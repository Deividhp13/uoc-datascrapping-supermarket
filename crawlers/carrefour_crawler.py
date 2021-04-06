from .base_crawler import BaseCrawler

class CarrefourCrawler(BaseCrawler):
    def __init__(self):
        super(CarrefourCrawler, self).__init__()

    def run(self):
        urls = [
            f'https://www.carrefour.es/supermercado/la-despensa/lacteos/leche/cat20093/c?offset={offset}'
            for offset in [0, 24, 48, 72, 96, 120]
        ]
        for url in urls:
            self.get(url)
            for product in self.find_by_class("product-card__detail"):
                element = self.parse(product)
    
    def try_get(self, content, className):
        try:
            return content.find_element_by_class_name(className).text
        except:
            return None

    def parse(self, product):
        print(self.try_get(product, "product-card__title"))
        print(self.try_get(product, "product-card__price"))
        print(self.try_get(product, "product-card__price-per-unit"))