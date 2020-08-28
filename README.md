# scopescrub
Cleans input lists of ip addresses, ranges, cidr's, domains, etc, in as many formats as possible for input or use in other tools and scripts. Outputs a cleaned list in "small" format, using cidr notation, and a cleaned list in "large" format, where cidr's and ranges are expanded to one host per line. Handles whitespace, commas, dashes, slashes, http prefixes, and multiple other common ip range notations.

A few example formats you can input:

8.8.8.8
8.8.8.8/24
8.8.8.8-255
8.8.8.8 - 255
8.8.8.8-8.8.8.255
8.8.8.8 - 8.8.8.255
8.8.8.8, 8.8.8.9/32, 8.8.8.10
google.com
https://google.com
