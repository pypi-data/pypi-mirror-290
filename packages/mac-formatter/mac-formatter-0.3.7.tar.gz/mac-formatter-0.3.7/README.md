mac-formatter
======
A simple library to convert MAC-addresses to different formats.
<br />
<hr>

## How to use in terminal(cli).

### positional arguments:

  mac_address: The MAC address to format

options:

  -h, --help: show this help message and exit
<br>
  -f, --format: {colon,dot,dash,doubledash,space,blank}, The format to use. If not specified, all formats will be printed.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;"The format to use. If not specified, all formats will be printed.<br><br>
    &nbsp;&nbsp;&nbsp;&nbsp;Available formats: <br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**colon**       : Colon-separated format, e.g., ab:12:cd:34:ef:56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**dot**         : Dot notation, e.g., abcd.ef12.3456.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**dash**        : Hyphen-separated format, e.g., ab-12-cd-34-ef-56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**ddash**  : Double-dash-separated format, e.g., ab12-cd34-ef56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**space**       : Space-separated format, e.g., ab 12 cd 34 ef 56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**blank**       : Continuous string with no delimiters, e.g., ab12cd34ef56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**binary**      : Binary format, e.g., 10101011 00010010 11001101 00110100 11101111 01010110.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**encoded**     : Base64 encoded format, e.g., qXLNTq9W.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**eui64**       : Cisco EUI-64 format, e.g., ab12.cd34.fffe.ef56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**bpf**         : BPF format with each byte prefixed by '\\x', e.g., \\xab\\x12\\xcd\\x34\\xef\\x56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**mixed**       : Mixed separator format, e.g., AB:12-CD-34.EF:56.<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**reverse**     : Reverse byte order, e.g., 56ef34cd12ab.<br>
      <br>
  -u, --uppercase: Prints the MAC address in uppercase.
  <br>
  -l, --lowercase: Prints the MAC address in lowercase.


Example usage:
`````bash
mac-formatter abcdef123456 -f dot
`````
output:
`````bash
abcd.ef12.3456
`````
There is also a shorter name `macf`:
`````bash
macf abcd.ef12.3456 -f colon -u
`````
output:
`````bash
AB:CD:EF:12:34:56
`````


## How to use in your code.

`````pycon
from mac_formatter import MacFormatter

mac_address = 'ab:cd:ef:12:34:56'
mac = MacFormatter(mac_address)

print(mac.dot)
print(mac.dash)
print(mac.ddash)
print(mac.space)
print(mac.colon)
print(mac.blank)
print(mac.binary)
print(mac.compact)
print(mac.eui64)
print(mac.bpf)
print(mac.reverse) 
`````
output:
`````bash
abcd.ef12.3456
ab-cd-ef-12-34-56
abcd-ef12-3456
ab cd ef 12 34 56
ab:cd:ef:12:34:56
abcdef123456
10101011 11001101 11101111 00010010 00110100 01010110
q83vEjRW
\xab\xcd\xef\x12\x34\x56
654321fedcba
`````
<hr>

<hr style="border-top: 3px solid rgba(255, 255, 255, 0.2);">
---

*thamuppet* <br>


