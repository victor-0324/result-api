from flask import Blueprint, request, render_template, url_for, redirect
import requests  
import csv
import pandas as pd 
from bs4 import BeautifulSoup  
from datetime import datetime
from builtins import str


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
        cabeca_6horario.append('20:00')
        cabeca_7horario.append('20:00')

        bichos_cabeca = [cabeca_1horario,cabeca_2horario ,cabeca_3horario ,cabeca_4horario ,cabeca_5horario ,cabeca_6horario, cabeca_7horario ]

        todos_bichos = [result[i:i+4]for i in range(0, len(result), 4)]

        return todos_bichos, bichos_cabeca

def Atrasados():
    url = "http://lotep.net/bicho-atrasado/"

    html = requests.get(url)  

    if html.status_code != 200: 
            print(">> Falha na requisição! <<")
            return []
    else:
    # content passa o conteúdo da página
        html_content = html.content
    # Parsear o conteúdo HTML buscado, para poder ficar mais estruturado de acordo com as tags HTML
        soup = BeautifulSoup(html_content, 'html.parser')
    # Pegando todo o resultados
        novo = soup.find_all('td')
        result = [pt.get_text() for pt in novo]
         # Criar lista de dicionários com as informações da tabela
        tabela = []
        for i in range(0, len(result), 3):
            linha = {
                "bicho": result[i],
                "milhar": result[i+1],
                "data": result[i+2]
            }
            tabela.append(linha)

        return tabela
        

    # extrai as dezenas correspondentes ao bicho pesquisado
    dezenas = [int(bicho_pesquisado[-2:])]
    for i in range(3):
        dezenas.append(dezenas[i] + 10)
    # filtra o dataframe para encontrar milhares correspondentes
    milhares = []
    for d in dezenas:
        milhares.extend(df[df['Milhar'] == d]['Milhar'].tolist())
    return milhares

dezenas_bicho = {
    'avestruz': ['01', '02', '03', '04'],
    'aguia': ['05', '06', '07', '08'],
    'burro': ['09', '10', '11', '12'],
    'borboleta': ['13', '14', '15', '16'],
    'cachorro': ['17', '18', '19', '20'],
    'cabra': ['21', '22', '23', '24'],
    'carneiro': ['25', '26', '27', '28'],
    'camelo': ['29', '30', '31', '32'],
    'cobra': ['33', '34', '35', '36'],
    'coelho': ['37', '38', '39', '40'],
    'cavalo': ['41', '42', '43', '44'],
    'elefante': ['45', '46', '47', '48'],
    'galo': ['49', '50', '51', '52'],
    'gato': ['53', '54', '55', '56'],
    'jacare': ['57', '58', '59', '60'],
    'leao': ['61', '62', '63', '64'],
    'macaco': ['65', '66', '67', '68'],
    'porco': ['69', '70', '71', '72'],
    'pavao': ['73', '74', '75', '76'],
    'peru': ['77', '78', '79', '80'],
    'touro': ['81', '82', '83', '84'],
    'tigre': ['85', '86', '87', '88'],
    'urso': ['89', '90', '91', '92'],
    'veado': ['93', '94', '95', '96'],
    'vaca': ['97', '98', '99', '00']
}
def get_dezenas_por_bicho(bicho):
    if bicho in dezenas_bicho:
        return dezenas_bicho[bicho]
  

    
apostar_app = Blueprint("apostar_app", __name__, url_prefix="/", template_folder='templates',static_folder='static')

