# Supermarket Price Scraper

Proyecto académico para la asignatura **Adquisición y Transmisión de Datos**.

El proyecto permite buscar y comparar precios de productos entre distintos supermercados online, normalizando la información y ordenando los resultados por precio real (€/kg o €/l).

## Supermercados soportados
- Mercadona (mediante API interna)
- Lidl (mediante scraping del HTML, requests + BeautifulSoap)

## Funcionalidades
- Búsqueda estándar de productos
- Filtrado de los productos más baratos según precio por unidad
- Arquitectura cliente-servidor (TCP)

## Tecnologías utilizadas
- Python
- requests
- BeautifulSoup
- sockets
