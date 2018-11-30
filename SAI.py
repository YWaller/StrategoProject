# -*- coding: utf-8 -*-
import random
import numpy as np
from copy import copy,deepcopy
import re
import getboards

sys_random = random.SystemRandom()

pd = {} #piececonversions
pd['1b'] = 1
pd['2b'] = 2
pd['3b'] = 3
pd['4b'] = 4
pd['5b'] = 5
pd['6b'] = 6
pd['7b'] = 7
pd['8b'] = 8
pd['9b'] = 9
pd['10b'] = 10
pd['11b'] = 11
pd['0b'] = 0
pd['1'] = -1

pd['1r'] = 21
pd['2r'] = 22
pd['3r'] = 23
pd['4r'] = 24
pd['5r'] = 25
pd['6r'] = 26
pd['7r'] = 27
pd['8r'] = 28
pd['9r'] = 29
pd['10r'] = 30
pd['0r'] = 20
pd['11r'] = 31    

ld = {} 
ld[-1] = -1
ld[21] = 1
ld[22] = 2
ld[23] = 3
ld[24] = 4
ld[25] = 5
ld[26] = 6
ld[27] = 7
ld[28] = 8
ld[29] = 9
ld[30] = 10
ld[20] = 0
ld[31] = 11
ld[-1] = -1
ld[1] = 1
ld[2] = 2
ld[3] = 3
ld[4] = 4
ld[5] = 5
ld[6] = 6
ld[7] = 7
ld[8] = 8
ld[9] = 9
ld[10] = 10
ld[0] = 0
ld[11] = 11

def manhattan_dist(move): #order doesn't matter
    a = move[0][0]
    b = move[0][1]
    c = move[1][0]
    d = move[1][1]
    mandist = abs(a-c)+abs(b-d)  
    print(mandist,"man dist")
    return mandist

#functions copied from main with ai as needed:
               
def casx(x):
    if(x < 150 or x > 650):
        return -1
    else:
        return int((x-150)/50)
        
def casy(y):
    if(y < 50 or y > 550):
        return -1
    else:
        return int((y-50)/50)
    
class TwoWayDict(dict): #I needed a two way dictionary for my number/board position pairs, so...
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2

