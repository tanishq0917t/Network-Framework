import sys
import socket
from threading import Thread
from network_common.wrappers import Request,Response
from network_server.config import Configuration
def request_processor(clientSocket,requestHandler):
    dataBytes=b''
    toReceive=1024
    while len(dataBytes)<toReceive:
        bytesRead=clientSocket.recv(toReceive-len(dataBytes))
        dataBytes+=bytesRead
    requestDataLen=int(dataBytes.decode("utf-8").strip())
    dataBytes=b''
    toReceive=requestDataLen
    while len(dataBytes)<toReceive:
        bytesRead=clientSocket.recv(toReceive-len(dataBytes))
        dataBytes+=bytesRead
    requestData=dataBytes.decode("utf-8")
    request=Request.from_json(requestData)
    response=requestHandler(request)
    responseData=response.to_json()
    clientSocket.sendall(bytes(str(len(responseData)).ljust(1024),"utf-8"))
    clientSocket.sendall(bytes(responseData,"utf-8"))
    clientSocket.close()
class NetworkServer:
    def __init__(self,requestHandler):
        self.server_configuration=Configuration()
        self.requestHandler=requestHandler
        self.server_configuration._obj._validate_values()
        if self.server_configuration._obj.has_exception:
            for exception in self.server_configuration._obj.exceptions.values():
                print(exception[1])
            sys.exit()
    def start(self):
        serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind(("localhost",self.server_configuration._obj.port))
        serverSocket.listen()
        while True:
            print(f"Server is listening in port: {self.server_configuration._obj.port}")
            clientSocket,socketName=serverSocket.accept()
            t=Thread(target=request_processor(clientSocket,self.requestHandler))
            t.start()
            
