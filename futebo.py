import requests  
import json

token = {'Authorization': 'Bearer test_98b1f9349d0e0489037646a93ab194'}
url = requests.get("https://api.api-futebol.com.br/v1/campeonatos/14/tabela", headers=token)

print(url.json())