class AI_Player():
    def __init__(self,color,board):
        self.color = color
        self.totalAllies = {'11':6,'10':1,'9':1,'8':1,'7':1,'6':2,'5':2,'4':2,'3':5,'2':7,'1':1,'0':1}
        self.totalEnemies = {'11':6,'10':1,'9':1,'8':1,'7':1,'6':2,'5':2,'4':2,'3':5,'2':7,'1':1,'0':1}
        self.hiddenornotdict = dict.fromkeys(range(0, 100), 0) #as pieces are positively identified, we'll change their hidden dict value from 0 to 1
        self.hiddenornotdict['-1'] = 0
        self.turncount = 0

    def rank_value_calc(self,totalAllies,totalEnemies):
        #Our pieces
        basevalue=dict()
        rankdifffactor=1.45
        for i in range(12):
            basevalue[str(i)]= 0.0
        basevalue[str(1)] = .05
        for i in range(2,11):
            if (self.totalAllies[str(i-1)]+self.totalAllies[str(i)] > 0)  and (self.totalEnemies[str(i-1)]+self.totalEnemies[str(i)]>0):
                basevalue[str(i)] = basevalue[str(i-1)]*rankdifffactor
            else:
                basevalue[str(i)] = basevalue[str(i-1)]
        
        #gets the highest value of basevalue for scaling
        highest = max(basevalue.values())
        #scale all the values and then add a value
        for i in range(11):
            basevalue[str(i)] = float(basevalue[str(i)])/float(highest)+(.5/sum(basevalue.values()))
        #specific pieces with alternate values
        
        #if there's an enemy spy, reduce the 10's importance
        if self.totalEnemies[str(1)] != 0:
            basevalue[str(10)] = basevalue[str(10)]*.8
            
        #highest = max(basevalue.itervalues(), key=(lambda key: basevalue[key]))  
        highest = max(basevalue.values())
        basevalue[str(1)] = basevalue[str(10)]/2
        basevalue[str(0)] = highest+.5
        basevalue[str(11)] = highest/2
            
        #if there are fewer than 3 miners, make them more valuable
        if self.totalAllies[str(3)] >= 3:
            basevalue[str(3)] = basevalue[str(3)]*((4-self.totalAllies[str(3)])/2)
            
        #if there are fewer than 3 scouts, make them more valuable
        if self.totalAllies[str(2)] >= 3:
            basevalue[str(2)] = basevalue[str(2)]*((4-self.totalAllies[str(2)])/3)
        
        #if enemy unit is hidden and has moved, make its value higher than the 2
        #if its hidden and has moved, make its value 
        
        return basevalue
       
    def read_in_go(self,board_version_moves,turncount,previous_move,board,piecelist):
        #this function houses the main AI logic
        
        def check_unit_ai(move): #given a board position, finds the matching class object and return its identifier
            for piece in piecelist:
                if (move[0],move[1]) == piece.get_pos():
                    return piece.identifier
            for piece in piecelist:
                print(piece.get_pos())
            print(move,"move")
        
        self.allyrankvalues = self.rank_value_calc(self.totalAllies,self.totalEnemies)
        self.enemyrankvalues = self.rank_value_calc(self.totalEnemies,self.totalAllies)
        #this board should be numbered 1-60, with -1s filling in the other spaces. It lets us know where each specific piece is.
        
        
        #make initial board...    
        ai_board = np.asarray(board)
        x=0
        y=0
        for row in ai_board:
            x=0
            for piece in row:
                ai_board[y,x] = pd[re.sub(r'[\W_]+', '', ai_board[y,x])]
                x+=1
            y+=1
        ai_board = ai_board.astype(int)
        
        allmovesforfunc = []
        for option in board_version_moves:
            yps = option[0]-1 #y
            xps = option[1]
            ypt = casy(option[2].rect.centery)-1
            xpt = casx(option[2].rect.centerx)    
            move = ((ypt,xpt),(yps,xps)) #MOVE[0] IS SOURCE
            allmovesforfunc.append(move)
            
        #print(self.hiddenornotdict)
        deletion_indices = []
        deletioncounter = 0
        for move in allmovesforfunc: #all of this code is to get the AI to not attack pieces it has learned are larger than whatever the piece its focused on is
            if self.hiddenornotdict[check_unit_ai((move[0][1],move[0][0]+1))] == 1: #check if the unit is hidden or not                #tuple(reversed(move[0]))
                if ld[ai_board[move[1]]] > ld[ai_board[move[0]]]: #if the unit at this position is bigger than this piece, remove the move from consideration
                    #so to make this a "memory" index, pick a random number between 1 and 10; if it's lower than whatever, don't assign the move, and make that piece hidden again
                    deletion_indices.append(copy(deletioncounter))
                    print("NOT THAT DUMB")
            deletioncounter+=1
        
        if len(deletion_indices) < len(allmovesforfunc): #prevents us from removing all our valid moves, but it's a bad place to be in if they're all attacking pieces bigger than us...
            for index in reversed(deletion_indices):
                print("move deleted: ",allmovesforfunc[index])
                del allmovesforfunc[index]                    
        
        #for the objective function, sum the number of allied pieces that are hidden and subtract the number of enemy pieces that are
        ai_board = np.asarray(ai_board)
        #[((1,0),(0,0)),((0,1),(0,0))]
        self.turncount+=2
        #if turncount is low, we don't really need to spend too much time on our move. Let's speed things up a bit...
        recursion_send = 7
        if self.turncount < 50:
            recursion_send = 6
        elif self.turncount < 30:
            recursion_send = 5
        elif self.turncount < 10:
            recursion_send = 4
        
        movestrengths = getboards.move_strength_ultimate([ai_board],allmovesforfunc,recursion_send) #current board, move list, recursion_depth; I don't recommend values above 10
        justnumbers = []
        for move in movestrengths:
            #print(move)
            justnumbers.append(copy(move))
        
        print(justnumbers)
        random.shuffle(justnumbers) #so if a couple have the same value, we'll get a random one of the best, since max takes the first occurrence of that value
        move = board_version_moves[justnumbers.index(max(justnumbers))]
        print("move selection complete.")
        return move
    
        
    
    
    