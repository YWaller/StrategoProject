# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 23:07:21 2017

@author: Yale
"""
#import all the functions from the game engine
#from mainwithai import * #Lesson: don't make circular references to other files, won't run; obvious when you realize it
import random


sys_random = random.SystemRandom()

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
        self.she=[] #specific hidden enemies
        if self.color == 'red':
            self.othercolor = 'blue'
        elif self.color == 'blue':
            self.othercolor = 'red'
        self.scoreline = 0
        self.allyrankvalues
        self.enemyrankvalues
            
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
        basevalue[str(1)] = .02
        for i in range(2,11):
            if (self.totalAllies[str(i-1)]+self.totalAllies[str(i)] > 0)  AND (self.totalEnemies[str(i-1)]+self.totalEnemies[str(i)]>0):
                basevalue[str(i)] = basevalue[str(i-1)]*rankdifffactor
            else:
                basevalue[str(i)] = basevalue[str(i-1)]
        
        #gets the highest value of basevalue for scaling
        highest = max(basevalue.iterkeys(), key=(lambda key: basevalue[key]))
        #scale all the values and then add a value
        for i in range(11):
            basevalue[str(i)] = float(basevalue[str(i)])/float(highest)+(.5/sum(basevalue.itervalues()))
        #specific pieces with alternate values
        
        #if there's an enemy spy, reduce the 10's importance
        if self.totalEnemies[str(1)] != 0:
            basevalue[str(10)] = basevalue[str(10)]*.8
            
        highest = max(basevalue.iterkeys(), key=(lambda key: basevalue[key]))        
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
        
    def read_in_go(self,board_version_moves,turncount,previous_move,board):
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
            print len(self.myboardsblue)
            try:
                if self.myboardsblue[-1] == self.myboardsblue[-2]:
                    print "They are the same, fuck you."
                else:
                    print "they are different."
            except IndexError:
                gg=2
        
        elif self.color == 'blue': 
            print len(self.myboardsblue)
            try:
                if self.myboardsblue[-1] == self.myboardsblue[-2]:
                    print "They are the same, fuck you."
                else:
                    print "they are different."
            except IndexError:
                gg=2
        
        self.allyrankvalues = rank_value_calc(self,self.totalAllies,self.totalEnemies)
        self.enemyrankvalues = rank_value_calc(self,self.totalEnemies,self.totalAllies) #reverse it for the enemy calculations
        #create a function that does the following:
        #updates the enemy or allied piece lists from the last move
        
        #for the objective function, sum the number of allied pieces that are hidden and subtract the number of enemy pieces that are
        
        move = sys_random.choice(board_version_moves)
            
        return move
        
    