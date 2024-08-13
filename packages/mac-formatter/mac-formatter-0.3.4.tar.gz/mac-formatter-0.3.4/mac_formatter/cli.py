import argparse
from .mac_formatter import MacFormatter

def main():
    parser = argparse.ArgumentParser(description="Format MAC addresses in various styles.")
    parser.add_argument("mac_address", type=str, help="The MAC address to format")
    parser.add_argument("-f", "--format", choices=["colon", "dot", "line", "space", "blank"], 
                        help="The format to use. If not specified, all formats will be printed.")
    parser.add_argument("-u", "--uppercase", action="store_true", help="Prints the MAC address in uppercase.")
    parser.add_argument("-l", "--lowercase", action="store_true", help="Prints the MAC address in lowercase.")
    
    args = parser.parse_args()

    formatter = MacFormatter(args.mac_address)

    def format_mac_output(output):
        return output.upper() if args.uppercase else output.lower() if args.lowercase else output

    if args.format:
        if args.format == "colon":
            print(format_mac_output(formatter.colon))
        elif args.format == "dot":
            print(format_mac_output(formatter.dot))
        elif args.format == "line":
            print(format_mac_output(formatter.line))
        elif args.format == "space":
            print(format_mac_output(formatter.space))
        elif args.format == "blank":
            print(format_mac_output(formatter.blank))
    else:
        print(format_mac_output(formatter.colon))
        print(format_mac_output(formatter.dot))
        print(format_mac_output(formatter.line))
        print(format_mac_output(formatter.space))
        print(format_mac_output(formatter.blank))

if __name__ == "__main__":
    main()

