#!/usr/bin/env python3
 
from includes import scan

def reader(input,output):
    try:
        with open(input,'r') as file:
            for line in file:
                scan.cvescan(line.strip(), output)
    except FileNotFoundError:
        print("File not found. Check the file path and name.")

    