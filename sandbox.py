# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:23:44 2018

@author: ylwaller
"""


no=[(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)]
def manhattan_dist(move): #order doesn't matter
    a = move[0][0]
    b = move[0][1]
    c = move[1][0]
    d = move[1][1]
    mandist = abs(a-c)+abs(b-d)    
    
    if (any (min([a, c]) < box[0] < max([a, c]) and min([b, d]) < box[1] < max([b, d])) for box in no):
        print("uhh")
        #calculate go-around logic
    
    return mandist



manhattan_dist(((0,2),(0,3)))



starting_board = [([[ -1, -1, -1,  11, 0,  11, -1,  -1,  -1, -1],
       [-1, -1, -1, -1, -1, -1, -1,  11, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, 6, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, 20, 31, -1, 25, -1, -1, -1]])]
    
    
moveless = {0,11,30,31,20,21,22,23,24,25,26,27,28,29}

anynotin = {element for row in starting_board[0] for element in row} - moveless
# OR
anynotin = set(np.asarray(starting_board[0]).ravel()) - set(moveless)







