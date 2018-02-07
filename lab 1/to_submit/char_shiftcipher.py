#!/usr/bin/env python3
# SUTD 50.020 Security Lab 1

# Import libraries
import sys
import argparse
import string
        
def validate_arguments(key,mode):
    return is_valid_key(key) and is_valid_mode(mode)
    
def is_valid_key(key):
    min_length = 1
    max_length = len(string.printable) - 1 
    if key<min_length or key>max_length:
        print("key length is {}, it must be within {} and {}".format(key,min_length,max_length))
        return False
    return True
    
def is_valid_mode(mode):
    valid_modes = ['d','D','E','e']
    if mode not in valid_modes:
        print("mode is "+str(mode)+", valid modes are "+str(valid_modes))
        return False
    return True

def shift_file(filein,fileout,key,mode):
    with open(filein, mode="r", encoding='utf-8', newline='\n') as fin:
        text = fin.read()

    shift_hashtable = create_shift_hashtable(key,mode)

    with open(fileout, mode="w", encoding='utf-8', newline='\n') as fout:
        for char in text:
            if char in string.printable:
                shifted_char = shift_hashtable[char]
                fout.write(shifted_char)
            else:
                print("character from {} not in string.printable".format('filein'))

def create_shift_hashtable(key,mode):
    # key is between 1 and len(string.printable)-1
    if mode == 'd' or mode == 'D': # shift backwards
        from_sequence = string.printable[key:] + string.printable[:key]

    else: # shift forward
        from_sequence = string.printable[-key:] + string.printable[:-key]
    
    return {from_sequence[i]:string.printable[i] for i in range(len(string.printable))}


# our main function
# -i [input filename] -o [output filename] -k [key] -m [mode]
if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein',help='input file')
    parser.add_argument('-o', dest='fileout', help='output file')
    parser.add_argument('-k', dest='key', help='key', type=int)
    parser.add_argument('-m', dest='mode', help='mode')

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode
    if validate_arguments(key,mode):
        print("arguments are valid")
        shift_file(filein,fileout,key,mode)
        print("encryption/decryption completed")
