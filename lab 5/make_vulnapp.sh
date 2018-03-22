#!/bin/bash
gcc -fno-stack-protector -z execstack -ggdb -o vulnapp vulnapp.c
gcc -fno-stack-protector -ggdb -o vulnappROP vulnapp.c
