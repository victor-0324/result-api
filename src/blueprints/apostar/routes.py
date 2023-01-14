from flask import Blueprint, request, render_template, url_for, redirect
import requests  
import json
from collections import Counter
from bs4 import BeautifulSoup  
from datetime import datetime

def Texto():
# 1. Pegar conteudo HTML a partir da URL
    url = "https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB" 
    html = requests.get(url)  

    if html.status_code != 200: 
            print(">> Falha na requisição! <<")
    else:
        # content passa o conteúdo da página
        html_content = html.content
        # Parsear o conteúdo HTML buscado, para poder ficar mais estruturado de acordo com as tags HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        novo = soup.find_all('td')
        # Pegando todo o resultados
        novo = soup.find_all('td')
        result = [pt.get_text() for pt in novo]

    # bichos de cabeça de todos os dias
        cabeca_1horario = result[0:4:]
        cabeca_2horario = result[40:44:]
        cabeca_3horario = result[80:84]
        cabeca_4horario = result[120:124:]
        cabeca_5horario = result[160:164]
        cabeca_6horario = result[200:204]
        cabeca_1horario.append('9:45')
        cabeca_2horario.append('10:45')
        cabeca_3horario.append('12:45')
        cabeca_4horario.append('15:45')
        cabeca_5horario.append('18:H')
        cabeca_6horario.append('20:00')

        bichos_cabeca = [cabeca_1horario,cabeca_2horario ,cabeca_3horario ,cabeca_4horario ,cabeca_5horario ,cabeca_6horario ]

        todos_bichos = [result[i:i+4]for i in range(0, len(result), 4)]

        saio_mais = Counter(result)
        

        return saio_mais

apostar_app = Blueprint("apostar_app", __name__, url_prefix="/apostar", template_folder='templates',static_folder='static')


# Tela de apostar
@apostar_app.route("/", methods=["GET", "POST"])
def mostrar():   
    token = {'Authorization': 'Bearer test_98b1f9349d0e0489037646a93ab194'}
    url = requests.get("https://api.api-futebol.com.br/v1/campeonatos/1/tabela", headers=token)
    tabela = url.json()

    return render_template("pages/apostar/mostrar.html", tabela=tabela)


@apostar_app.route("/statistica", methods=["GET", "POST"])
def statistica(): 
    texto = Texto()  
    return render_template("pages/apostar/statistica.html",texto=texto)