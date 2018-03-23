#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.020 Security
# Oka, SUTD, 2014
from present import present, present_inv 
import argparse

nokeybits=80
blocksize=64


def ecb(infile, outfile, key, mode):
    if mode == 'e':
        print("encrypting..")
        transform = present
    elif mode == 'd':
        print("decrypting..")
        transform = present_inv
    else:
        raise TypeError('mode should be "d" or "e"')
    s = 0 
    byte_number = 0
    done = False
    with open(infile, 'rb') as f_in:
        with open(outfile, 'wb') as f_out:
            while not done:
                byte = f_in.read(1)
                if byte:
                    s += byte[0] << (8 * (int(blocksize/8) - 1 - byte_number))
                    byte_number += 1 
                else:
                    s = s << (int(blocksize/8)-byte_number)*8
                    byte_number == 8    
                    done = True

                if byte_number % (blocksize/8) == 0:
                    assert s < 2**64
                    transformed_data = transform(s, key)
                    
                    out = [] 
                    for i in range(0, 8):
                        out.append(transformed_data>>(i*8)&0xff)
                    out.reverse()

                    f_out.write(bytes(out))
                    s = 0
                    byte_number=0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile', help='input file')
    parser.add_argument('-o', dest='outfile', help='output file')
    parser.add_argument('-k', dest='keyfile', help='key file')
    parser.add_argument('-m', dest='mode', help='mode')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode

 #   key = open(keyfile, 'r').read()
    key = 0xFFFFFFFFFFFFFFFFFFFF
    ecb(infile, outfile, key, mode)
