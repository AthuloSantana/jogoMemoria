import tkinter as tk
from selecionandoImagens import caminhosImagens
import random            
from PIL import ImageTk, Image
import socket
import threading
import pickle

# variaveis globais
ALTURA = 50
LARGURA = 60
NUM_LINHAS = 4
NUM_COLUNAS = 4
LARGURA_CARTA = 5
ALTURA_CARTA = 5

IP = 'localhost'
PORTA = 5001

botoes_cartas = []
levantadas = []
cartas = []

def recvMessage(socket):
    while True:
        serverMessage = socket.recv(1024)

        if not serverMessage:
            break

        serverMessage = pickle.loads(serverMessage)
        abrir_carta(serverMessage[0], serverMessage[1])

def fechar_carta(carta):
    carta['image'] = None
    carta['bg'] = 'black'

def clicar(x, y, window, socket):
    socket.sendall(pickle.dumps((x,y)))
    abrir_carta(x, y, window)

def abrir_carta(linha, coluna):
    global windows

    carta = botoes_cartas[linha][coluna]
    color = carta['bg']

    if color == 'black':
        imagem = Image.open(cartas[linha][coluna])
        redimensionada = imagem.resize((40,80))        

        ph = ImageTk.PhotoImage(redimensionada)

        label = tk.Label(windows, image=ph)
        label.image = ph
    
        carta['image'] = ph
        carta['width'] = 40
        carta['height'] = 80
    
def iniciar(socket):
    global windows
    #Layout tela
    windows = tk.Tk()
    windows.title('Jogo da memória: Estados Brasileiros')
    windows.configure(bg='#343a40')

    for linha in range(NUM_LINHAS):
        linhas_cartas = []

        for col in range(NUM_COLUNAS):
            carta = tk.Button(windows, width=LARGURA_CARTA, height=ALTURA_CARTA, bg='black',  command=lambda r=linha, c=col: clicar(r,c, windows, socket))

            carta.grid(row=linha, column=col, padx=5, pady=5)
            linhas_cartas.append(carta)

        botoes_cartas.append(linhas_cartas)

    estilo_botao = {'activebackground': '#f8f9fa'}
    windows.option_add('button',estilo_botao)

    windows.mainloop()

if __name__ == "__main__":
    nome = input('Nome: ')

    try:
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket.connect((IP, PORTA))
        socket.sendall(str(nome).encode())

        print('Conectado')

        cartas = pickle.loads(socket.recv(1024))

        recvThread = threading.Thread(target=recvMessage, args=(socket,))
        recvThread.start()

        interfaceThread = threading.Thread(target=iniciar, args=(socket,))
        interfaceThread.start()

    except Exception as e:
        print('Um erro aconteceu' + e.__dict__)