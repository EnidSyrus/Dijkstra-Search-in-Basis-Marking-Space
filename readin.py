# -*- coding: utf-8 -*-
"""
Created on Sun May 24 10:35:35 2020

@author: Syrus
"""
import numpy as np
import re

def str_to_array(line): # Single-line string convert to row matrix
    line = line.strip('[]\n').split(',')  
    line = map(int, line) 
    line = list(line)
    line = np.array(line) 
    return(line)

def readin_Post(): 
    file = open("Post.txt","r",encoding="utf-8")   
    lines = file.readlines()  
    Post = []
    for line in lines:
        line = str_to_array(line)    
        Post.append(line)
    Post = np.array(Post)
    return(Post)

def readin_Pre(): 
    file = open("Pre.txt","r",encoding="utf-8")   
    lines = file.readlines()  
    Pre = []
    for line in lines:
        line = str_to_array(line)    
        Pre.append(line)
    Pre = np.array(Pre)
    return(Pre)

def readin_Mwkzbc(): # Read in Ms、w、k、z、b、c
    file = open("inputs.txt","r",encoding="utf-8")   
    next(file) # Skip the first line
    lines = file.readlines()  
    
    Ms = str_to_array(lines[0])
    w = str_to_array(lines[1])
    k = int(lines[2].strip())
    z = str_to_array(lines[3])
    b = int(lines[4].strip())
    c = str_to_array(lines[5])
    return(Ms,w,k,z,b,c)

def readin_TE(): # Read in TE
    TE = []
    file = open("TE.txt","r",encoding="utf-8")  
    line = file.read() 
    line = line.strip().split(',')
    for t in line:
        index = re.findall(r"\d+",t)  # Find the number after each t (that is, the corresponding transition label)
        TE.append(int(index[0])-1)
    return(TE)