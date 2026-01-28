from socket import *
import json

def format_price(item):
    price = item.get("price")
    label = item.get("price_label")  # "pack" / "ud" / etc
    if price is None:
        return ""
    if label:
        return f"{price} €/{label}"
    return f"{price} €"

def format_bulk(item):
    bulk = item.get("bulk_price")
    unit = item.get("bulk_unit")  # "L" / "kg" / etc
    if bulk is None or unit is None:
        return ""
    return f"{bulk} €/{unit}"


def format_cmd(cmd):
    cmd = cmd.strip().lower()
    if cmd in ("1", "buscar", "busqueda", "b", "search"):
        return "SEARCH"
    if cmd in ("2", "top", "t"):
        return "TOP"
    if cmd in ("3", "salir", "exit", "e", "q"):
        return "EXIT"
    return None

def read_cmd():
    while True:
        print("\n¿Qué quieres hacer?")
        print("  1) BUSCAR productos")
        print("  2) TOP más baratos (por precio unitario)")
        print("Escribe 1/2 o BUSCAR/TOP. Escribe SALIR para terminar.")
        text = input("> ").strip()

        cmd = format_cmd(text)
        if cmd is None:
            print("Opción no válida. Prueba otra vez.")
            continue
        return cmd
    
def read_query():
    while True:
        text = input("Introduce búsqueda (o ATRAS / SALIR)\n> ").strip().lower()

        if text in ("salir", "exit", "e", "q"):
            return "-EXIT-"
        if text in ("atras", "atrás", "back", "`"):
            return None
        if len(text) == 0:
            print("Búsqueda vacía. Escribe algo.")
            continue
        return text
    
def read_limit():
    while True:
        text = input("Límite (Enter = límite estándar de 5, o ATRAS / SALIR)\n> ").strip().lower()

        if text in ("salir", "exit", "e", "q"):
            return -1
        if text in ("atras", "atrás", "back", "`"):
            return None
        if text == "" or text == "0":
            return 0
        try:
            n = int(text)
            if n < 0:
                print("Límite no puede ser negativo.")
                continue
            return n
        except:
            print("No es un número. Usaré el límite estándar de 5.")
            return 0
        
def send_request(req):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(("localhost", 10000))

    client.send(json.dumps(req).encode())

    response = client.recv(16384).decode()
    client.close()

    return json.loads(response)

def print_results(res):
    if not res:
        print(f"\nNo se encontraron resultados.")
        return
    for i, item in enumerate(res, start=1):
        store = item.get("store", "")
        name = item.get("name", "")
        size = item.get("size", "")
        price_str = format_price(item)
        bulk_str = format_bulk(item)
        url = item.get("url", "")
        img = item.get("image_url", "")

        print(f"{i}. [{store}] {name}")
        if size:
            print(f"   Size: {size}")
        if price_str:
            print(f"   Price: {price_str}")
        if bulk_str:
            print(f"   Unit price: {bulk_str}")
        if url:
            print(f"   URL: {url}")
        if img:
            print(f"   IMG: {img}")
        print()



if __name__ == "__main__":
    while True:
        cmd = read_cmd()
        if cmd == "EXIT":
            break

        query = read_query()
        if query == "-EXIT-":
            break
        if query is None:
            continue
        
        limit = read_limit()
        if limit == -1:
            break
        if limit is None:
            continue

        request = {
            "cmd": cmd,
            "query": query,
            "limit": limit
        }

        try:
            response = send_request(request)
        except Exception as e:
            print(f"Error inesperado: e")
            continue

        res = response.get("res", [])

        print_results(res)