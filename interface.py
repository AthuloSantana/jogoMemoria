import pickle
import socket
import threading
import tkinter as tk

from PIL import ImageTk, Image

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

aberto = []

pontos_server = 0
pontos = 0


# Thread para receber as mensagens do servidor
def recvMessage(socket):
    global pontos_server

    while True:
        serverMessage = socket.recv(1024)

        if not serverMessage:
            break

        serverMessage = pickle.loads(serverMessage)

        if isinstance(serverMessage, bool):
            aberto.clear()

            if serverMessage:
                trava_tudo()
            else:
                destrava_tudo()

        if isinstance(serverMessage, tuple):
            abrir_carta(serverMessage[0], serverMessage[1])
            x, y = serverMessage[0], serverMessage[1]
            aberto.append(botoes_cartas[x][y])

            if len(aberto) == 2:
                res = verificar()

                if res:
                    pontos_server += 1


# Retorna a carta para o estado fechado
def fechar_carta(carta):
    carta['image'] = ''
    carta['width'] = LARGURA_CARTA
    carta['height'] = ALTURA_CARTA
    carta['bg'] = 'black'


# Função utilizada no clique de uma carta
def clicar(x, y, socket):
    global pontos
    socket.sendall(pickle.dumps((x, y)))

    carta = botoes_cartas[x][y]
    aberto.append(carta)
    abrir_carta(x, y)

    if len(aberto) == 2:
        res = verificar()

        if res:
            pontos += 1
        else:
            socket.sendall(pickle.dumps(False))
            trava_tudo()


def verificar():
    c1x, c1y = coordenada(aberto[0])
    c2x, c2y = coordenada(aberto[1])

    c1 = cartas[c1x][c1y]
    c2 = cartas[c2x][c2y]

    btn1 = aberto[0]
    btn2 = aberto[1]

    aberto.clear()

    if c1 != c2:
        global windows
        windows.after(1000, lambda: close())
        botoes_cartas[c1x][c1y].config(command=None)
        botoes_cartas[c2x][c2y].config(command=None)


    def close():
        fechar_carta(btn1)
        fechar_carta(btn2)

    return c1 == c2


def travar(x, y):
    botoes_cartas[x][y]['state'] = 'disabled'


def destravar(x, y):
    botoes_cartas[x][y]['state'] = 'normal'


def trava_tudo():
    for array in botoes_cartas:
        for carta in array:
            x, y = coordenada(carta)
            travar(x, y)


def destrava_tudo():
    for array in botoes_cartas:
        for carta in array:
            x, y = coordenada(carta)
            destravar(x, y)


def coordenada(carta):
    for x, array in enumerate(botoes_cartas):
        for y, item in enumerate(array):
            if item == carta:
                return x, y
                break

    return None


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
        redimensionada = imagem.resize((40, 80))

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

    # Layout tela
    windows = tk.Tk()
    windows.title(f'{nome}_Estados Brasileiros')
    windows.configure(bg='#343a40')

    for linha in range(NUM_LINHAS):
        linhas_cartas = []

        for col in range(NUM_COLUNAS):
            carta = tk.Button(windows, width=LARGURA_CARTA, height=ALTURA_CARTA, bg='black',
                              command=lambda r=linha, c=col: clicar(r, c, socket))

            carta.grid(row=linha, column=col, padx=5, pady=5)
            linhas_cartas.append(carta)

        botoes_cartas.append(linhas_cartas)

    estilo_botao = {'activebackground': '#f8f9fa'}
    windows.option_add('button', estilo_botao)

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

        # Se o jogador inicia
        inicia = pickle.loads(socket.recv(1024))

        # Iniciar as threads da interface e de escutar o servidor.
        recvThread = threading.Thread(target=recvMessage, args=(socket,))
        recvThread.start()

        interfaceThread = threading.Thread(target=iniciar, args=(socket,))
        interfaceThread.start()

        if not inicia:
            import time

            time.sleep(1)
            trava_tudo()



    except Exception as e:
        print('Um erro aconteceu' + e.__dict__)
