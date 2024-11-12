#####################################################################################################################
# AUTOR(S): Maria Fernanda de Oliveira Mazzo, Hellen Caroline de Melo                                               #
#                                                                                                                   #
# OBJETIVO: Software para pré-alfabetização de crianças com autismo.                                                #
#                                                                                                                   #
# DESCRIÇÂO: Esse código é uma aplicação web em Flask que utiliza o PaddleOCR para reconhecer letras desenhadas,    # 
# pode salvar os resultados em um arquivo CSV, gera análises em PDF e permite o download do arquivo. Sendo assim,   #
# cria uma interface onde o usuário possa desenhar uma letra, verificar se a letra foi corretamente reconhecida     #
# pelo sistema, armazenar os resultados, e gerar um relatório com as taxas de acerto e erro.                        #
#                                                                                                                   #
# DATA (última alteração): 02/11/2024                                                                               #
#####################################################################################################################


# BIBLIOTECAS:
# Flask - para o servidor
# PaddleOCR - para reconhecimento óptico de caracteres
# Numpy e PIL - para processamento de imagem
# csv - salvar dados
# datatime - para timestamp
# pandas - para manipulação de dados
# reportlab- para gerar os pdf

from flask import Flask, request, jsonify, render_template, send_file
from paddleocr import PaddleOCR
import numpy as np
import io
from PIL import Image
import csv
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

#Cria a instância da aplicação Flask
app = Flask(__name__)

# Inicializa o OCR, defini linguagem
ocr = PaddleOCR(use_angle_cls=True, lang='pt')

# Função para salvar os resultados em um arquivo CSV e PDF, 
# Está comentada, pois não será mais utilizada.
'''def save_result(expected, recognized, success):
    with open('test_results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), expected, recognized, success])

# Função para gerar PDF da análise
def generate_pdf(dataframe, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("Helvetica", 12)

    # Título
    c.drawString(100, 800, "Análise de Reconhecimento de Letras - Taxa de Acertos e Erros")
    c.drawString(100, 780, f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Cabeçalho
    c.drawString(50, 750, "Letra")
    c.drawString(150, 750, "Taxa de Acertos")
    c.drawString(300, 750, "Taxa de Erros")

    # Dados
    y = 730
    for _, row in dataframe.iterrows():
        c.drawString(50, y, row['Letter'])
        c.drawString(150, y, f"{row['Accuracy Rate']:.2%}")
        c.drawString(300, y, f"{row['Error Rate']:.2%}")
        y -= 20

    c.save()'''

# Página inicial, rota inicial
@app.route('/')
def index():
    return render_template('index.html')


#Inicia o servidor Flask em modo de depuração.
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)