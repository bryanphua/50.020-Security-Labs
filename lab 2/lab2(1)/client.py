#!/usr/bin/python3
# -*- coding: utf-8 -*-
# DA+Nils 2018

"""
Lab2: Breaking Ciphers

Pwntool client for python3

Install: see install.sh

Documentation: https://python3-pwntools.readthedocs.io/en/latest/

Answers here are HARDCODED
"""

from pwn import remote
import string

# pass two bytestrings to this function
def XOR(a, b):
	r = b''
	for x, y in zip(a, b):
		r += (x ^ y).to_bytes(1, 'big')
	return r


def english_frequency_order_list():
	order = ' etaohrndislw\ng,ucmyfp.bk\"v-j\'?q:\txz'
	#order = ' etaoinshrdlcumwfgypbvkjxqz'
	#	'r':'i',	
	#	'd':'s',
	# i,a
	# r,h
	return list(order)

def get_text_frequency(text):
	char_list = list(set(list(text)))
	print('size of ciphertext character set: {}'.format(len(char_list)))
	ascii_dict = {char:0 for char in char_list}
	count=0

	for char in text:
		if ascii_dict[char]==0:
			count+=1
		ascii_dict[char] +=1
	#print("count={}".format(count))
	return ascii_dict

def get_naive_mapping(text):
	text_frequency_order = get_frequency_order(text)
	mapping = {string[0]:string[1] for string in \
		zip(text_frequency_order,english_frequency_order_list())}
	printable_list = list(string.printable)
	for value in mapping.values():
		if value in printable_list:
			printable_list.remove(value)
		else:
			print(value)
			assert False	
	for encrypt_char in text_frequency_order:
		if encrypt_char not in mapping.keys():
			mapping[encrypt_char] = printable_list[0]
			printable_list.remove(printable_list[0])
	return mapping
	
def get_frequency_order(text):
	freq_dict = get_text_frequency(text)
	frequencies = sorted(freq_dict.values(),reverse=True)
	prev_freq = None
	order_list = []
	for freq in frequencies:
		if freq != prev_freq:
			sublist = []
			for k,v in freq_dict.items():
				if v == freq:
					sublist.append(k)
			sublist.sort()
			order_list += sublist
		prev_freq = freq	
	return order_list

def decrypt(text,mapping):
	plaintext = ''
	for char in text:
		if char in mapping.keys():
			plaintext += mapping[char]
		else:
#			print("{} not in mapping".format(char))
			plaintext += char
	return plaintext

def sol1():
	conn = remote(URL, PORT)
	message = conn.recvuntil('-Pad')  # receive TCP stream until end of menu
	conn.sendline("1")  # select challenge 1

	dontcare = conn.recvuntil(':')
	challenge = conn.recvline()
#	print(challenge)
	
	# decrypt the challenge here
	ciphertext = ''.join([chr(byte) for byte in challenge])
	mapping = get_naive_mapping(ciphertext)
	
	plaintext = decrypt(ciphertext,mapping)
	print(plaintext)
	solution = str.encode(plaintext)
	conn.send(solution)
	message = conn.recvline()
	message = conn.recvline()
	if b'Congratulations' in message:
		print(message)
	conn.close()


def sol2():
	expected = b'Student ID: 1001550 and grade 4. [<-- this is not the exact plaintext]\n'


	conn = remote(URL, PORT)
	message = conn.recvuntil('-Pad')  # receive TCP stream until end of menu
	conn.sendline("2")  # select challenge 2

	dontcare = conn.recvuntil(':')
	challenge = conn.recvline()

	mask1 = 0x4 << 8*8
	mask2 = 0x5 << 16*8
	mask3 = 0x5 << 17*8
	mask4 = 0x1 << 18*8
	mask = mask1 + mask2 + mask3 + mask4
	mask = mask.to_bytes(len(challenge), 'big')
	positions = [8,16,17,18]
	for position in positions:
		print("position {} = {}".format(position,challenge[32-position]))
	message = XOR(challenge, mask)
	print("after XOR")
	for position in positions:
		print("position {} = {}".format(position,message[32-position]))
	conn.send(message)
	message = conn.recvline()
	message = conn.recvline()
	if b'exact' in message:
		print(message)
	conn.close()


if __name__ == "__main__":

	# NOTE: UPPERCASE names for constants is a (nice) Python convention
	URL = 'scy-phy.net'
	PORT = 1337

	sol1() 
	sol2()
