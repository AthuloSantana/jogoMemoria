import os
import random

caminho_atual = os.getcwd()
diretorio =  os.path.join(caminho_atual, 'downloads')  # seu diretório
quantidade_de_imagens = 8

# Lista todos os arquivos no diretório
arquivos = os.listdir(diretorio)

# Filtra apenas os arquivos de imagem 
arquivos_de_imagem = [arquivo for arquivo in arquivos if arquivo.endswith(('png'))]
#escolhe 8 imagens
imagens_escolhidas = random.sample(arquivos_de_imagem, quantidade_de_imagens)

caminhosImagens = [os.path.join(diretorio, imagem) for imagem in imagens_escolhidas]

# Testando
# for caminho in caminhosImagens:
#     print(caminho)
