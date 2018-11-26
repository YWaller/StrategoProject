# -*- coding: utf-8 -*-
import random
import numpy as np
#import keras
#from keras.models import load_model
from copy import copy
import re
import getboards


sys_random = random.SystemRandom()
#model = load_model('neuralstrategoALL.h5')


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
        self.board = board
        self.totalAllies = {'11':6,'10':1,'9':1,'8':1,'7':1,'6':2,'5':2,'4':2,'3':5,'2':7,'1':1,'0':1}
        self.totalEnemies = {'11':6,'10':1,'9':1,'8':1,'7':1,'6':2,'5':2,'4':2,'3':5,'2':7,'1':1,'0':1}
        self.myboardsred=[]
        self.myboardsblue=[]
        self.pieceident=TwoWayDict()
        if self.color == 'red':
            self.othercolor = 'blue'
        elif self.color == 'blue':
            self.othercolor = 'red'
        self.scoreline = 0
        self.allyrankvalues = dict()
        self.enemyrankvalues = dict()
        self.alliedhidden = dict()
        self.enemyhidden = dict()
        self.allboards = []
            
    def initializepiecelist(self,piecelist,board): #construct initial two way dict
        #put first board into board list
        self.truepiecelist = dict() #need a way to get actual piece from hash
        self.uniquecount = 0
        self.piecelist = piecelist
        self.enemyhidden = dict()
        for piece in piecelist:
            self.truepiecelist[hash(piece)] = piece
            self.uniquecount -= 1
                        #Give each enemy unit a unique negative number identifier  
            self.pieceident[self.uniquecount] = hash(piece)
            #set the lists of allies and enemies to hidden first
            self.alliedhidden[self.uniquecount] = 'h'
            if piece.team != self.color:
                self.enemyhidden[self.uniquecount] = 'h' 
            else:
                self.alliedhidden[self.uniquecount] = 'h'

        self.myboard = self.boardconvert(piecelist,board)    
        if self.color == 'red':
            self.myboardsred.append(self.myboard)
        elif self.color == 'blue':
            self.myboardsblue.append(self.myboard)  

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
                        
            
    def boardconvert(self,piecelist,boardd): #convert a board passed from the engine to here
        #assign the unique identifier to the board position along with the piece 
        w, h = 8, 10;
        i_board = [['-1' for x in range(h)] for y in range(w)] #internal function board
        for x in range(len(boardd)):
            for y in range(10):
                for piece in piecelist:
                    if (x,y) == (casy(piece.rect.centery)-1,casx(piece.rect.centerx)):
                        i_board[x][y] = boardd[x][y]+"Q"+str(self.pieceident[hash(piece)])                 
        return i_board
        
    #def parsemove(self,boardd,previous_move):
        #use previous move to determine if the piece is a two        
       
    def read_in_go(self,board_version_moves,turncount,previous_move,board,piecelist):
        #this function houses the main AI logic
        
        #convert the given board to one the AI can use
        self.myboard = self.boardconvert(self.piecelist,board)
        if self.color == 'red':
            self.myboardsred.append(self.myboard)
        elif self.color == 'blue':
            self.myboardsblue.append(self.myboard)                                 
            
            #todo: make way to check if unique identifer has been discovered or not, if not, replace board info with -2
            #bring unique identifier along with piece
    
        #count number of friendly pieces, if it went down by one, we lost someone to combat and know who they are
        #need to implement the logic; find place that's different, and then see what piece is there and such
        friendlycount = 0
        if self.color == 'red':   
            for x in range(len(self.board)):
                for y in range(10):
                    if 'r' in self.myboard[x][y]:
                        friendlycount+=1
                    if 'r' in self.myboardsred[-1]:
                        friendlycount+=1
        elif self.color == 'blue':
            for x in range(len(self.board)):
                for y in range(10):
                    if 'r' in self.myboard[x][y]:
                        friendlycount+=1
                    if 'r' in self.myboardsblue[-1]:
                        friendlycount+=1
                        

        if self.color == 'red':
            print(len(self.myboardsblue))
            try:
                if self.myboardsblue[-1] == self.myboardsblue[-2]:
                    print("They are the same, fuck you.")
                else:
                    print("they are different.")
            except IndexError:
                gg=2
        
        elif self.color == 'blue': 
            print(len(self.myboardsblue))
            try:
                if self.myboardsblue[-1] == self.myboardsblue[-2]:
                    print("They are the same, fuck you.")
                else:
                    print("they are different.")
            except IndexError:
                gg=2
        
        self.allyrankvalues = self.rank_value_calc(self.totalAllies,self.totalEnemies)
        self.enemyrankvalues = self.rank_value_calc(self.totalEnemies,self.totalAllies)
        
        #print(self.allyrankvalues)
        #print(self.enemyrankvalues)
        
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
        
        '''
        def update_board(move, ai_board):
            self.allboards
            ib = copy(ai_board)
            if ib[move[0]] == 10 and ld[ib[move[1]]] == 1: #spy
                ib[move[0]] = ib[move[1]]
                ib[move[1]] = -1
            elif ib[move[0]] == 11 and ld[ib[move[1]]] == 3: #miner
                ib[move[0]] = ib[move[1]]
                ib[move[1]] = -1
            elif ib[move[0]] < ld[ib[move[1]]]: #win
                ib[move[0]] = ib[move[1]]
                ib[move[1]] = -1    
            elif ib[move[0]] > ld[ib[move[1]]]: #lose
                ib[move[1]] = -1
            elif ib[move[0]] == ld[ib[move[1]]]: #tie
                ib[move[1]] = -1
                ib[move[0]] = -1 
            self.allboards.append(copy(ib))
        '''
        #now the board is in its proper form. So now we need to go through the moves and make all the new boards.
        
        self.allboards = []
        allmovesforfunc = []
        for option in board_version_moves:
            yps = option[0]-1 #y
            xps = option[1]
            ypt = casy(option[2].rect.centery)-1
            xpt = casx(option[2].rect.centerx)    
            move = ((ypt,xpt),(yps,xps))
            allmovesforfunc.append(move)
            try:
                ld[ai_board[move[1]]]
            except:
                continue
            #update_board(move,ai_board)

        
        '''
        m1 = np.zeros((1,10)) #empty matrix row
        m1.fill(-1)
        m1 = m1.astype(int)
                       
        counter = 0    
        for matrix in self.allboards:
            matrix = np.asarray(matrix)
            matrix = matrix.astype(int)
            matrix = np.vstack((m1,matrix,m1))
            self.allboards[counter] = copy(matrix)
            counter+=1
        '''           
        
        #allsamples = np.array(self.allboards)
        #allsamples = allsamples.reshape(len(allsamples),10,10,1)
        #preds = model.predict(allsamples)   
        #preds = preds.tolist()
        #random.shuffle(preds)
        #maxmove = board_version_moves[preds.index(max(preds))]
        
        #reverse it for the enemy calculations
        #create a function that does the following:
        #updates the enemy or allied piece lists from the last move
        
        #for the objective function, sum the number of allied pieces that are hidden and subtract the number of enemy pieces that are
        ai_board = np.asarray(ai_board)
        #[((1,0),(0,0)),((0,1),(0,0))]
        movestrengths = getboards.move_strength_ultimate([ai_board],allmovesforfunc,10) #current board, move list, recursion_depth
        justnumbers = []
        for move in movestrengths:
            #print(move)
            justnumbers.append(copy(move))
        
        print(justnumbers)
        #print(board_version_moves)
        random.shuffle(justnumbers) #so if a couple have the same value, we'll get a random one of the best, since max takes the first occurrence of that value
        move = board_version_moves[justnumbers.index(max(justnumbers))]
        print("move selection complete.",move)
        return move
    
    #output turn count and board to a text file
        
    
    
    