# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:18:01 2020

@author: Syrus
"""

def search_route(pi,vmin,y_star): # Backtracking the path
    M_list = []
    sigma = 0  # Sequence length count
    for i in pi:
        M_list.append(i[0])

    v0_vmin = []
    v0_vmin.append(str(vmin[5]) + ' --> t' + str(vmin[4] + 1))
    sigma = sigma + sum(vmin[5]) + 1 
    ind = M_list.index(vmin[3])

    while pi[ind][3] != []:
        v0_vmin.append(str(pi[ind][5]) + ' --> t' + str(pi[ind][4] + 1))
        sigma = sigma + sum(pi[ind][5]) + 1
        ind = M_list.index(pi[ind][3])

    v0_vmin.reverse()
    v0_vmin = ' --> '.join(v0_vmin)
    v0_vmin = v0_vmin + ' --> ' + str(y_star)
    sigma = sigma + sum(y_star) 
    
    return(v0_vmin,sigma)

