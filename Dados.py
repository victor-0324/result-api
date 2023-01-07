from flask import Blueprint, request, render_template, url_for, redirect
import requests  
from bs4 import BeautifulSoup  
from datetime import datetime
import pandas as pd


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
    res = [pt.get_text() for pt in novo]
    i = input('Digite o numero de um bicho')
    for i in res:
        if i == '06':
            print(i , 'Cabra')

#     Horarios
#     tabela = soup.find_all('div', class_="col-sm-12 col-md-6 col-lg-4")  
#     novo = soup.find_all('h3')

#   Tabelas
   
       
    
        
    # dia = pd.DataFrame({
        
    # })
    # print(res[0])

