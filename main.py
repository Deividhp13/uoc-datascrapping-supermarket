import csv
import dataclasses
from crawlers.carrefour_crawler import CarrefourCrawler


crawl = CarrefourCrawler()

result = list(map(dataclasses.asdict, crawl.run()))

keys = result[0].keys()
with open('data.csv', 'w+', encoding='utf8', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(result)