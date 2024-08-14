import re
import base64

class MacFormatter:
    def __init__(self, mac_address):
        self.mac = ''.join(re.findall(r'[0-9a-fA-F]', mac_address))
        if not re.match(r'^[0-9a-fA-F]{12}$', self.mac):
            raise ValueError("Invalid MAC address format. Insert 12 hexadecimal characters/digits in any format.")


    def format_mac(self, delimiter, segment_length, length_mod=0, step_size=None):
        """
            Returns a formatted MAC address with specified delimiter and segment length.
            
            Args:
                delimiter (str): Delimiter between segments.
                segment_length (int): Characters in each segment.
                length_mod (int): Ensures the MAC address doesn't end with a separator. This doesn't change the actual MAC address length. Default is 0.
                step_size (int): Step size for iteration, defaults to segment_length.
        
            Returns:
                str: Formatted MAC address.
        """

        if step_size is None:
            step_size = segment_length


        try:
            return delimiter.join(
                [self.mac[i:i + segment_length] for i in range(0, len(self.mac) - length_mod, step_size)])
        except Exception as e:
            raise ValueError("Error while formatting MAC address:", e)

    @property
    def dot(self):
        """Returns MAC address in dot notation, with segments of 4 characters separated by dots (e.g., abcd.ef12.3456)."""
        return self.format_mac('.', 4, 3)

    @property
    def colon(self):
        """Returns MAC address in colon-separated format, with segments of 2 characters (e.g., ab:12:cd:34:ef:56)."""
        return self.format_mac(':', 2)

    @property
    def dash(self):
        """Returns MAC address in hyphen-separated format, with segments of 2 characters (e.g., ab-12-cd-34-ef-56)."""
        return self.format_mac('-', 2)
    
    @property
    def ddash(self):
        """Returns MAC address in double-dash-separated format, with segments of 4 characters (e.g., ab12-cd34-ef56)."""
        return self.format_mac('-', 4, 0)

    @property
    def space(self):
        """Returns MAC address in space-separated format, with segments of 2 characters (e.g., ab 12 cd 34 ef 56)."""
        return self.format_mac(' ', 2)

    @property
    def blank(self):
        """Returns MAC address as a continuous string with no delimiters (Windows Registry e.g., ab12cd34ef56)."""
        return self.mac

    @property
    def binary(self):
        """Returns MAC address in binary format, with 8-bit binary segments (e.g., 10101011 00010010 11001101 00110100 11101111 01010110)."""
        return ' '.join(format(int(c, 16), '08b') for c in re.findall(r'.{2}', self.mac))

    @property
    def compact(self):
        """Returns MAC address encoded in Base64 format (e.g., qXLNTq9W)."""
        mac_bytes = bytes.fromhex(self.mac)
        return base64.b64encode(mac_bytes).decode('utf-8')

    @property
    def eui64(self):
        """Returns MAC address in Cisco EUI-64 format, with 'fffe' inserted in the middle (e.g., ab12.cd34.fffe.ef56)."""
        return self.format_mac('.', 4, 0)

    @property
    def bpf(self):
        r"""Returns MAC address in BPF (Berkeley Packet Filter) format, with each byte prefixed by '\x' (e.g., \xab\x12\xcd\x34\xef\x56)."""
        return '\\x' + '\\x'.join(self.mac[i:i + 2] for i in range(0, len(self.mac), 2))

    @property
    def reverse(self):
        """Returns MAC address in reverse byte order (e.g., 56ef34cd12ab)."""
        return self.mac[::-1]


