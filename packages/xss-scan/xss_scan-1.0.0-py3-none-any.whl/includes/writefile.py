#!/usr/bin/env python3

 
def writedata(output,data):
    with open(output,'a') as file:
        file.write(data)