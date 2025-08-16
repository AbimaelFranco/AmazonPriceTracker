import httpx

try:
    r = httpx.get("https://api.telegram.org")
    print("Conexión exitosa:", r.status_code)
except Exception as e:
    print("Error de conexión:", e)
