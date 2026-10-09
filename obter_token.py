import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MELI_CLIENT_ID")
CLIENT_SECRET = os.getenv("MELI_CLIENT_SECRET")
REDIRECT_URI = "https://ofertabot.k8sloss.com.br/callback"

# Cole o código INTEIRO aqui dentro das aspas (começando com TG-)
codigo = "TG-6abeef2f3567d100018bd001-77289457"

url = "https://api.mercadolibre.com/oauth/token"
payload = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": codigo,
    "redirect_uri": REDIRECT_URI
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

if response.status_code == 200:
    dados = response.json()
    token = dados.get("access_token")
    refresh = dados.get("refresh_token")
    print("\nToken obtido com sucesso!")
    print(f"\nMELI_ACCESS_TOKEN={token}\nMELI_REFRESH_TOKEN={refresh}")
else:
    print(f"\nErro ({response.status_code}):", response.text)