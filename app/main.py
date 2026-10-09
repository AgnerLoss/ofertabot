from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from app.services.meli import buscar_produtos_meli

app = FastAPI(title="OfertaBot")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home(request: Request, q: str = Query(default="eletrônicos")):
    # Busca produtos reais na API
    produtos = buscar_produtos_meli(termo=q, limite=12)
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "produtos": produtos,
            "termo_busca": q
        }
    )
