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

# Página principal, rota principal
@app.route('/principal')
def principal():
    return render_template('principal.html')

# Página letras, rota letras
@app.route('/letras')
def letras():
    return render_template('letras.html')

# Página fala, rota fala
@app.route('/fala')
def fala():
    return render_template('fala.html')

# Página perfil, rota perfil
@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

#Rota /predict para processar o arquivo da letra desenhada. 
# Converte a imagem para RGB, realiza OCR, salva e verifica se a 
# letra foi reconhecida corretamente, retornando o resultado 
# em JSON.@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    expected_letter = request.form.get('expectedLetter', '').upper()

    try:
        img = Image.open(io.BytesIO(file.read())).convert('RGB')
        img = np.array(img)

        result = ocr.ocr(img, cls=True)
        prediction = [word_info[1][0].upper() for line in result for word_info in line]
        recognized_letter = prediction[0] if prediction else 'Não reconhecido'

        # Verifica se o reconhecimento é bem-sucedido
        success = recognized_letter == expected_letter or (expected_letter == 'O' and recognized_letter == '0')

        # Salva o resultado da tentativa de reconhecimento
        #save_result(expected_letter, recognized_letter, success)

        return jsonify({'prediction': recognized_letter, 'success': success})

    except Exception as e:
        print(f'Erro durante o reconhecimento: {e}')
        return jsonify({'prediction': 'Erro ao reconhecer', 'success': False}), 500


# Rota para análise de resultados e geração de PDF, não será mais utilizada
'''@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        # Carrega os dados do CSV
        df = pd.read_csv('test_results.csv', names=['Timestamp', 'Expected', 'Recognized', 'Success'])
        
        # Calcula as taxas de acertos e erros para cada letra
        analysis = df.groupby('Expected')['Success'].mean().reset_index()
        analysis['Error Rate'] = 1 - analysis['Success']
        analysis.columns = ['Letter', 'Accuracy Rate', 'Error Rate']

        # Caminho do arquivo PDF
        pdf_path = 'letter_analysis.pdf'

        # Gera o PDF com a análise
        generate_pdf(analysis, pdf_path)

        # Envia o arquivo PDF para download
        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print(f'Erro na análise de dados: {e}')
        return jsonify({'error': 'Erro na análise de dados'}), 500'''

#Inicia o servidor Flask em modo de depuração.
if __name__ == '__main__':
    app.run(debug=True)