# Description: This file contains the server code for the chat application

import threading
import socket

# Server configuration
host = "localhost"
port = 65000

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4, TCP
server.bind((host, port))  # Bind the server to the host and port
server.listen()  # Listen for connections

# List to store clients
clients = []  # List to store clients
nicknames = []  # List to store nicknames


# def for broaadcasting messages to all clients
def broadcast(message):
    for client in clients:  # Loop through all clients
        client.send(message)  # Send message to all clients


# def for handling messages from clients
def handle(client):
    while True:
        try:
            # Broadcasting messages
            message = client.recv(1024)  # Receive message from client
            broadcast(message)  # Broadcast message to all clients
        except:
            # Removing and closing clients
            index = clients.index(client)  # Get the index of the client
            clients.remove(client)  # Remove the client from the list
            client.close()  # Close the client
            nickname = nicknames[index]  # Get the nickname of the client
            broadcast(
                f"{nickname} left the chat!".encode("ascii")
            )  # Broadcast the message
            nicknames.remove(nickname)  # Remove the nickname from the list
            break


# def for receiving messages from clients
def receive():
    while True:
        # Accept connection
        client, address = server.accept()  # Accept connection from client
        print(f"Connected with {str(address)}")  # Print the address of the client

        # Request and store nickname
        client.send("NICK".encode("ascii"))  # Send the message to the client
        nickname = client.recv(1024).decode("ascii")  # Receive nickname from the client
        nicknames.append(nickname)  # Append the nickname to the list
        clients.append(client)  # Append the client to the list

        # Print and broadcast nickname
        print(f"Nickname of the client is {nickname}")  # Print nickname of client
        broadcast(f"{nickname} joined the chat!".encode("ascii"))  # Broadcast message
        client.send("Connected to the server!".encode("ascii"))  # message to client

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))  # Create a thread
        thread.start()  # Start the thread


print("Server is listening...")  # Print message
receive()  # Call the receive function
