from flask import Blueprint, request, render_template, url_for, redirect
import requests  
import json
from bs4 import BeautifulSoup  


url = ["https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-02",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-03",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-04",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-05",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-06",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-07",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-08",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-09",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-10",
"https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB/do-dia/2023-01-11",
]

for lista in url:

    html = requests.get(lista)  

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
        cabeca_1horario = result[0:4]
        cabeca_2horario = result[40:44]
        cabeca_3horario = result[80:84]
        cabeca_4horario = result[120:124]
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
        bichos_cabeca = [cabeca_1horario,cabeca_2horario ,cabeca_3horario ,cabeca_4horario ,cabeca_5horario ,cabeca_6horario]

        todos_bichos = [result[i:i+4]for i in range(0, len(result), 4)]
        
      
        for i in bichos_cabeca:
            if '03' in i: 
                print(i)

            # if i == '22':
            #     print(i)
               

    # Pegando os horarios
        # novo = soup.find_all('h3')
        # resulte = [pt.get_text() for pt in novo]
        # for i in resulte:
        #     lista_result = i.split(',')
        #     lista_result.pop(0)
        #     hor = list(filter(None, lista_result))
        #     horarios = ','.join(hor)
        #     print(horarios)

            
