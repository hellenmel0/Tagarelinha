# Etapa 1: Construir a imagem com uma imagem do Python oficial
FROM python:3.11-slim as builder

# Definir diretório de trabalho
WORKDIR /app

# Copiar o arquivo requirements.txt para instalar as dependências
COPY requirements.txt .

# Instalar as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Etapa 2: Criar a imagem final usando a imagem distroless da Chainguard
FROM ghcr.io/chainguard/python-distroless:latest

# Definir diretório de trabalho
WORKDIR /app

# Copiar as dependências instaladas e o código da aplicação do estágio de build
COPY --from=builder /app /app

# Definir a variável de ambiente para o comando que será executado
CMD ["python", "main.py"]
