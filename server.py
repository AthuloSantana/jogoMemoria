import pickle
from socket import *
from threading import *
from selecionandoImagens import imagens

clients = []
nomes_clientes = {}


def clientThread(clientSocket, inicia):
    clientSocket.send(pickle.dumps(imagens))
    clientSocket.send(pickle.dumps(inicia))

    while True:
        msg = clientSocket.recv(1024)

        if not msg:
            break

        msg = pickle.loads(msg)

        for client in clients:
            if client != clientSocket:
                client.sendall(pickle.dumps(msg))


hostSocket = socket(AF_INET, SOCK_STREAM)  # Cria um socket tcp/ip
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,
                      1)  # permitindo que o endereço do soquete seja reutilizado imediatamente após o encerramento do soquete anterior

hostIp = "0.0.0.0"
portNumber = 5001
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()

print("Aguardando conexão...")

while True:
    if len(clients) < 2:
        clientSocket, clientAddress = hostSocket.accept()
        nome_cliente = clientSocket.recv(1024).decode('utf-8')

        clients.append(clientSocket)
        nomes_clientes[clientSocket] = nome_cliente

        print("Conectado por: " + nome_cliente)

    if len(clients) == 2:
        thread = Thread(target=clientThread, args=(clients[0], True))
        thread.start()

        thread2 = Thread(target=clientThread, args=(clients[1], False))
        thread2.start()
        break
