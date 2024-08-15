import argparse
from .mac_formatter import MacFormatter

def main():
    parser = argparse.ArgumentParser(
        description="Format MAC addresses in various styles."
    )
    
    parser.add_argument(
        'mac_address',
        type=str,
        help="The MAC address to format (e.g., AB:CD:EF:12:34:56)."
    )
    
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['colon', 'dot', 'dash', 'ddash', 'space', 'blank', 'binary', 'compact', 'eui64', 'bpf', 'reverse'],
        help=(
            "The format to use. If not specified, all formats will be printed.\n"
            "Available formats:\n"
            "  colon       : Colon-separated format, e.g., ab:12:cd:34:ef:56.\n"
            "  dot         : Dot notation, e.g., abcd.ef12.3456.\n"
            "  dash        : Hyphen-separated format, e.g., ab-12-cd-34-ef-56.\n"
            "  ddash       : Double-dash-separated format, e.g., ab12-cd34-ef56.\n"
            "  space       : Space-separated format, e.g., ab 12 cd 34 ef 56.\n"
            "  blank       : Continuous string with no delimiters, e.g., ab12cd34ef56.\n"
            "  binary      : Binary format, e.g., 10101011 00010010 11001101 00110100 11101111 01010110.\n"
            "  compact     : Base64 encoded format, e.g., qXLNTq9W.\n"
            "  eui64       : Cisco EUI-64 format, e.g., ab12.cd34.fffe.ef56.\n"
            "  bpf         : BPF format with each byte prefixed by '\\x', e.g., \\xab\\x12\\xcd\\x34\\xef\\x56.\n"
            "  reverse     : Reverse byte order, e.g., 56ef34cd12ab."
        )
    )
    
    parser.add_argument(
        '-u', '--uppercase',
        action='store_true',
        help="Prints the MAC address in uppercase."
    )

    parser.add_argument(
        '-l', '--lowercase',
        action='store_true',
        help="Prints the MAC address in lowercase."
    )
    
    args = parser.parse_args()

    formatter = MacFormatter(args.mac_address)

    def format_mac_output(output):
        return output.upper() if args.uppercase else output.lower() if args.lowercase else output

    if args.format:
        if args.format == "colon":
            print(format_mac_output(formatter.colon))
        elif args.format == "dot":
            print(format_mac_output(formatter.dot))
        elif args.format == "dash":
            print(format_mac_output(formatter.dash))
        elif args.format == "ddash":
            print(format_mac_output(formatter.ddash))
        elif args.format == "space":
            print(format_mac_output(formatter.space))
        elif args.format == "blank":
            print(format_mac_output(formatter.blank))
        elif args.format == "binary":
            print(format_mac_output(formatter.binary))
        elif args.format == "compact":
            print(format_mac_output(formatter.compact))
        elif args.format == "eui64":
            print(format_mac_output(formatter.eui64))
        elif args.format == "bpf":
            print(format_mac_output(formatter.bpf))
        elif args.format == "reverse":
            print(format_mac_output(formatter.reverse))
    else:
        print(f'colon: {format_mac_output(formatter.colon)}')
        print(f'dot: {format_mac_output(formatter.dot)}')
        print(f'dash: {format_mac_output(formatter.dash)}')
        print(f'ddash: {format_mac_output(formatter.ddash)}')
        print(f'space: {format_mac_output(formatter.space)}')
        print(f'blank: {format_mac_output(formatter.blank)}')
        print(f'binary: {format_mac_output(formatter.binary)}')
        print(f'compact: {format_mac_output(formatter.compact)}')
        print(f'eui64: {format_mac_output(formatter.eui64)}')
        print(f'bpf: {format_mac_output(formatter.bpf)}')
        print(f'reverse: {format_mac_output(formatter.reverse)}')

if __name__ == "__main__":
    main()

