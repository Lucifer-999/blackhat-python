from threading import Thread
import socket

class Proxy2Server(Thread):
    def __init__ (self, host, port) :
        self.host = host
        self.port = port
        self.client = None # Will be initialized later

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.host, self.port))

    def run(self):
        while True:
            response = self.server.recv(4096)
            if response:
                sendResponse = self.handle(response)
                self.client.sendall(sendResponse)

    def handle(self, response):
        print(f"Recv  <-- {response.encode('hex')}")
        return response

    
class Client2Proxy(Thread):
    def __init__ (self, host, port):
        self.host = host
        self.port = port
        self.server = None  # Will be initialized later

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((self.host, self.port))
        sock.listen(1)

        self.client, _ = sock.accept()

    def run(self):
        while True:
            data = self.client.recv(4096)
            if data:
                sendData = self.handle(data)
                self.server.sendall(sendData)

    def handle(self, data):
        print(f"Send  --> {data.encode('hex')}")
        return data


class Proxy(Thread):
    def __init__(self, fromHost, fromPort, toHost, toPort):
        self.fromHost = fromHost
        self.fromPort = fromPort
        self.toHost = toHost
        self.toPort = toPort

    def run(self):
        print(f"Setting Up Proxy [{self.fromHost}:{self.fromHost} -> {self.toHost}:{self.toPort}]")
        
        self.Client = Client2Proxy(self.fromHost, self.fromPort)
        self.Server = Proxy2Server(self.toHost, self.toPort)

        print(f"Proxy Connected [{self.fromHost}:{self.fromHost} -> {self.toHost}:{self.toPort}]")

        # Setting the server and client of objects
        self.Client.server = self.Server.server
        self.Server.client = self.Client.client

        self.Server.start()
        self.Client.start()

