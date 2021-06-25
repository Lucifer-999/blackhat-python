import threading
import socket

class Proxy2Server:
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
                self.handle(response)
                self.client.sendall(response)

    def handle(self, response):
        print(f"Recv  <-- {response.encode('hex')}")

    
class Client2Proxy:
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
                self.handle(data)
                self.server.sendall(data)

    def handle(self, data):
        print(f"Send  --> {data.encode('hex')}")


class Proxy(threading.Thread):
    def __init__(self, fromHost, fromPort, toHost, toPort):
        self.fromHost = fromHost
        self.fromPort = fromPort
        self.toHost = toHost
        self.toPort == toPort

    def run(self):
        
    
