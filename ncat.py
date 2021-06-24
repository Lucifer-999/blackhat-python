import shlex
import subprocess
import argparse

def execute(command):
    command = command.strip()
    if (not command):
        return

    output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
    return output.decode()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Custom NCAT Tool",
        epilog='''Example:
            \tpython ncat.py -s \t# Spawn a shell
            \tpython ncat.py -e <command>\t# Execute a command
            '''
    )
    parser.add_argument('-s', '--shell', action='store_true', help="Spawn a shell")
    parser.add_argument('-e', '--execute', help="Execute a command")

    args = parser.parse_args()

    return args


def shell():
    

def main():
    args = parse_arguments()
    
    if args.execute:
        print(execute(args.execute))

    elif args.shell:
        shell()

if __name__ == "__main__":
    main()