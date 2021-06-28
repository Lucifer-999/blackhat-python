import getpass
import paramiko
import sys


def ssh_connect (user, ssh_password, host, ssh_port, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(host, port=ssh_port, username=user, password=ssh_password)

    _, output, error = client.exec_command(command)

    result = output.readlines() + error.readline()

    if result:
        print("Output:\n")
        for line in result:
            print(line.strip())


def main():
    if len(sys.argv) != 5:
        print(f"Usage:\t\tpython {sys.argv[0]} <user> <host/ip of server> <port> <command>")
        print(f"Example:\tpython {sys.argv[0]} root 127.0.0.1 22 whoami")
        exit

    user = sys.argv[1]
    password = getpass.getpass()
    host = sys.argv[2]
    port = sys.argv[3]
    cmd = sys.argv[4]

    ssh_connect(user, password, host, port, cmd)

if __name__ == "__main__":
    main()