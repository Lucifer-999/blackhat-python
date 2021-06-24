import socket
import threading

ip = "0.0.0.0"
port = 8080

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    print(f"[*] Listening {ip}:{port}")

    while True:
        try:
            client, addr = server.accept()
            print(f"[*] Connection recieved from {addr[0]}:{addr[1]}")
            handler = threading.Thread(target = handler_func, args = (client,addr[0]))
            handler.start()
        except KeyboardInterrupt:
            exit()


def handler_func(client_sock, address):
    with client_sock as socket:
        while True:
            try:
                request = socket.recv(1024)
                print(f"[*] Recvd ({address}): {request.decode('utf-8')}")
                socket.send(b'ACK')
            except BrokenPipeError:
                break

if __name__ == "__main__":
    main()
