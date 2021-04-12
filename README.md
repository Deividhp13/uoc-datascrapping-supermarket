# uoc-datascrapping-supermarket

# Ficheros
* pdf/ Entrega, preguntas y [respuestas](./pdf/respuestas.md) de la práctica
* Crawlers/
  * base_crawler: Clase base del buscador, pide las urls, busca en el html y maneja el navegador.
  * carrefour_crawler: Fichero para buscar los enlaces de carrefour y posteriormente parsearlos.
  * dia_crawler:  Fichero para buscar los enlaces de carrefour y posteriormente parsearlos.
* Models/
  * article: Artículo común para todos los supermercados

* main.py: fichero principal, su ejecución da lugar a la base de datos ejecutando todos los crawlers.


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
