# -*- coding: utf-8 -*-
"""
Created on Sun May 24 19:32:57 2020

@author: Syrus
"""

import numpy as np
import time
from readin import readin_Post
from readin import readin_Pre
from readin import readin_Mwkzbc
from readin import readin_TE
from Ymin import initialize_ABF
from Ymin import compute_Ymin
from search_route import search_route
from ILP import opt

# Read in 
Post = readin_Post()
Pre = readin_Pre()
[M0,w,k,z,b,c] = readin_Mwkzbc() 
TE = readin_TE()

C = Post - Pre
[m,n] = Post.shape

# Start the timer
start_time = time.clock()
    
# Add t that satisfies the condition to set TE
TE = set(TE)
for t in range(n):
    if np.dot(z,C[:,t]) > 0:
        TE.add(t)
TE = list(TE)

# Initialize matrix A,AB,F (Preparing for the solution of Ymin)
[A,AB,F] = initialize_ABF(m,n,C,TE)

# Initialize storage list pi and cmin
[y_star,r0,exctime] = opt(w,C,k,M0,TE,n,c)
runILP = 1 
ILPtime = exctime 
q0 = 0
M_list = [M0]
q_list = [q0]
pi = [[list(M0),q0,r0,[],[],[]]]
cmin = r0

while len(M_list) != 0:
    ind = q_list.index(min(q_list))
    M = M_list.pop(ind)
    q = q_list.pop(ind)
    for t in TE:  
        Ymin = compute_Ymin(A,AB,F,m,n,Pre,M,t)
        for y in Ymin:
            if z @ (M + C @ y) <= b:
                continue
            M_ = M + np.dot(C,y) + C[:,t]
            q_ = q + np.dot(c,y) + c[t]
            if q_ >= cmin:
                continue 
            find_flag = 0
            listM_ = list(M_)
            for row in pi:
                if row[0] == listM_:  
                    find_flag = 1
                    if q_ < row[1]:  # Find a lower cost path from the source identifier M0 to the Mb that has been reached before 
                        row[1] = q_
                        row[3] = M
                        row[4] = t
                        row[5] = y
                        if cmin > q_ + row[2]:   
                            cmin = q_ + row[2] 
                            vmin = row
                    break  
                    
            if find_flag == 1:
                continue
            else:   # Find a new path from the source identifier M0 to the Mb that has not been reached before
                [y_star,r_,exctime] = opt(w,C,k,M_,TE,n,c)
                runILP += 1
                ILPtime += exctime 
                pi.append([list(M_),q_,r_,list(M),t,list(y)])
                M_list.append(M_)
                q_list.append(q_)
                if cmin > q_ + r_:   
                    cmin = q_ + r_
                    vmin = [list(M_),q_,r_,list(M),t,list(y)]

# solve y_n+1
M = np.array(vmin[0])  
[y_star,r,exctime] = opt(w,C,k,M,TE,n,c) 
runILP += 1
ILPtime += exctime
y_star = list(y_star)

    
# Output results to file 'output.txt'
f = open('output.txt', 'w',encoding="utf-8")
f.write('# output of the Benchmark:\n')
f.close()

if cmin >= 1073741823:
    elapsed = time.clock() - start_time
    f = open('output.txt', 'a',encoding="utf-8")
    f.write('\n')
    f.write('M0: '+ str(M0) + '\n')
    f.write('TE : ')
    for t in TE:
        f.write('t%d ' % (t+1))
    f.write('\n')
    f.write('runILP: %d times' % (runILP) + '\n')
    f.write('ILP mean excution time: %f s' % (ILPtime/runILP) + '\n')
    f.write('Total Execution Time: %f s' % (elapsed) + '\n')
    f.write('无解' + '\n')
    f.close()
    
else:
    [v0_vmin,sigma] = search_route(pi,vmin,y_star)  # Backtracking the path
    elapsed = (time.clock() - start_time)
    size = len(pi) 
    f = open('output.txt', 'a',encoding="utf-8")
    f.write('\n')
    f.write('TE : ')
    for t in TE:
        f.write('t%d ' % (t+1))
    f.write('\n')
    f.write('runILP: %d times' % (runILP) + '\n')
    f.write('ILP mean excution time: %f s' % (ILPtime/runILP) + '\n')
    f.write('Total Execution Time: %f s' % (elapsed) + '\n')
    f.write('graph size: %d' % (size) + '\n')
    f.write('cmin: '+ str(cmin) + '\n')
    f.write('sigma_min: '+ str(sigma) + '\n')
    f.write('routes: '+ v0_vmin + '\n')
    f.close()
        

    
                       