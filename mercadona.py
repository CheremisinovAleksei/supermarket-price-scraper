import requests

API_KEY = "9d8f2e39e90df472b4f2e559a116fe17"
APP_ID = "7UZJKL1DJ0"

def normalize_number(x):
    if x is None:
        return None
    
    try:
        x = float(x)
    except:
        return None
    
    if x.is_integer():
        return int(x)
    else:
        return x
    
def format_size(pi):
    if pi:
        unit_name = pi.get("unit_name")      # botellas, latas, etc
        total_units = normalize_number(pi.get("total_units"))
        unit_size = normalize_number(pi.get("unit_size"))     # tamano por unidad
        pack_size = normalize_number(pi.get("pack_size"))     #tamano por unidad en los packs
        size_format = pi.get("size_format")  # L, kg, etc

        def convert(value, unit):
            if value and unit:
                if unit == "l" and value < 1:
                    return normalize_number(value*1000), "ml"
                if unit == "kg" and value < 1:
                    return normalize_number(value*1000), "g"
            return value, unit
        #si es un pack (12 latas x 330ml, 2 botellas x 2L, etc)
        if pi.get("is_pack") and total_units and unit_name and pack_size and size_format:
            value, unit = convert(pack_size, size_format)
            return f"{total_units} {unit_name} x {value} {unit}"

        #si no es un pack
        if unit_size and size_format:
            value, unit = convert(unit_size, size_format)
            return f"{value} {unit}"

    return None


def search_mercadona(query, limit = 10):
    url = "https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_vlc1_es/query"

    headers = {
    "x-algolia-api-key": API_KEY,
    "x-algolia-application-id": APP_ID
    }
    
    if limit == 0:
        limit = 100

    payload = {
        "query": query,
        "hitsPerPage": limit,
        "page": 0
    }

    r = requests.post(url, headers=headers, json=payload)
    data = r.json()

    def price_label(pi):
        if pi and pi.get("is_pack"):
            return "pack"
        return "ud"

    results = []
    for product in data.get("hits"):
        pi = product.get("price_instructions")

        results.append({
            "store": "Mercadona",
            "name": product.get("display_name"),
            "price": normalize_number(pi.get("unit_price")),
            "price_label": price_label(pi),
            "bulk_price": normalize_number(pi.get("bulk_price")),
            "bulk_unit": pi.get("reference_format"),
            "size": format_size(pi),
            "url": product.get("share_url"),
            "image_url": product.get("thumbnail")
        })

    return results