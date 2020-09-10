# -*- coding: utf-8 -*-
"""
Created on Sun May 24 10:40:00 2020

@author: Syrus
"""
import numpy as np
from gurobipy import Model
from gurobipy import GRB
import time

def generate_A_b(w,C,k,M,TE,n):
    wC = w @ C
    k_wM = k - w @ M
    negative_M = -M
    A0 = np.diag(np.ones(n,dtype= int))
    b0 = np.zeros(n,dtype= int)
    A1 = A0[TE]
    b1 = np.zeros(len(TE),dtype= int)
    return(wC,k_wM,negative_M,A0,b0,A1,b1)
    
def opt(w,C,k,M,TE,n,c):

    [wC,k_wM,negative_M,A0,b0,A1,b1] = generate_A_b(w,C,k,M,TE,n)
    y_star = (-1)* np.ones(n,dtype= int)

    timer = time.clock()
    # Create a new model
    model = Model("ILP-A")
    
    # Create variables
    y = model.addMVar(shape = n, vtype = GRB.INTEGER, name = "y") 

    # Set objective
    model.setObjective(c @ y, GRB.MINIMIZE)
        
    # Add constraint
    model.addConstr(C @ y >= negative_M, name ="c0")
    model.addConstr(wC @ y <= k_wM, name ="c1")  
    model.addConstr(A0 @ y >= b0, name ="c2")
    model.addConstr(A1 @ y <= b1, name ="c3")
    
    model.optimize()
    
    if model.status == GRB.Status.INFEASIBLE:
        f_star = 1073741823
 
    else:
        for i,v in zip(range(n),model.getVars()):
            #print(v.varName, v.x)
            y_star[i] = v.x
            
        f_star = model.objVal
    timer =  time.clock() - timer # Solve time
    
    return(y_star,f_star,timer)
