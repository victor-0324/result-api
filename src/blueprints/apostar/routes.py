from flask import Blueprint, request, render_template, url_for, redirect
import requests  
import csv
import pandas as pd 
from bs4 import BeautifulSoup  
from datetime import datetime

def Bichos():
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
        cabeca_1horario.append('09:45')
        cabeca_2horario.append('10:45')
        cabeca_3horario.append('12:45')
        cabeca_4horario.append('15:45')
        cabeca_5horario.append('18:H')
        cabeca_6horario.append('19:00')
        cabeca_7horario.append('20:00')

        bichos_cabeca = [cabeca_1horario,cabeca_2horario ,cabeca_3horario ,cabeca_4horario ,cabeca_5horario ,cabeca_6horario, cabeca_7horario ]

        todos_bichos = [result[i:i+4]for i in range(0, len(result), 4)]

        return todos_bichos, bichos_cabeca



apostar_app = Blueprint("apostar_app", __name__, url_prefix="/apostar", template_folder='templates',static_folder='static')

# Tela de apostar
@apostar_app.route("/", methods=["GET", "POST"])
def mostrar():   
    return render_template("pages/apostar/mostrar.html")

@apostar_app.route("/statistica", methods=["GET", "POST"])
def statistica():   
    ver, cabeca = Bichos()
    df = pd.read_csv("bichos.csv")
    df = df.drop(columns=['Unnamed: 0'])
    df = df.dropna()
    df.rename(columns={'0': 'Posicao', 
                    '1': 'Milhar', 
                    '2': 'Grupo', 
                    '3': 'Bichos'}, inplace=True)
# Top 10 mais e menos que sairam
    df_posicao_1 = df[df['Posicao'] == '1º']
    agrupado = df_posicao_1.groupby(['Bichos']).size().reset_index(name='counts')
    agrupado_mas = agrupado.sort_values(by='counts', ascending=False)
    agrupado = agrupado.sort_values(by='counts', ascending=True)
    menos_frequentes = agrupado.head(12).to_dict(orient='records')
    bichos_mais_frequentes  = agrupado_mas.head(13).to_dict(orient='records')

#  Top 10 milhar
    top = df.groupby(['Milhar']).size().reset_index(name='counts')
    milhares = top.sort_values(by='counts', ascending=False)
    top_m = milhares.iloc[1:].head(16).to_dict(orient='records')
     
#   Quantas vezes cada Bicho saio do 1º ao 10º
    busca_nos_10 = df[df['Posicao'] >= '1º']
    todos = busca_nos_10.groupby(['Bichos']).size().reset_index(name='counts')
    menos_decimos = todos.sort_values(by='counts', ascending=True)
    nos_decimos = todos.sort_values(by='counts', ascending=False)
    nos_decimos = nos_decimos.head(12).to_dict(orient='records')
    menos_decimo = menos_decimos.head(12).to_dict(orient='records')
    if request.method == 'POST':
        # Pesquisa milhar 
        milhar = request.form.get("milhar")
        bicho = request.form.get("bicho")
        if 'milhar' in request.form:
            if milhar is None:
                return render_template("pages/apostar/statistica.html", error="Erro")
            try:
                milhar_int = int(milhar)
            except ValueError :
                return render_template("pages/apostar/statistica.html", error="Erro")
                
            df = pd.read_csv("bichos.csv")
            df = df.drop(columns=['Unnamed: 0'])
            df = df.dropna()
            df.rename(columns={'0': 'Posicao', 
                        '1': 'Milhar', 
                        '2': 'Grupo', 
                        '3': 'Bichos'}, inplace=True)
            
            resultado = df.loc[df['Milhar'] == milhar_int].to_dict('records')
            valor = len(resultado)
            pesquisa_m = milhar
            return render_template("pages/apostar/statistica.html", pesquisa=bicho, cabeca=cabeca, menos_frequentes=menos_frequentes,bichos_mais_frequentes=bichos_mais_frequentes,pesquisa_m=milhar,valor=valor,resultado=resultado,top_m=top_m,nos_decimos=nos_decimos,menos_decimo=menos_decimo)
        elif 'bicho' in request.form:
            if bicho is not None:
                encontrados = list(filter(lambda x: bicho in x, ver))

                vezes = len(encontrados)
            else:
                encontrados = []
                vezes = 0
            return render_template("pages/apostar/statistica.html",bichos=encontrados, vezes=vezes, pesquisa=bicho, cabeca=cabeca, menos_frequentes=menos_frequentes,bichos_mais_frequentes=bichos_mais_frequentes,pesquisa_m=milhar,top_m=top_m,nos_decimos=nos_decimos,menos_decimo=menos_decimo)
    return render_template("pages/apostar/statistica.html",cabeca=cabeca, menos_frequentes=menos_frequentes,bichos_mais_frequentes=bichos_mais_frequentes,top_m=top_m,nos_decimos=nos_decimos,menos_decimo=menos_decimo)