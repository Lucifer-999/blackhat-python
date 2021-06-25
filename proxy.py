import argparse
import socket
import sys
from threading import Thread

class Proxy2Server(Thread):
    def __init__ (self, host, port) :
        super(Proxy2Server, self).__init__()

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
        print(f"Recv <--  {response.decode()}")
        return response

    
class Client2Proxy(Thread):
    def __init__ (self, host, port):
        super(Client2Proxy, self).__init__()

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
                try:
                    self.server.sendall(sendData)
                except BrokenPipeError:
                    self.client.close()
                    sys.exit("Connection Closed By Server")

    def handle(self, data):
        print(f"Send -->  {data.decode()}")
        return data


class Proxy(Thread):
    def __init__(self, fromHost, fromPort, toHost, toPort):
        super(Proxy, self).__init__()

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


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Python Proxy v1",
        epilog='''Example:
            \tpython proxy.py -l <localhost> -lp <localport> -r <remotehost> -rp <remoteport>'''
    )
    parser.add_argument('-l', '--localhost', help="Client IP Address / Hostname", required=True)
    parser.add_argument('-lp', '--localport', type=int, help="Client Port", required=True)
    parser.add_argument('-r', '--remotehost', help="Remote IP Address / Hostname", required=True)
    parser.add_argument('-rp', '--remoteport', type=int, help="Remote Port")
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if not args.remoteport:
        args.remoteport = args.localport

    proxyObject = Proxy(args.localhost, args.localport, args.remotehost, args.remoteport)
    proxyObject.start()


if __name__ == "__main__":
    main()