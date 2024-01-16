import socket
import threading
from constants import GENERATOR_PORT , START_SERVER_PORT , SERVER_CNT ,HOST
from time import sleep

'''
class Generator has start to initialise the socket for recieving the request from client
broadcast function to send the message to all the servers
'''
class Generator:
    def __init__(self, host, port, server_cnt):
        self.host = host
        self.port = port
        self.id = 1
        self.server_cnt = server_cnt

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print("Generator/Sequencer started listening...")
            while True:
                cs,(conn, addr) = s.accept()  
                print("Getid Req Received from client " , addr,conn)
                message=self.id
                broadcastThread=threading.Thread(target=self.broadcast(message=str(message),connection_socket=cs))
                broadcastThread.start()
                self.id += 1   

    def broadcast(self,message,connection_socket):
        servers = []

        def send_to_server(port , message):
            serverName = socket.gethostbyname(socket.gethostname())
            serverSocket = port
            print("Broadcasting to server " , serverSocket)
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName, serverSocket))
            clientSocket.send(message.encode())
            msg = clientSocket.recv(1024)
            # print("Server sending back",msg)
            try:
                connection_socket.send(bytes(msg))
                print("Response sending to client....")
                sleep(2.0)
            except:
                pass
        
            return
            
        for i in range(SERVER_CNT):
            t1 = threading.Thread(target=(send_to_server) , args = (START_SERVER_PORT + i , message , ))
            servers.append(t1)
        
        for i in range(SERVER_CNT):
            servers[i].start()

        for i in range(SERVER_CNT):
            servers[i].join()


if __name__=="__main__":
    generator=Generator(HOST,GENERATOR_PORT,SERVER_CNT)
    generator.start()
