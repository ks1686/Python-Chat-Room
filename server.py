# Description: This file contains the server code for the chat application

import threading
import socket

# Server configuration
host = "localhost"
port = 55555

# Create a socket
sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever.bind((host, port))
sever.listen()

# List to store clients
clients = []
nicknames = []


# def for broaadcasting messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# def for handling messages from clients
def handle(client):
    while True:
        try:
            # Broadcasting messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode("ascii"))
            nicknames.remove(nickname)
            break


# def for receiving messages from clients
def receive():
    while True:
        # Accept connection
        client, address = sever.accept()
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode("ascii"))
        client.send("Connected to the server!".encode("ascii"))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
