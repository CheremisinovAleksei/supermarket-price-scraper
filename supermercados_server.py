from socket import *
import json

from mercadona import search_mercadona
from lidl import search_Lidl

def top_cheapest(products, top_n = 10):
    x = []
    for product in products:
        if product.get("bulk_price") and product.get("bulk_unit") != "ud":
            x.append(product)
    
    x.sort(key=lambda dict: dict["bulk_price"])
    return x[:top_n]

def make_request(req):

    req = json.loads(req)

    cmd = req.get("cmd")
    query = req.get("query")
    limit = req.get("limit")

    if limit == 0:
        limit = 5
    if limit > 100:
        limit = 100
    
    if cmd == "TOP":
        search_limit = 100
    else:
        search_limit = limit

    mercadona = search_mercadona(query, search_limit)
    lidl = search_Lidl(query, search_limit)

    total = []
    total.extend(mercadona)
    total.extend(lidl)

    if cmd == "TOP":
        res = top_cheapest(total, limit)
    else:
        res = total
    
    return {
        "res": res
    }
    

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('localhost', 10000))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        req = conn.recv(1024).decode()

        response = make_request(req)

        conn.send(json.dumps(response).encode())

        conn.close()