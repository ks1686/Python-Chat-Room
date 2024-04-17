# client program for the chat application

import re
import threading
import socket

# Nickname of the client
nickname = input("Choose a nickname: ")  # Ask the user to choose a nickname

# Client configuration
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4, TCP
client.connect(("localhost", 55555))  # Connect to the server


# Function to receive messages from the server
def receive():
    while True:
        try:
            # Receive message from server
            message = client.recv(1024).decode("ascii")  # Receive message from server
            if message == "NICK":
                client.send(nickname.encode("ascii"))  # Send nickname to the server
            else:
                print(message)  # Print message
        except:
            # Close the connection
            print("An error occurred!")
            client.close()  # Close the connection
            break


def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode("ascii"))


# Create threads for receiving and writing messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
