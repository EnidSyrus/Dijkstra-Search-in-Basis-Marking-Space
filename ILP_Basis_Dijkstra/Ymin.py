# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:09:53 2020

@author: Syrus
"""
import numpy as np

def initialize_ABF(m,n,C,TE): 
    A = C.copy() 
    for t in TE:
        A[:,t] = np.zeros(m)

    A = np.transpose(A)
    B = np.diag(np.ones(n, dtype=np.int))
    AB = np.block([A,B])

    F = np.zeros((1,n), dtype=np.int)
    return(A,AB,F)
    
def findmin(F):  # Extract all the smallest vectors from F
    n = F.shape[0]
    j = 0  # At the beginning, point j to the first line
    while True: # Loop j
        if j >= n - 1:
            break
        else:
            k = j + 1 # Point k to the next line of j
            while True: # Loop k
                if k >= n:
                    break
                else:
                    if np.all(F[j,:] <= F[k,:]): # If every element in the jth row is smaller than the kth row, delete the kth row
                        F = np.delete(F,k,0)
                        n -= 1
                    elif np.all(F[j,:] >= F[k,:]): # If each element of the jth row is larger than the kth row, assign the kth row to the jth row, then delete the original kth row, and reset k back to the next row of j
                        F[j,:] = F[k,:]
                        F = np.delete(F,k,0)
                        n -= 1
                        k = j + 1
                    else: # If the two rows cannot be compared, keep the kth row, point k to the next row of the row, and continue to compare the current j and k
                        k += 1
            j += 1
    return(F) 
    
def getNeg(DF,m):  # Return the coordinate i, j of a negative element in the matrix DF
    rowSize = DF.shape[0]
    columnSize = m
    for i in range(rowSize):
        for j in range(columnSize):
            if DF[i,j]<0:
                return [i,j]
    return [-1,-1]

#-----For each t, output its minimum vector set Ymin-----#
def compute_Ymin(A,AB,F,m,n,Pre,M,t): 
    D = M - Pre[:,t]
    D = np.reshape(D,(1,m))
    DF = np.block([D,F])
     
    negElement = getNeg(DF,m)  # Get the coordinate i, j of a negative element in the matrix DF
    while negElement != [-1,-1]:
        for rowIndex in range(n):  # Check every line of AB
            if AB[rowIndex,negElement[1]] > 0:  # If the jth column corresponding to the rowIndex row above the negative value is a positive value, add this row to the ith row of DF
                line = AB[rowIndex,:] + DF[negElement[0],:]
                DF = np.vstack((DF, line)) 
        DF = np.delete(DF, negElement[0], 0)  # Delete the ith row of DF 
        
        negElement = getNeg(DF,m)   
    F = DF[:,m:m+n]
    Ymin = findmin(F)
    return(Ymin)