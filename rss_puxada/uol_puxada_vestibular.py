import requests
import feedparser
import json
import os

def postar_noticia_discord(conteudo: str, detalhes: str):
    url_webhook = 'https://discord.com/api/webhooks/1353735159559622717/nHoIbNcAff0kAHeDxBiqDolRJfIQV4w1hK10uHs8XGSFuFUoDAUppeL5tmEw5tXxcngm'

    data = {
        "embeds": [
            {
                "title": "📰 Nova Notícia",
                "description": conteudo,
                "color": 5814783,
                "fields": [
                    {
                        "name": "Detalhes",
                        "value": detalhes,
                        "inline": False
                    }
                ]
            }
        ]
    }

    response = requests.post(url_webhook, json=data)

    if response.status_code == 204:
        print("✅ Notícia postada com sucesso no Discord!")
    else:
        print(f"❌ Falha ao postar notícia: {response.status_code}, {response.text}")

def puxar_noticias_rss(url_rss: str):
    feed = feedparser.parse(url_rss)
    noticias = []

    for entry in feed.entries:
        noticia = {
            "id": entry.link,
            "titulo": entry.title,
            "link": entry.link,
            "publicado": entry.published,
            "resumo": entry.summary
        }
        noticias.append(noticia)

    return noticias

def carregar_noticias_publicadas(arquivo: str):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    return []

def salvar_noticias_publicadas(arquivo: str, noticias: list):
    with open(arquivo, "w") as f:
        json.dump(noticias, f)

# Exemplo de uso
arquivo_registro = "noticias_publicadas.json"
url_rss = "https://rss.uol.com.br/feed/vestibular.xml"
noticias = puxar_noticias_rss(url_rss)
publicadas = carregar_noticias_publicadas(arquivo_registro)

for noticia in noticias:
    if noticia["id"] not in publicadas:
        conteudo = noticia["titulo"]
        detalhes = f"{noticia['resumo']}\n\nLeia mais: {noticia['link']}"
        postar_noticia_discord(conteudo, detalhes)
        publicadas.append(noticia["id"])

salvar_noticias_publicadas(arquivo_registro, publicadas)