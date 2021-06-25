import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description = "Hex Dump any file using python.",
        epilog = '''Example: python hexdump.py <file>'''
    )
    parser.add_argument("file", help="Absolute or Relative path to the file.")

    args = parser.parse_args()

    return args.file


def hexDump( readString, length = 16, show = True):
    NonAsciiFilter = ''.join(
        [chr(character) if (len(repr(chr(character))) == 3) else "." for character in range(512)]
    )
    
    if isinstance(readString, bytes):
        readString = readString.decode()

    result = list()

    for block in range(0, len(readString), length):
        stringBlock = readString[block : block + length]
        
        hexBlock = " ".join([
            f"{ord(character):02X}" for character in stringBlock
        ])

        stringBlock = stringBlock.translate(NonAsciiFilter)

        blockNumber = f"{block:04X}"

        hexWidth = length * 3

        result.append(f"{blockNumber}    {hexBlock:<{hexWidth}}    {stringBlock}")

    return result


def main():
    filePath = parse_args()
    
    try:
        f = open(filePath, 'r')
        print(f"{filePath}:")
        res = "\n".join(hexDump(f.read()))

        print(res)

    except FileNotFoundError:
        print("File Not Found! Please check and try again.")

if __name__ == "__main__":
    main()