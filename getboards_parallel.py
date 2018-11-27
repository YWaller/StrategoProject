# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:16:26 2018

@author: ylwaller
"""

#TODO: Haven't run it yet, but top_recursion_func doesn't expecta tuple, so build out a new one here that does bc it will fail
#TODO: Make double triple sure that order is preserved by the parallel processing; and if not/even if it is, the list we get back won't have the scores in order, so we probably need to get 
#the new t_r_f to also RETURN a tuple, including the move it was testing this on so we know

'''
from multiprocessing import Pool
from copy import copy

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(2) as p:
        print(p.map(f, [1, 2, 3]))
'''


from getboards import top_recursion_func, node_strength, error_check_boards, flip_boards, get_scores, worth_considering, do_move, get_all_boards, check_terminal, create_board, create_boardnot2

starting_array = [([[ 6, -1, -1,  11, 0,  11, -1,  -1,  -1, -1],
       [-1, -1, -1, -1, -1, -1, -1,  11, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, 1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, 20, 31, -1, 25, -1, -1, -1]])]
option_list=[((0,0), (1,0)), ((0,0), (2,0)), ((0, 0), (3, 0)), ((0, 0), (4, 0)), ((0, 0), (5, 0)), ((0, 0), (6, 0)), ((0, 0), (0, 1)), ((0, 0), (0, 2)), ((0, 4), (1, 4)), ((0, 5), (1, 5)), ((0, 6), (1, 6)), ((0, 6), (2, 6)), ((0, 8), (1, 8)), ((0, 8), (0, 9)), ((1, 7), (2, 7)), ((1, 7), (1, 6)), ((1, 7), (1, 8))]
strengthlist = move_strength_ultimate(starting_array,option_list,3)
print(strengthlist)

def obergruppen_recurse(strengthlist,move_list,move_value_cutoff,playernumber,recursion_depth,starting_board, consider_depth): #This function is used in m_s_u. It handles recursion and move ordering.
    optioncount = 0    
    poolList = []
    for move in move_list:
        if strengthlist[move_list.index(move)] <= move_value_cutoff:
            pass
        else:
            moveboard = do_move(copy(starting_board[0]),option)
            poolList.append((copy(moveboard),playernumber,round(recursion_depth/2),round(recursion_depth/2)))
            
    if __name__ == '__main__':
        with Pool(4) as p:
            strengthlist = p.map(top_recursion_func, [poolList])
        
    return strengthlist


def move_strength_ultimate(starting_board,move_list,recursion_depth): #This is the main function. You'll notice it hooks into SAI. It decides what moves to look at.
    optioncount = 0
    playernumber = 0
    strengthlist = [[]]*len(move_list)
    print("number of moves: ", len(move_list))
    for option in move_list:
        moveboard = do_move(copy(starting_board[0]),option)
        #strengthlist[optioncount] = 0
        strengthlist[optioncount] = top_recursion_func(moveboard,playernumber,1,1)
        print("considering initial depth: ",strengthlist[optioncount])
        optioncount+=1
    
    justnumbers = [] #this is just for getting what the cutoff number should be, strengthlist will be in the original order still
    for score in strengthlist:
        justnumbers.append(copy(score))
    justnumbers.sort(reverse=True)
    move_value_cutoff = justnumbers[int(len(justnumbers)/2)] #cuts it in half
    print(justnumbers,"allnums")
    
    while all(score <= move_value_cutoff for score in justnumbers):
        move_value_cutoff -= .1
    
    strengthlist = obergruppen_recurse(strengthlist,move_list,move_value_cutoff,playernumber,recursion_depth,starting_board,"half")
  
    justnumbers = []
    for score in strengthlist:
        justnumbers.append(copy(score))
    justnumbers.sort(reverse=True)
    move_value_cutoff = justnumbers[2] #only consider top 3 moves
    print(justnumbers,"allnums")

    while all(score <= move_value_cutoff for score in justnumbers):
        move_value_cutoff -= .1
        
    strengthlist = obergruppen_recurse(strengthlist,move_list,move_value_cutoff,playernumber,recursion_depth*2,starting_board,"full")      #*2 so it actually does the whole recursion depth     
    
    #print(strengthlist)        
    return strengthlist