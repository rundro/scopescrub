#!/usr/bin/env python3
###
### Author: Rundro
###

import os
import sys
import re
import netaddr
from netaddr import *

print ("")

if len(sys.argv) == 1 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print ("Usage: python3 scopescrub.py <input list>\n")
    print ("The goal of scopescrub is to take a rough list of domains, IP addresses, and CIDR")
    print ("ranges in as many formats as possible, and output a clean, formatted, text file to")
    print ("be used as an input to other scripts and tools. IPv6 will be removed and added to ")
    print ("a seperate file.\n")
    print ("A few example formats:\n")
    print ("    8.8.8.8")
    print ("    8.8.8.8/24")
    print ("    8.8.8.8-255")
    print ("    8.8.8.8 - 255")
    print ("    8.8.8.8-8.8.8.255")
    print ("    8.8.8.8 - 8.8.8.255")
    print ("    8.8.8.8, 8.8.8.9/32, 8.8.8.10")
    print ("    google.com")
    print ("    https://google.com\n")
    exit()

# Read the file, format, remove whitespace, remove ipv6
with open(sys.argv[1]) as infile, open('tmp', 'w') as outfile:
    for line in infile:
        if not line.strip(): continue  # skip the empty line
        line = line.replace(' ', '')
        line = line.replace(',','\n')
        line = line.lower()
        line = line.replace('http://','')
        line = line.replace('https://','')
        # If line is an IPv6 address or CIDR, remove and add to a seperate file
        if line.count(":") >= 2:
            print ("[*] Removing IPv6 address: "+line, end='')
            print (line, file=open("tmpv6", "a"))
        else:
            outfile.write(str(line))

# Convert weird IP range formats to CIDR
with open("tmp") as infile, open('tmp1', 'w') as outfile:
    for line in infile:
        #print ("Line: "+line)

        # If the line is strictly numbers and special chars (identifies IP ranges)
        # but also not a single IP address
        if not any(c.isalpha() for c in line):
            if "-" in line:
                startip,endip = line.split('-')
                startip = startip.strip('\n')
                endip = endip.strip('\n')

                # If the IP range is in the format 10.0.0.1-10, create end IP from start IP
                # otherwise, treat format as 10.0.0.1-10.0.0.10
                if len(endip) < 4:
                    base = (startip.rsplit('.', 1)[0])
                    final = ("{}.{}".format(base, endip))
                    final = str(final)
                    final = final.strip()
                    #print ("Start: "+startip)
                    #print ("Final: "+final)
                    cidrs = netaddr.iprange_to_cidrs(startip, final)
                elif len(endip) > 3:
                    cidrs = netaddr.iprange_to_cidrs(startip, endip)
                for i in cidrs:
                    #print (i)
                    outfile.write(str(i)+"\n")
            else:
                outfile.write(line)
        else:
            outfile.write(line)


# Remove duplicate lines from tmp1 and create the small.txt output
lines_seen = set() # holds lines already seen
with open("small.txt", "w") as output_file:
	for each_line in open("tmp1", "r"):
	    if each_line not in lines_seen: # check if line is not duplicate
	        output_file.write(each_line)
	        lines_seen.add(each_line)


# Expand CIDRs
with open('small.txt') as infile, open('tmp2', 'w') as outfile:
    for line in infile:
        cidr ="n"
        try:
            for ip in IPNetwork(str(line)):
                ip = str(ip)+"\n"
                outfile.write(ip)
            cidr = "y"
        except:
            pass
        if cidr == "n":
            outfile.write(str(line))
        else:
            cidr = "n"


# Remove duplicate lines from tmp2 and create the large.txt output
lines_seen = set() # holds lines already seen
with open("large.txt", "w") as output_file:
	for each_line in open("tmp2", "r"):
	    if each_line not in lines_seen: # check if line is not duplicate
	        output_file.write(each_line)
	        lines_seen.add(each_line)


# Remove whitespace from IPv6 file
try:
    with open("tmpv6") as infile, open('IPv6.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)
except:
    pass


# Cleanup
os.remove("tmp")
os.remove("tmp1")
os.remove("tmp2")
try:
    os.remove("tmpv6")
except:
    pass


# Print output files
print ("\nOutput: ")
print ("       ./small.txt  -  condensed and formatted scope")
print ("       ./large.txt  -  expanded cidrs and formatted")
print ("       ./IPv6.txt   -  IPV6 addresses and cidrs removed")

