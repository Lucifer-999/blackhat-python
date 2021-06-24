import socket

host = "localhost"
port = 8080

data = b"GET / HTTP\1.1\r\nHost: www.google.com\r\n\r\n"

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(data, (host,port))

response, addr = client.recvfrom(4096)

print(response.decode())

client.close()

