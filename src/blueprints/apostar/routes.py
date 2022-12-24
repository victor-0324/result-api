from flask import Blueprint, request, render_template, url_for, redirect
import requests  
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

        # cabecario = soup.select('b')[0 : 5]
        # bichos = soup.find_all('tbody', id=True)
        # data = soup.find_all('h3', class_='g')

        tabela = soup.find_all('div', class_="col-sm-12 col-md-6 col-lg-4")  
        novo = soup.find_all('td')
       
        return novo

apostar_app = Blueprint("apostar_app", __name__, url_prefix="/apostar", template_folder='templates',static_folder='static')


# Tela de apostar
@apostar_app.route("/", methods=["GET", "POST"])
def mostrar():   
    return render_template("pages/apostar/mostrar.html")


@apostar_app.route("/statistica", methods=["GET", "POST"])
def statistica(): 
    texto = Texto()  
    return render_template("pages/apostar/statistica.html",texto=texto)