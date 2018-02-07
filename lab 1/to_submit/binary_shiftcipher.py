#!/usr/bin/env python3

# Import libraries
import sys
import argparse
import string

def binary_shift_file(filein,fileout,key,mode):
    # open file handles to both files
    fin_b = open(filein, mode='rb')  # binary read mode
    fout_b = open(fileout, mode='wb')  # binary write mode
    c_bytes   = fin_b.read()         # read in file into c as a str

    c_byte_array = bytearray(c_bytes)
    if mode == 'd' or mode == 'D':
        key = -key

    mask = 0xFF
    for byte in c_byte_array:
        shifted_byte = (byte + key) & mask
        fout_b.write(shifted_byte.to_bytes(1,'big')) 
        
    # close all file streams
    fin_b.close()
    fout_b.close()

    
def validate_arguments(filein,fileout,key,mode):
    return is_valid_key(key) and\
            is_valid_mode(mode)
    

def is_valid_key(key):
    min_value = 0
    max_value = 255
    if key<min_value or key>max_value:
        print("key value is {}, it must be within {} and {}".format(key,min_value,max_value))
        return False
    return True
    
def is_valid_mode(mode):
    valid_modes = ['d','D','E','e']
    if mode not in valid_modes:
        print("mode is "+str(mode)+", valid modes are "+str(valid_modes))
        return False
    return True

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
    if validate_arguments(filein,fileout,key,mode):
        print("arguments are valid")
        binary_shift_file(filein,fileout,key,mode)    
        print("encryption/decryption completed")

    # all done


