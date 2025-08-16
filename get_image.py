import requests
from bs4 import BeautifulSoup
import re

def get_image(url):
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
            print("Error al acceder a Amazon:", res.status_code)
            return None

        soup = BeautifulSoup(res.content, "html.parser")

        # 1. Intento con id="landingImage"
        img = soup.find("img", id="landingImage")
        if img and img.get("src"):
            return img["src"]

        # 2. Intento con data-old-hires
        img = soup.find("img", attrs={"data-old-hires": True})
        if img:
            return img["data-old-hires"]

        # 3. Expresión regular como última opción
        match = re.search(r'https://m\.media-amazon\.com/images/I/[^\s"]+\.jpg', res.text)
        if match:
            return match.group(0)

    except Exception as e:
        print("Error:", e)

    return None
