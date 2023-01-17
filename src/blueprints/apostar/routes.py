from flask import Blueprint, request, render_template, url_for, redirect
import requests  
import csv
from collections import Counter
from bs4 import BeautifulSoup  
from datetime import datetime

def Bichos():
# 1. Pegar conteudo HTML a partir da URL
    url = "https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/"

    html = requests.get(url)  

    if html.status_code != 200: 
            print(">> Falha na requisição! <<")
    else:
    # content passa o conteúdo da página
        html_content = html.content
    # Parsear o conteúdo HTML buscado, para poder ficar mais estruturado de acordo com as tags HTML
        soup = BeautifulSoup(html_content, 'html.parser')
    # Pegando todo o resultados
        novo = soup.find_all('td')
        result = [pt.get_text() for pt in novo]

        todos_bichos = [result[i:i+4]for i in range(0, len(result), 4)]

        return todos_bichos

def CaBeca():
# 1. Pegar conteudo HTML a partir da URL
    url = "https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-16"

    html = requests.get(url)  

    if html.status_code != 200: 
            print(">> Falha na requisição! <<")
    else:
    # content passa o conteúdo da página
        html_content = html.content
    # Parsear o conteúdo HTML buscado, para poder ficar mais estruturado de acordo com as tags HTML
        soup = BeautifulSoup(html_content, 'html.parser')
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
        cabeca_7horario = result[240:244]
        cabeca_1horario.append('9:45')
        cabeca_2horario.append('10:45')
        cabeca_3horario.append('12:45')
        cabeca_4horario.append('15:45')
        cabeca_5horario.append('18:H')
        cabeca_6horario.append('20:00')
        cabeca_7horario.append('20:00')

        bichos_cabeca = [cabeca_1horario,cabeca_2horario ,cabeca_3horario ,cabeca_4horario ,cabeca_5horario ,cabeca_6horario, cabeca_7horario ]

        return bichos_cabeca

def buscar_bicho(bicho, lista):
    return [sublist for sublist in lista if bicho in sublist]

apostar_app = Blueprint("apostar_app", __name__, url_prefix="/apostar", template_folder='templates',static_folder='static')

# Tela de apostar
@apostar_app.route("/", methods=["GET", "POST"])
def mostrar():   
    return render_template("pages/apostar/mostrar.html")

@apostar_app.route("/statistica", methods=["GET", "POST"])
def statistica():   
    ver = Bichos()
    cabeca = CaBeca()
    print(cabeca)
    if request.method == 'POST':
        bicho = request.form.get("bicho")
        encotrados = buscar_bicho(bicho, ver)
        # df = pd.read_csv('resultados.csv')
        # encotrados = df.loc[df['Bicho']== bicho]

        encontrados = list(filter(lambda x: bicho in x, Bichos()))
        ver = len(encontrados)
        return render_template("pages/apostar/statistica.html",bichos=encotrados, vezes=ver,pesquisa=bicho,cabeca=cabeca)
    return render_template("pages/apostar/statistica.html",cabeca=cabeca)
