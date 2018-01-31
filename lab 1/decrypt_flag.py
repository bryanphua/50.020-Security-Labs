#!/usr/bin/env python3
# SUTD 50.020 Security Lab 1

# Import libraries
import sys
import argparse
import string

def decrypt(filein,fileout):
    # open file handles to both files
    fin_b = open(filein, mode='rb')  # binary read mode
    fout_b = open(fileout, mode='wb')  # binary write mode
    c_bytes   = fin_b.read()         # read in file into c as a str
    b_array = bytearray(c_bytes)
   
    key = get_key(b_array)
    if key is None:
        print("cannot find key")
        return

    mask = 0xFF
    for byte in b_array:
        shifted_byte = (byte + key) & mask
        fout_b.write(shifted_byte.to_bytes(1,'big')) 
        
    # close all file streams
    fin_b.close()
    fout_b.close()

def get_key(b_array):
    for i in range(0,256):
        first_eight_bytes = shift_byte_array(b_array[:8],i)
        if is_png(first_eight_bytes):
            print('found the key! key= +{}'.format(i))
            return i
    return None

def shift_byte_array(b_array,key):
    shifted_b_array = bytearray(len(b_array)) 
    mask = 0xFF
    for i in range(len(b_array)):
        shifted_b_array[i] = (b_array[i]+key) & mask 
    return shifted_b_array


def is_png(first_eight_bytes):
    png_signature = bytearray([0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A])
    if first_eight_bytes == png_signature:
        return True
    else:
        return False

# our main function
# -i [input filename] -o [output filename] -k [key] -m [mode]
if __name__=="__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein',help='input file')
    parser.add_argument('-o', dest='fileout', help='output file')

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    decrypt(filein,fileout)
    print("encryption/decryption completed")
    

