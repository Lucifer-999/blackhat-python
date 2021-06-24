import socket

host = "127.0.0.1"
port = 8080

data = b"GET / HTTP/1.1\r\nHost: www.meusec.com\r\n\r\n"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host,port))

client.send(data)

response = client.recv(4096)

print(response.decode())

client.close()

