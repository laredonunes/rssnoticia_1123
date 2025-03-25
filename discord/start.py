import requests

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
        return True
    else:
        print(f"❌ Falha ao postar notícia: {response.status_code}, {response.text}")
        return False

