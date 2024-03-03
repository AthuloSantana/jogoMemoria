import tkinter as tk
from selecionandoImagens import caminhosImagens
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

# Array dos botões da interface
botoes_cartas = []

# Array dos caminhos de cartas
cartas = []

# Thread para receber as mensagens do servidor
def recvMessage(socket):
    while True:
        serverMessage = socket.recv(1024)

        if not serverMessage:
            break

        serverMessage = pickle.loads(serverMessage)
        abrir_carta(serverMessage[0], serverMessage[1])

# Retorna a carta para o estado fechado
def fechar_carta(carta):
    carta['image'] = None
    carta['bg'] = 'black'

# Função utilizada no clique de uma carta
def clicar(x, y, socket):
    socket.sendall(pickle.dumps((x,y)))
    abrir_carta(x, y)

# Função utilizada para virar uma carta
def abrir_carta(linha, coluna):
    # Variável global da janela
    global windows

    # Obter o botão na posição do clique
    carta = botoes_cartas[linha][coluna]

    # Variavel do fundo da carta
    color = carta['bg']

    # VERIFICAR
    if color == 'black':
        imagem = Image.open(cartas[linha][coluna])
        redimensionada = imagem.resize((40,80))        

        ph = ImageTk.PhotoImage(redimensionada)

        label = tk.Label(windows, image=ph)
        label.image = ph
    
        carta['image'] = ph
        carta['width'] = 40
        carta['height'] = 80

# Método para iniciar a interface
def iniciar(socket):
    # Variável global da janela, para ser acessivel de outros métodos
    global windows

    #Layout tela
    windows = tk.Tk()
    windows.title('Jogo da memória: Estados Brasileiros')
    windows.configure(bg='#343a40')

    for linha in range(NUM_LINHAS):
        linhas_cartas = []

        for col in range(NUM_COLUNAS):
            carta = tk.Button(windows, width=LARGURA_CARTA, height=ALTURA_CARTA, bg='black',  command=lambda r=linha, c=col: clicar(r,c, socket))

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

        # Enviar nome do usuário
        socket.sendall(str(nome).encode())

        print('Conectado')

        # Receber a matriz de cartas
        cartas = pickle.loads(socket.recv(1024))

        # Iniciar as threads da interface e de escutar o servidor.
        recvThread = threading.Thread(target=recvMessage, args=(socket,))
        recvThread.start()

        interfaceThread = threading.Thread(target=iniciar, args=(socket,))
        interfaceThread.start()

    except Exception as e:
        print('Um erro aconteceu' + e.__dict__)