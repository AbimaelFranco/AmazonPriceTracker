import requests
from bs4 import BeautifulSoup

def get_product_title(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"Error HTTP: {res.status_code}")
            return None

        soup = BeautifulSoup(res.content, "html.parser")

        # Buscar el título del producto
        title_tag = soup.find("span", id="productTitle")
        if title_tag:
            return title_tag.get_text(strip=True)

        return None

    except Exception as e:
        print("Error al obtener título:", e)
        return None
