#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.020 Security
# Oka, SUTD, 2014
import argparse
from present import present_inv
def getInfo(headerfile):
    with open(headerfile, 'rb') as f:
        info_bytes = f.read()
    return info_bytes

def bytes_to_integer(byte_array):
    i = 0
    out = 0
    for byte in byte_array[::-1]:
       out += byte << 8*(len(byte_array)-i-1)
       i+=1
    return out

def integer_to_bytes(integer,num_bytes):
    out = []
    for i in range(num_bytes):
        byte = (integer >> (num_bytes*8*i)) & 0xFF
        out.append(byte)

    out.reverse()
    out = bytes(out)
    return out

def extract(infile,outfile,headerfile):
    blocksize = 8  # bytes
    frequency_dict = {}
    key = 0x0000000000000000000
    with open(infile, 'rb') as f_in:
        block = f_in.read(blocksize)
        out = []
#       while block:
#            block = bytes_to_integer(block)
#            transformed_block = present_inv(block, key)
#            out += integer_to_bytes(transformed_block,blocksize)
#            block = f_in.read(blocksize)
#    for byte in out:1
        while block:
            if block in frequency_dict.keys():
                frequency_dict[block] += 1
            else:
                frequency_dict[block] = 1
            out.append(block)
            block = f_in.read(blocksize)
    out.reverse() 
    print("number of keys={}".format(len(frequency_dict.keys())))
    print(frequency_dict.values())
   
    maxx_key = None
    maxx_freq = None
    for k,v in frequency_dict.items():
        if maxx_key is None:
            maxx_key = k
            maxx_freq = v
        if v > maxx_freq:
            maxx_key = k
            maxx_freq = v

    f_out = open(outfile, 'w')
    info = open(headerfile, 'r').read()
    f_out.write(info)
    f_out.write('\n')
    for block in out:
        if block == maxx_key:
            f_out.write('00000000')
        else:
            f_out.write('11111111')
    f_out.close()
    f_in.close()
    headerfile.close()


if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)

    success=extract(infile,outfile,headerfile)

            