# Tela de apostar
@apostar_app.route("/todos-os-bichos", methods=["GET", "POST"])
def mostrar():
   
    ver, cabeca = Bichos()
    nomes_bichos = [item[3] for item in cabeca if len(item) > 3]
    minha_que_saiu = [item[1]  for item in ver if len(item) > 1]
    milhar_se_saiu = list(map(int, minha_que_saiu))
    df = pd.read_csv("bichos.csv")
    df = df.drop(columns=['Unnamed: 0'])
    df = df.dropna()
    df.rename(columns={'0': 'Posicao', 
                    '1': 'Milhar', 
                    '2': 'Grupo', 
                    '3': 'Bichos'}, inplace=True)

    df_pos1 = df[df['Posicao'] == "1º"]
    milhares_pos = df_pos1.groupby('Milhar').size().reset_index(name='counts')
    milhares_pos1 = milhares_pos.iloc[211:].head(20).to_dict(orient='records')
    top = df.groupby(['Milhar']).size().reset_index(name='counts')
    milhares = top.sort_values(by='counts', ascending=False)
    milhar1 = milhares.iloc[17:].head(16).to_dict(orient='records')
    milhar2 = milhares.iloc[33:].head(16).to_dict(orient='records')
    milhar3 = milhares.iloc[150:].head(16).to_dict(orient='records')
    milhar4 = milhares.iloc[503:].head(16).to_dict(orient='records')
    milhar5 = milhares.iloc[1143:].head(16).to_dict(orient='records')
    milhar6 = milhares.iloc[3505:].head(16).to_dict(orient='records')

    if request.method == "POST":
        bicho_pesquisado = request.form.get("bicho")
        dezenas_str = get_dezenas_por_bicho(bicho_pesquisado)

        if dezenas_str is not None:
            dezenas = dezenas_str
            mostrar = "Dezenas pesquisadas"
        else:
            dezenas = []
      
        return render_template("pages/apostar/mostrar.html", milhares_pos1=milhares_pos1, milhar_se_saiu=milhar_se_saiu,
                            milhar1=milhar1, milhar2=milhar2, milhar3=milhar3, milhar4=milhar4, milhar5=milhar5,
                            milhar6=milhar6, nomes_bichos=nomes_bichos, dezenas=dezenas, mostrar=mostrar, bicho_pesquisado=bicho_pesquisado)

    return render_template("pages/apostar/mostrar.html", milhares_pos1=milhares_pos1, milhar_se_saiu=milhar_se_saiu,
                           milhar1=milhar1, milhar2=milhar2, milhar3=milhar3, milhar4=milhar4, milhar5=milhar5,
                           milhar6=milhar6, nomes_bichos=nomes_bichos)

@apostar_app.route("/statistica", methods=["GET", "POST"])
def statistica(): 
    atrasado = Atrasados() 
    ver, cabeca = Bichos()
    nomes_bichos = [item[3] for item in cabeca if len(item) > 3]
    minha_que_saiu = [item[1]  for item in ver if len(item) > 1]
    milhar_se_saiu = list(map(int, minha_que_saiu))
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
    
# Top 10 milhar
    top = df.groupby(['Milhar']).size().reset_index(name='counts')
    milhares = top.sort_values(by='counts', ascending=False)
    top_m = milhares.iloc[1:].head(16).to_dict(orient='records')
    
# Quantas vezes cada Bicho saio do 1º ao 10º
    busca_nos_10 = df[df['Posicao'] >= '1º']
    todos = busca_nos_10.groupby(['Bichos']).size().reset_index(name='counts')
    menos_decimos = todos.sort_values(by='counts', ascending=True)
    nos_decimos = todos.sort_values(by='counts', ascending=False)
    nos_decimos = nos_decimos.head(13).to_dict(orient='records')
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
            return render_template("pages/apostar/statistica.html", pesquisa=bicho, cabeca=cabeca, menos_frequentes=menos_frequentes,bichos_mais_frequentes=bichos_mais_frequentes,pesquisa_m=milhar,valor=valor,resultado=resultado,top_m=top_m,nos_decimos=nos_decimos,menos_decimo=menos_decimo,atrasado=atrasado,nomes_bichos=nomes_bichos,milhar_se_saiu=milhar_se_saiu)
        elif 'bicho' in request.form:
            if bicho is not None:
                encontrados = list(filter(lambda x: bicho in x, ver))
                vezes = len(encontrados)
            else:
                encontrados = []
                vezes = 0
            return render_template("pages/apostar/statistica.html",bichos=encontrados, vezes=vezes, pesquisa=bicho, cabeca=cabeca, menos_frequentes=menos_frequentes,bichos_mais_frequentes=bichos_mais_frequentes,pesquisa_m=milhar,top_m=top_m,nos_decimos=nos_decimos,menos_decimo=menos_decimo,atrasado=atrasado,nomes_bichos=nomes_bichos,milhar_se_saiu=milhar_se_saiu)
    return render_template("pages/apostar/statistica.html",cabeca=cabeca, menos_frequentes=menos_frequentes,bichos_mais_frequentes=bichos_mais_frequentes,top_m=top_m,nos_decimos=nos_decimos,menos_decimo=menos_decimo,atrasado=atrasado,nomes_bichos=nomes_bichos,milhar_se_saiu=milhar_se_saiu) 

