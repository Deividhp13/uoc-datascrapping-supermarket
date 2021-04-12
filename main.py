import csv
import dataclasses
from crawlers.carrefour_crawler import CarrefourCrawler
from crawlers.dia_crawler import DiaCrawler

crawl = CarrefourCrawler()
crawl = DiaCrawler()

result = []

for crawler in [CarrefourCrawler(), DiaCrawler()]:
    result += list(map(dataclasses.asdict, crawler.run()))

keys = result[0].keys()

print("Se han obtenido los datos")

with open('full_data.csv', 'w+', encoding='utf8', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(result)