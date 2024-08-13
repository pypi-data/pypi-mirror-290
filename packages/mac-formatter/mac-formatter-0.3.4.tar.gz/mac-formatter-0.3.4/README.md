mac-formatter
======
A simple library to convert MAC-addresses to different formats.
<br />
<hr>

### How to use in terminal(cli).

# Run the following to see how mac_formatter is used directly in your terminal

`````bash
mac-formatter --help
`````
Example usage:
`````bash
mac-formatter 01ab02cd03ef -f dot
`````
output:
`````bash
01ab.02cd.03ef
`````

### How to use in your code.

`````pycon
from mac_formatter import MacFormatter

mac_address = '01:ab:02:cd:03:ef'
mac = MacFormatter(mac_address)

print(mac.dot)
print(mac.line)
print(mac.space)
print(mac.colon)
print(mac.blank)
`````
output:
`````bash
01ab.02cd.03ef
01-ab-02-cd-03-ef
01 ab 02 cd 03 ef
01:ab:02:cd:03:ef
01ab02cd03ef
`````
<hr>

<hr style="border-top: 3px solid rgba(255, 255, 255, 0.2);">
---

*thamuppet* <br>


