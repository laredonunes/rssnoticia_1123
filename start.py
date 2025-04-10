import requests
import feedparser
import json
import os
import time
import re

# inicio ==============================|


def extrair_e_limpar_imagem(texto: str):
    """
    Procura por uma tag <img> no texto, extrai a URL da imagem e retorna:
    - texto_sem_img: o texto sem a tag <img>
    - url_img: a URL extraída ou None se não encontrada
    """
    img_regex = r'<img.*?src="([^"]+)".*?>'
    resultado = re.search(img_regex, texto, re.IGNORECASE)
    url_img = None
    if resultado:
        url_img = resultado.group(1)
        # Remove todas as ocorrências da tag <img>
        texto = re.sub(img_regex, '', texto, flags=re.IGNORECASE).strip()
    return texto, url_img


def postar_noticia_discord(conteudo: str, detalhes: str):
    url_webhook = 'https://discord.com/api/webhooks/1353735159559622717/nHoIbNcAff0kAHeDxBiqDolRJfIQV4w1hK10uHs8XGSFuFUoDAUppeL5tmEw5tXxcngm'

    # Extrai a imagem (se houver) e limpa o texto em cada variável
    conteudo_limpo, url_img_conteudo = extrair_e_limpar_imagem(conteudo)
    detalhes_limpo, url_img_detalhes = extrair_e_limpar_imagem(detalhes)

    # Se encontrar a imagem em ambas, priorize uma (por exemplo, a do conteúdo)
    url_img = url_img_conteudo or url_img_detalhes

    data = {
        "embeds": [
            {
                "title": "📰 Nova Notícia",
                "description": conteudo_limpo,
                "color": 5814783,
                "fields": [
                    {
                        "name": "Detalhes",
                        "value": detalhes_limpo,
                        "inline": False
                    }
                ]
            }
        ]
    }

    if url_img:
        # Adiciona a imagem ao embed do Discord
        data["embeds"][0]["image"] = {"url": url_img}

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

def verificar_e_postar():
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

# Loop infinito a cada 6 horas
while True:
    verificar_e_postar()
    print("⏰ Próxima verificação em 6 horas.")
    time.sleep(21600)  # 6 horas em segundos
