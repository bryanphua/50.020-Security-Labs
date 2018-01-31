#!/usr/bin/env python3
# SUTD 50.020 Security Lab 1
# Simple file read in/out
# Quyen, 2014

# Import libraries
import sys
import argparse
import string

def doStuff(filein,fileout):
    # open file handles to both files
    fin  = open(filein, mode='r', encoding='utf-8', newline='\n')       # read mode
    fin_b = open(filein, mode='rb')  # binary read mode
    fout = open(fileout, mode='w', encoding='utf-8', newline='\n')      # write mode
    fout_b = open(fileout, mode='wb')  # binary write mode
    c    = fin.read()         # read in file into c as a str
    # and write to fileout

    # close all file streams
    fin.close()
    fin_b.close()
    fout.close()
    fout_b.close()

    # PROTIP: pythonic way
    with open(filein, mode="r", encoding='utf-8', newline='\n') as fin:
        text = fin.read()
        # do stuff

        # file will be closed automatically when interpreter reaches end of the block

def validate_arguments(filein,fileout,key,mode):
    return is_valid_file(filein) and\
            is_valid_file(fileout) and\
            is_valid_key(key) and\
            is_valid_mode(mode)
    
def is_valid_file(filename):
    return True

def is_valid_key(key):
    min_length = 1
    max_length = len(string.printable) - 1 
    if key<min_length or key>max_length:
        print("key length is {}, it must be within {} and {}".format(key,min_length,max_length))
        return False
    return True
    
def is_valid_mode(mode):
    valid_modes = ['d','e']
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
        #doStuff(filein,fileout)
        pass
    

    # all done


