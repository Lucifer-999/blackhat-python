import base64
import sys

def main():
    if len(sys.argv) == 2 :
        encodedString = sys.argv[1]

    else:
        encodedString = input("Enter Base64 Endoded string: ")

    decodedString = base64.b64decode(encodedString)

    print(decodedString.decode())

if __name__ == "__main__":
    main()