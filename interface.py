import tkinter as tk
from selecionandoImagens import caminhosImagens
import random            
from PIL import ImageTk, Image

# variaveis globais
ALTURA = 50
LARGURA = 60
NUM_LINHAS = 4
NUM_COLUNAS = 4
LARGURA_CARTA = 5
ALTURA_CARTA = 5


def criar_grid():
    imagens = []

    imagens = caminhosImagens * 2
    random.shuffle(imagens)

    grid = []

    for _ in range(NUM_LINHAS):
        linhas = []

        for _ in range(NUM_COLUNAS):
            imagem = imagens.pop()
            linhas.append(imagem)

        grid.append(linhas)

    return grid

 
#Layout tela
windows = tk.Tk()
windows.title('Jogo da memória: Estados Brasileiros')
windows.configure(bg='#343a40')

def fechar_carta(carta):
    carta['image'] = None
    carta['bg'] = 'black'

def abrir_carta(linha, coluna, window):
    carta = cartas[linha][coluna]
    color = carta['bg']

    if color == 'black':
        imagem = Image.open(grid[linha][coluna])
        redimensionada = imagem.resize((40,80))        

        ph = ImageTk.PhotoImage(redimensionada)

        label = tk.Label(window, image=ph)
        label.image = ph
    
        carta['image'] = ph
        carta['width'] = 40
        carta['height'] = 80
    
grid = criar_grid()
cartas = []
levantadas = []

for linha in range(NUM_LINHAS):
    linhas_cartas = []

    for col in range(NUM_COLUNAS):
        carta = tk.Button(windows, width=LARGURA_CARTA, height=ALTURA_CARTA, bg='black',  command=lambda r=linha, c=col: abrir_carta(r,c, windows))

        carta.grid(row=linha, column=col, padx=5, pady=5)
        linhas_cartas.append(carta)

    cartas.append(linhas_cartas)

estilo_botao = {'activebackground': '#f8f9fa'}
windows.option_add('button',estilo_botao)

windows.mainloop()
