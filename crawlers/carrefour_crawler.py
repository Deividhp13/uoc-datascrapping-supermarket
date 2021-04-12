import time
import re
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
            for offset in [0, 12, 24, 36, 48, 60, 72, 84 ,96, 108, 120]
        ]
        
        result = []

        product_urls = self.get_product_urls(urls)
        
        for url in product_urls:
            self.get(url)
            self.scroll_bottom(steps=5, sleep=1)
            result.append(self.parse_detail())
            time.sleep(1)
        print(f"link number: {len(result)}")
        return result

    def get_info_dt(self, boxes):
        get_key = lambda box : self.try_get(box, "info-title", lambda x: x.strip())
        get_value = lambda box : self.try_get(box, "info-txt", lambda x: x.strip())
        return { get_key(box): get_value(box) for box in boxes}

    def get_size_from_desc(self, desc):
        m = self.get_meassure_desc(desc)
        if m is not None:
            m = re.search("\d", m)
            return None if m is None else int(m.group(0))
        return None

    def get_meassure_desc(self, desc):
        m = re.search("brik|botella \d l", desc)
        return None if m is None else m.group(0)

    def parse_detail(self):
        box_prices = self.get_by_class("buybox__prices")
        description = self.get_by_class("product-header__name").text
        info_boxes = self.find_by_class("nutrition-more-info__container")
        offer_price = self.try_get(
            box_prices,
            "buybox__price-strikethrough",
            lambda x: float(x.strip().replace("€","").replace(",",".")),
            print_exc=False)
    
        price = self.try_get(
            box_prices,
            "buybox__price--current",
            lambda x: float(x.strip().replace("€","").replace(",",".")),
            print_exc=False)
        
        if price is None:
            price = self.try_get(
                box_prices,
                "buybox__price",
                lambda x: float(x.strip().replace("€/l","").replace("€","").replace(",",".")))
        
        if price is None:
            print(self.browser.current_url)
            print(box_prices, box_prices.text)
        
        pum = self.try_get(
            box_prices,
            "buybox__price-per-unit",
            lambda x: float(x.strip().split(" ")[0].replace(",",".")))

        info_dt = self.get_info_dt(info_boxes)
        
        meassure_str = info_dt.get("Medidas", None) 
        size = self.get_size_from_desc(description)
        
        meassure_desc = self.get_meassure_desc(description)
        matches = re.search("R-\d+",self.browser.current_url)
        identifier = matches.group(0) if  matches is not None else ""
        return Article(
            description=description,
            brand=info_dt.get("Marca", None),
            name=info_dt.get("Denominación legal", None),
            price=price,
            market="carrefour",
            offer_price=str(offer_price),
            meassure=meassure_str[-1] if meassure_str is not None else "",
            pum=pum,
            size=size,
            meassure_description="",
            identifier=identifier,
            timestamp=time.time())

    def try_get(self, content, className, process, print_exc=True):
        try:
            return process(content.find_element_by_class_name(className).text)
        except Exception as ex:
            if print_exc:
                print(ex)
                print(className)
            return None