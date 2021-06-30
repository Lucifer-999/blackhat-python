import base64
import sys

def main():
    if len(sys.argv) == 2 :
        decodedString = sys.argv[1]

    else:
        decodedString = input("Enter string: ")

    encodedString = base64.b64encode(decodedString.encode())

    print(encodedString.decode())

if __name__ == "__main__":
    main()