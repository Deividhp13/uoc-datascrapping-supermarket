---
title: "uoc-datascrapping-supermarket: Precios de productos de supermercados "
author: "Andrés Baamonde Lozano"
author: "David Herrero Pascual"
date: "12 de marzo de 2021"
---

# Ficheros

## Doc

* pdf/ Entrega

## Código

* Crawlers/
  * base_crawler: Clase base del buscador, pide las urls, busca en el html y maneja el navegador.
  * carrefour_crawler: Fichero para buscar los enlaces de carrefour y posteriormente parsearlos.
  * dia_crawler:  Fichero para buscar los enlaces de carrefour y posteriormente parsearlos.
* Models/
  * article: Artículo común para todos los supermercados

* main.py: fichero principal, su ejecución da lugar a la base de datos ejecutando todos los crawlers.

## Datos

* data_carrefour.csv: datos de leche supermercado carrefour.
* data_dia.csv: datos de leche supermercado Dia.
* full_data.csv: datos definitivos, todos los supermercados.

# Instalación 

## Requirements

* python version > 3.8

```bash
python -m venv venv
venv\bin\pip -r install requirements.txt
```

# Ejecución

```bash
make
```
o 

```bash
venv/bin/python  main.py
```