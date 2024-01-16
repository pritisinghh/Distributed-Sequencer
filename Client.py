import socket
from constants import GENERATOR_PORT


if __name__=="__main__":
    while True:
        input("Press enter to send getid request: ")
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        host = socket.gethostname()
    
        port = GENERATOR_PORT
        clientsocket.connect((host, port))
        msg=clientsocket.recv(1024).decode()
        print("Id Received :",msg)
        clientsocket.close()
