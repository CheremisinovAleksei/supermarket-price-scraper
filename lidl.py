import requests
from bs4 import BeautifulSoup

url = "https://www.lidl.es/es/search"

def format_size(amount):
    if amount:
        amount = amount.strip().lower()
        amount = amount.replace("por", "").strip()
        amount = amount.replace("-", " ").strip()
    return amount

def format_baseprice(baseprice):
    # 1 kg = 10.48 -> 10.48, "kg"
    if baseprice:
        x = baseprice.strip().lower()
        if "=" in x:
            left, right = x.split("=")
            left = left.strip()
            right = right.strip()

            bulk_parts = left.split()
            bulk_unit = bulk_parts[1] if len(bulk_parts) >= 2 else None

            bulk_price  = normalize_number(right)

            return bulk_price, bulk_unit
    
    return None, None

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

def parse_Lidl(product):

    #name
    title = product.find("div", class_="plp-product-grid-box-tile__title")

    name_tag = title.find("strong") if title else None
    name = name_tag.text.strip() if name_tag else None

    #price
    price_tag = product.find("div", class_ = "price-pill__price")
    price = price_tag.text.strip() if price_tag else None
    price = normalize_number(price)

    #price label (Lidl no tiene division en packs/unidades)
    price_label = "ud"

    #base price
    baseprice_tag = product.find("small", class_ = "baseprice")
    baseprice = baseprice_tag.text.strip() if baseprice_tag else None
    bulk_price, bulk_unit = format_baseprice(baseprice)

    #size
    amount_tag = title.find("small", class_ = "amount") if title else None
    amount = amount_tag.text.strip() if amount_tag else None
    size = format_size(amount)

    #url
    url_tag = product.find("a")
    url = None
    if url_tag and url_tag.get("href"):
        url = "https://www.lidl.es/" + url_tag.get("href")

    #image url
    img_tag = url_tag.find("img")
    image_url = None
    if img_tag and img_tag.get("src"):
        image_url = "https://www.lidl.es/" + img_tag.get("src")

    return {
        "store": "Lidl",
        "name": name,
        "price": price,
        "price_label": price_label,
        "bulk_price": bulk_price,
        "bulk_unit": bulk_unit,
        "size": size,
        "url": url,
        "image_url": image_url
    }

def search_Lidl(query, limit=10):
    response = requests.get(url, params={"query": query})
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    products = soup.find_all("div", class_="plp-product-grid-box-tile__wrapper")
    results = []

    for product in products[:limit]:
        parsed = parse_Lidl(product)
        results.append(parsed)
    
    return results