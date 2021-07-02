import os
import paramiko
import socket
import sys
import threading


def getPort():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(f"Usage: python {sys.argv[0]} <port> [default port is 22]")
            print(f"Example: python {sys.argv[0]} 22")
            sys.exit(0)

        try:
            if int(sys.argv[1]) < 49152 and int(sys.argv[1]) > 0:
                port = int(sys.argv[1])
        except ValueError:
            print("Please provide a proper port number.")
            sys.exit(1)

    else:
        port = 22

    return port


def main():
    port = getPort()
    host = "127.0.0.1"

if __name__ == "__main__":
    main()