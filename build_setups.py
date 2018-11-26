# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 13:35:42 2018

@author: ylwaller
"""

class colors:  #cyan, purple, red, orange...
    #reset='\033[0m'
    #bold='\033[01m'
    #disable='\033[02m'
    #underline='\033[04m'
    #reverse='\033[07m'
    #strikethrough='\033[09m'
    #invisible='\033[08m'
    #black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    #lightgrey='\033[37m'
    #darkgrey='\033[90m'
    #lightred='\033[91m'
    #lightgreen='\033[92m'
    #yellow='\033[93m'
    #lightblue='\033[94m'
    #pink='\033[95m'
    #lightcyan='\033[96m'
    class bg: 
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'
  
#print(colors.green, "Amartya") 



import random
import numpy as np
from copy import copy

class PieceLimitError(Exception):
    pass


default_map = [[ 1, 1, 1,  1, 1,  1, 1,  1,  1, 1],
       [1, 1, 1, 1, 1, 1, 1,  1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

blued = {} #these are for processing the setups into a state that the main game engine can use.
blued[1] = '1b'
blued[2] = '2b'
blued[3] = '3b'
blued[4] = '4b'
blued[5] = '5b'
blued[6] = '6b'
blued[7] = '7b'
blued[8] = '8b'
blued[9] = '9b'
blued[10] = '10b'
blued[0] = '0b'
blued[11] = '11b'

redd = {}
redd[1] = '1r'
redd[2] = '2r'
redd[3] = '3r'
redd[4] = '4r'
redd[5] = '5r'
redd[6] = '6r'
redd[7] = '7r'
redd[8] = '8r'
redd[9] = '9r'
redd[10] = '10r'
redd[0] = '0r'
redd[11] = '11r'

pc = {}
pc[1] = 1
pc[2] = 7
pc[3] = 5
pc[4] = 2
pc[5] = 2
pc[6] = 2
pc[7] = 1
pc[8] = 1
pc[9] = 1
pc[10] = 1
pc[0] = 1
pc[11] = 6


middle_map = [['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
       ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']]

initial_blue_map = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

remainder_dict = copy(pc)
blue_map = copy(initial_blue_map)
counter569034 = 0

counter569034 = 0

while sum(remainder_dict.values()) > 0:
    counter569034+=1
    if counter569034 == 1:
        print("Lo, the battlefield was wild and waste...")
        print("You are blue. This will be programmatic eventually.")
        print("Array your forces, marshal, in the Martian hinterlands.") #name backgrounds some shit and then change "Martian" to whatever that is
    print(blue_map[0])
    print(blue_map[1])
    print(blue_map[2])
    #insert "would you like to swap some pieces?" logic here
    while True:
        print("Please select a piece. You have this many of each left: ", remainder_dict)
        piece_val = int(input("Integer from 0-11: "))
        try:
            if remainder_dict[piece_val] == 0:
                print("None left. Try again.")
                continue
        except KeyError:
            print("That's not a piece, bucko.")
            continue
        board_row = int(input("Select the board row (1-3): "))
        if board_row not in [1,2,3]:
            print("Bad row. Try again.")
            continue
        board_col = int(input("Select the board col (1-10): "))
        if board_row not in [1,2,3,4,5,6,7,8,9,10]:
            print("Bad column. Try again.")
            continue
        if blue_map[board_row-1][board_col-1] != -1:
            print("Already occupied, d-d-do it agaaaaiiiinnnn.")
            continue
        break
        
    blue_map[board_row-1][board_col-1] = copy(piece_val)
    remainder_dict[piece_val] -= 1
    if ((counter569034+1) % 4) == 0:
        yesno = input("Would you like to assign the rest randomly (y/n)? ")
        if yesno == 'y':
            while sum(remainder_dict.values()) > 0:
                #print("working, pieces left: ",sum(remainder_dict.values()))
                random_piece = random.choice([a for a in remainder_dict if remainder_dict[a] != 0])
                placed = False
                while placed == False:
                    random_row = random.choice([0,1,2])
                    random_col = random.choice([0,1,2,3,4,5,6,7,8,9])
                    #print("trying...",random_row,random_col,blue_map[random_row][random_col])
                    if blue_map[random_row][random_col] == -1:
                       blue_map[random_row][random_col] = random_piece
                       remainder_dict[random_piece] -= 1
                       placed = True
                    else:
                        pass
        print("Random assignment completed. Ending. Goodbye.")

    
initial_red_map = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
    
red_map = copy(initial_red_map)

remainder_dict = copy(pc)


counter569034 = 0

while sum(remainder_dict.values()) > 0:
    counter569034+=1
    if counter569034 == 1:
        print("Lo, the battlefield was wild and waste...")
        print("You are red. This will be programmatic eventually.")
        print("Array your forces, marshal, in the Martian hinterlands.") #name backgrounds some shit and then change "Martian" to whatever that is
    print(red_map[0])
    print(red_map[1])
    print(red_map[2])
    #insert "would you like to swap some pieces?" logic here
    while True:
        print("Please select a piece. You have this many of each left: ", remainder_dict)
        piece_val = int(input("Integer from 0-11: "))
        try:
            if remainder_dict[piece_val] == 0:
                print("None left. Try again.")
                continue
        except KeyError:
            print("That's not a piece, bucko.")
            continue
        board_row = int(input("Select the board row (1-3): "))
        if board_row not in [1,2,3]:
            print("Bad row. Try again.")
            continue
        board_col = int(input("Select the board col (1-10): "))
        if board_row not in [1,2,3,4,5,6,7,8,9,10]:
            print("Bad column. Try again.")
            continue
        if red_map[board_row-1][board_col-1] != -1:
            print("Already occupied, d-d-do it agaaaaiiiinnnn.")
            continue
        break
        
    red_map[board_row-1][board_col-1] = copy(piece_val)
    remainder_dict[piece_val] -= 1
    if ((counter569034+1) % 4) == 0:
        yesno = input("Would you like to assign the rest randomly (y/n)? ")
        if yesno == 'y':
            while sum(remainder_dict.values()) > 0:
                #print("working, pieces left: ",sum(remainder_dict.values()))
                random_piece = random.choice([a for a in remainder_dict if remainder_dict[a] != 0])
                placed = False
                while placed == False:
                    random_row = random.choice([0,1,2])
                    random_col = random.choice([0,1,2,3,4,5,6,7,8,9])
                    #print("trying...",random_row,random_col,red_map[random_row][random_col])
                    if red_map[random_row][random_col] == -1:
                       red_map[random_row][random_col] = random_piece
                       remainder_dict[random_piece] -= 1
                       placed = True
                    else:
                        pass
        print("Random assignment completed. Ending. Goodbye.")
           
x=0
for row in blue_map:
    y=0
    for piece in row:
        blue_map[x][y] = blued[piece]
        y+=1
    x+=1

x=0
for row in red_map:
    y=0
    for piece in row:
        red_map[x][y] = redd[piece]
        y+=1
    x+=1
    

print_board = blue_map+middle_map+red_map
print(print_board)


'''
a = np.asarray(blue_map)
unique, counts = np.unique(a, return_counts=True)
b = dict(zip(unique, counts))

offender_error = 0
for i in range(12):
    if not pc[i] == b[i]:
        print("correct count: ", pc[i])
        print("offender (piece, count): ",i,b[i])
        offender_error+=1

if offender_error != 0:
    raise PieceLimitError

x=0
'''








