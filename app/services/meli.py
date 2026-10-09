import os
import requests
from dotenv import load_dotenv

load_dotenv()

MELI_ACCESS_TOKEN = os.getenv("MELI_ACCESS_TOKEN", "")
AFFILIATE_TOOL = os.getenv("MELI_AFFILIATE_TOOL", "53987737")
AFFILIATE_TAG = os.getenv("MELI_AFFILIATE_TAG", "agner1984")

def gerar_link_afiliado(url_original: str) -> str:
    """Carimba o link do produto com a tag de afiliado do Agner"""
    if not url_original or url_original == "#":
        return "#"
    separador = "&" if "?" in url_original else "?"
    return f"{url_original}{separador}matt_tool={AFFILIATE_TOOL}&matt_word={AFFILIATE_TAG}"


MOCK_PRODUTOS = [
    {
        "id": "MLB2001",
        "categoria": "suplementos",
        "titulo": "Creatina Monohidratada 100% Pura 250g Growth Supplements",
        "preco": "39,90",
        "preco_original": "64,90",
        "desconto": 38,
        "parcelas_qtd": 3,
        "parcelas_valor": "13,30",
        "foto": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?auto=format&fit=crop&w=400&q=80",
        "link": "https://www.mercadolivre.com.br",
        "full": True,
        "frete_gratis": True,
    },
    {
        "id": "MLB2002",
        "categoria": "camping",
        "titulo": "Barraca de Camping Iglu Resistente à Água Para Até 4 Pessoas",
        "preco": "101,00",
        "preco_original": "196,00",
        "desconto": 48,
        "parcelas_qtd": 3,
        "parcelas_valor": "33,66",
        "foto": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=400&q=80",
        "link": "https://www.mercadolivre.com.br",
        "full": True,
        "frete_gratis": True,
    },
    {
        "id": "MLB2003",
        "categoria": "ar condicionado",
        "titulo": "Ar Condicionado Split Inverter Elgin Eco II 12.000 BTUs Frio 220V",
        "preco": "1.979,00",
        "preco_original": "2.249,00",
        "desconto": 12,
        "parcelas_qtd": 10,
        "parcelas_valor": "197,90",
        "foto": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80",
        "link": "https://www.mercadolivre.com.br",
        "full": True,
        "frete_gratis": True,
    },
    {
        "id": "MLB2004",
        "categoria": "smartphone",
        "titulo": "Smartphone Samsung Galaxy S23 5G 256GB Preto 8GB RAM",
        "preco": "2.999,00",
        "preco_original": "3.899,00",
        "desconto": 23,
        "parcelas_qtd": 10,
        "parcelas_valor": "299,90",
        "foto": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=400&q=80",
        "link": "https://www.mercadolivre.com.br",
        "full": True,
        "frete_gratis": True,
    },
    {
        "id": "MLB2005",
        "categoria": "notebook",
        "titulo": "Notebook Lenovo IdeaPad 1 R5-7520U 16GB SSD 512GB Linux 15.6",
        "preco": "2.449,00",
        "preco_original": "2.899,00",
        "desconto": 15,
        "parcelas_qtd": 10,
        "parcelas_valor": "244,90",
        "foto": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=400&q=80",
        "link": "https://www.mercadolivre.com.br",
        "full": True,
        "frete_gratis": True,
    },
    {
        "id": "MLB2006",
        "categoria": "suplementos",
        "titulo": "100% Whey Concentrado 900g Baunilha Growth Supplements",
        "preco": "89,90",
        "preco_original": "119,00",
        "desconto": 24,
        "parcelas_qtd": 4,
        "parcelas_valor": "22,47",
        "foto": "https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?auto=format&fit=crop&w=400&q=80",
        "link": "https://www.mercadolivre.com.br",
        "full": True,
        "frete_gratis": True,
    }
]

def buscar_produtos_meli(termo: str = "suplementos", limite: int = 12):
    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {"q": termo, "limit": limite}
    headers = {"User-Agent": "OfertaBot/1.0"}

    if MELI_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {MELI_ACCESS_TOKEN}"

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        produtos_formatados = []
        for item in data.get("results", []):
            preco = item.get("price", 0)
            preco_original = item.get("original_price")
            
            desconto = 0
            if preco_original and preco_original > preco:
                desconto = int(round(((preco_original - preco) / preco_original) * 100))

            installments = item.get("installments") or {}
            parcelas_qtd = installments.get("quantity", 0)
            parcelas_valor = installments.get("amount", 0)

            thumb = item.get("thumbnail", "")
            foto_hd = thumb.replace("-I.jpg", "-O.jpg").replace("http://", "https://")

            # Aplica o rastreador de afiliado no link do produto
            link_original = item.get("permalink", "#")
            link_afiliado = gerar_link_afiliado(link_original)

            shipping = item.get("shipping", {})
            eh_full = shipping.get("logistic_type") == "fulfillment"
            frete_gratis = shipping.get("free_shipping", False)

            produtos_formatados.append({
                "id": item.get("id"),
                "titulo": item.get("title"),
                "preco": f"{preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "preco_original": f"{preco_original:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if preco_original else None,
                "desconto": desconto,
                "parcelas_qtd": parcelas_qtd,
                "parcelas_valor": f"{parcelas_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "foto": foto_hd,
                "link": link_afiliado,
                "full": eh_full,
                "frete_gratis": frete_gratis,
            })

        return produtos_formatados

    except Exception:
        termo_lower = termo.lower().strip()
        filtrados = [
            p for p in MOCK_PRODUTOS 
            if termo_lower in p["categoria"] or termo_lower in p["titulo"].lower()
        ]
        base = filtrados if filtrados else MOCK_PRODUTOS
        
        # Garante a tag também nos mocks
        for item in base:
            item["link"] = gerar_link_afiliado(item.get("link", "#"))
            
        return base