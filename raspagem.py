import os
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import threading

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "image/avif,image/webp,/",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin"
    }


url = 'https://www.infoescola.com/geografia/estados-do-brasil/'
htmldata = requests.get(url, headers=headers)
soup = BeautifulSoup(htmldata.text, 'html.parser')

images = soup.find_all('img', class_='aligncenter')

save_directory = 'D:\SistemasDistribuidos\jogoMemoria\downloads'
os.makedirs(save_directory, exist_ok=True)


def download_imagem(url):
    nome = url.split('/')[-1]
    caminho_imagem = os.path.join(save_directory, nome)
    response = requests.get(url, headers=headers)

    if response.ok:
        with open(caminho_imagem, 'wb') as image_file:
            image_file.write(response.content)
        print(f'Imagem {caminho_imagem} baixada com sucesso.')
    else:
        print(f'Falha ao baixar {caminho_imagem}. Código de status: {response.status_code} {url}')

for image in images:
    url = image.attrs.get('src') ## Obtém um dicionario e busca todos os atributos src de image
    
    if url.endswith('png'):
       thread = threading.Thread(target=download_imagem, args=(url, ))
       thread.start()
