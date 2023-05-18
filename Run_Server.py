import socket
import threading
from Filter_functions import make_prediction

HOST = '127.0.0.1'
PORT = 9090

server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):

    for client in clients:
        client.send(message)
    

def handle(client): 
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            if(make_prediction(message)==0):
                broadcast(message)
            else:
                client.send("Hatefull Comments are not Allowed\n".encode('utf-8'))

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():

    while True:
        client , address = server.accept()
        print(f"connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of  the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server ".encode('utf-8'))

        thread = threading.Thread(target = handle , args = (client,))
        thread.start()


print("Server connected...")
receive()