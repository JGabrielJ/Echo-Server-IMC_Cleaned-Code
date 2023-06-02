# imports the necessary libraries to connect to 'server.py',
# send the data to the server and instantiate the client
import socket, json
from app import App

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the IP address of the local machine (localhost)
# this IP address must be the same as the server IP
host = '127.0.0.1'
# server port
port = 9999

# connecting client to server
client_socket.connect((host, port))

# create a App object
client_app = App()

# collecting user data
while True:
    try:
        values = client_app.collect_user_data()
    except KeyboardInterrupt:
        print('\n\nValor inválido!\n'.upper())
        App.generate_header()
    else:
        break

# processing user data
list_data = client_app.validate_data(values)
final_data = client_app.generate_dict(list_data)

# serializing data (pass data to json)
data = json.dumps(final_data)

# pass to bytes
data = data.encode('ascii')

# send data to server
client_socket.send(data)

# receive no more than 1024 bytes and pass to json
response = client_socket.recv(1024).decode()

# pass to dict
response = json.loads(response)

# instantiate the menu
while True:
    try:
        client_app.menu(response)
    except KeyboardInterrupt:
        App.padding()
        print('\nErro: Opção Inválida!')
    else:
        break

# close connection
client_socket.close()
