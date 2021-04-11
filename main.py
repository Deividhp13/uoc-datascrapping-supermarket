import csv
import dataclasses
from crawlers.carrefour_crawler import CarrefourCrawler
from crawlers.dia_crawler import DiaCrawler

#crawl = CarrefourCrawler()
crawl = DiaCrawler()

result = list(map(dataclasses.asdict, crawl.run()))

keys = result[0].keys()

print("Se han obtenido los datos")

with open('data_dia.csv', 'w+', encoding='utf8', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(result)