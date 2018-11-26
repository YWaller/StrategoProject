# -*- coding: utf-8 -*-

import numpy as np
from copy import copy, deepcopy
import keras
from keras.models import load_model
model = load_model('neuralstrategoALL.h5')

typecheck = np.asarray(3.4) #I'm lazy and this is easy; it gets used to check if the type of certain things are equal to array. Couldn't get it to recognize "array" or anything, and had more important stuff to do

#this file might be named "getboards," but it actually does all the tree search stuff so :P


ld = {} #this is used to translate pieces for combat evaluation 
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
ld[-1] = -1

md = {} #md is used to flip boards
md[-1] = -1
md[21] = 1
md[22] = 2
md[23] = 3
md[24] = 4
md[25] = 5
md[26] = 6
md[27] = 7
md[28] = 8
md[29] = 9
md[30] = 10
md[20] = 0
md[31] = 11
md[1] = 21
md[2] = 22
md[3] = 23
md[4] = 24
md[5] = 25
md[6] = 26
md[7] = 27
md[8] = 28
md[9] = 29
md[10] = 30
md[0] = 20
md[11] = 31
md[-1] = -1
no=[(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)] #list of board locations where no piece can move
unitno = [1,2,3,4,5,6,7,8,9,10] #just a list of pieces that can move
unitteam = [0,1,2,3,4,5,6,7,8,9,10,11] #list of our team's pieces
moveless = {0,11,30,31,20,21,22,23,24,25,26,27,28,29} #a set of pieces that we cannot move

def create_boardnot2(move,recurboard): #FOR THESE MOVE[0] IS TARGET AND MOVE[1] IS SOURCE; evaluates the given move and returns a board, for pieces that are not 2s.
    reb = copy(recurboard)
    global counter
    global counter2
    global recur
    if move[0] in no: #this means the attempted move is a block
        pass
    elif reb[move[0]] in unitteam:       
        pass
    else:
        if ld[reb[move[0]]] == 10 and ld[reb[move[1]]] == 1: #spy
            reb[move[0]] = reb[move[1]]
            reb[move[1]] = -1
        elif ld[reb[move[0]]] == 11 and ld[reb[move[1]]] == 3: #miner
            reb[move[0]] = reb[move[1]]
            reb[move[1]] = -1
        elif ld[reb[move[0]]] > ld[reb[move[1]]]: #win
            reb[move[1]] = reb[move[0]]
            reb[move[0]] = -1    
        elif ld[reb[move[0]]] < ld[reb[move[1]]]: #lose
            reb[move[0]] = -1
        elif ld[reb[move[0]]] == ld[reb[move[1]]]: #tie
            reb[move[1]] = -1
            reb[move[0]] = -1
        recur.append(copy(reb))
        counter2+=1 
        
def create_board(move,recurboard): #FOR THESE MOVE[0] IS TARGET AND MOVE[1] IS SOURCE; evaluates the given move and returns a board, for pieces that ARE 2s.
    reb = copy(recurboard)
    global counter
    global counter2
    global recur
    if move[0] in no: #this means the attempted move is a block
        pass
    elif reb[move[0]] in unitteam: 
        pass
    else:
        if ld[reb[move[0]]] < ld[reb[move[1]]]: #win
            reb[move[0]] = reb[move[1]]
            reb[move[1]] = -1  
        elif ld[reb[move[0]]] > ld[reb[move[1]]]: #lose
            reb[move[1]] = -1
        elif ld[reb[move[0]]] == ld[reb[move[1]]]: #tie
            reb[move[1]] = -1
            reb[move[0]] = -1
        recur.append(copy(reb))
        counter2+=1  
        return 0


def check_terminal(board): #tries to determine if a board state is terminal. Note, if pieces exist but have no viable moves (e.g. they're incased by bombs), then g_a_b implicitly handles that
        if np.count_nonzero(board) != 79: #the first two check to see if either side has lost their flag on this board
            return True
        
        flipped = copy(board)
        x=0
        for row in flipped:
            y=0
            for piece in row:
                flipped[x,y] = md[piece]
                y+=1
            x+=1
        if np.count_nonzero(flipped) != 79: #there should only be one zero, hence the non-zero count should be 79
            return True 
        
        anynotin = set(np.asarray(board).ravel()) - moveless #this one checks to see if this team has any pieces that can move
        if len(anynotin) == 1:
            return True

        anynotin = set(np.asarray(flipped).ravel()) - moveless
        if len(anynotin) == 1:
            return True
        
        return False

   
def get_all_boards(allboards): #given a board (or boards), returns all the possible one-depth-away boards that could result from it. TODO: plugging in terminal score, so we know how many boards result in a win/loss for us at this depth; if there are viable pieces but they're trapped, also add that to terminal score.
    global counter2
    global counter
    global recur
    counter2 = 0
    counter = 0
    recur = []
            
    #board-->row in board-->piece in board-->if the unit is in the allowed list-->if the unit is a 2-->rotate through all options of movement for either one
    counter=0
    oo=0
    counter2=0
    terminal_score = 0
    allboards = error_check_boards(allboards)
    for boardop in allboards:
        boardop = np.asarray(boardop)

        if check_terminal(boardop): #returns true if the board state is terminal, goes to the next board
            continue

        x=0        
        for row in boardop:
            y=0
            for piece in row:
                #print(x,y)
                if boardop[x,y] in unitno:
                    if boardop[x,y] != 2: #if the unit isn't a 2
                        #print("no whiles")
                        try:
                                #these four handle if the unit is on our side. The function handles if it's out of bounds
                            move=((x-1,y),(x,y))
                            create_boardnot2(move,boardop)
                        except IndexError:
                            pass #placeholder
                        try:
                            move=((x,y-1),(x,y))
                            create_boardnot2(move,boardop)      
                        except IndexError:
                            pass  
                        try:
                            move=((x,y+1),(x,y))
                            create_boardnot2(move,boardop)   
                        except IndexError:
                            pass
                        try:
                            move=((x+1,y),(x,y))
                            create_boardnot2(move,boardop) 
                        except IndexError:
                            pass
                    else: #handling if the unit is a 2
                        i = 0
                        j = 0
                        #print("whiles")
                        while x-i >= 0 and j == 0: #have we hit a wall or encountered a unit?
                            move=((x-i,y),(x,y))
                            create_board(move,boardop)
                            i+=1
                            #print("while1")
                            try:
                                if boardop[x-i,y] > -1: #encountered a unit
                                    j+=1
                            except IndexError:
                                j+=1
                        i=0 
                        j = 0
                        while x+i <= 7 and j == 0:
                            move=((x+i,y),(x,y))
                            create_board(move,boardop)
                            i+=1  
                            #print("while1")                        
                            try:
                                if boardop[x+i,y] > -1: #encountered a unit
                                    j+=1
                            except IndexError:
                                j+=1
                        i=0
                        j = 0
                        while y-i >= 0 and j == 0:
                            move=((x,y-i),(x,y))
                            create_board(move,boardop)
                            i+=1
                            #print("while1")                        
                            try:
                                if boardop[x,y-i] > -1: #encountered a unit
                                    j+=1
                            except IndexError:
                                j+=1
                        i=0
                        j = 0
                        while y+i <= 9 and j == 0: 
                            move=((x,y+i),(x,y))
                            create_board(move,boardop)
                            i+=1
                            #print("while1")                        
                            try:
                                if boardop[x,y+i] > -1: #encountered a unit
                                    j+=1
                            except IndexError:
                                j+=1
                        i=0
                        j = 0                    
                y+=1         
            x+=1    
        counter+=1
        #if terminal_counter == 0:
        #    terminal_score += 1
    L = {array.tostring(): array for array in recur}
    #print(len(recur),"all boards")
    recur = list(L.values())
    #print(len(recur),"recur")
    if len(recur) > 1:
        return [recur]
    else:
        return recur


def do_move(upboard, move): #processes a move on a board
    print(move,"the move")
    #print(type(upboard),"type")
    #print(len(upboard),"len")
    upboard = np.asarray(upboard)
    #keepercheck = copy(upboard)
    if upboard[move[0]] == 1 and ld[upboard[move[1]]] == 10: #spy
        upboard[move[1]] = upboard[move[0]]
        upboard[move[0]] = -1
    elif upboard[move[0]] == 3 and ld[upboard[move[1]]] == 11: #miner
        upboard[move[1]] = upboard[move[0]]
        upboard[move[0]] = -1
    elif upboard[move[0]] > ld[upboard[move[1]]]: #win
        upboard[move[1]] = upboard[move[0]]
        upboard[move[0]] = -1  
    elif upboard[move[0]] < ld[upboard[move[1]]]: #lose
        upboard[move[0]] = -1
    elif upboard[move[0]] == ld[upboard[move[1]]]: #tie      
        upboard[move[1]] = -1
        upboard[move[0]] = -1 

    return upboard

def worth_considering(nestedboards): #given some boards, and their scores, return the ones we think this player would actually consider. 
    nested2=[]
    nestedpreds = get_scores(nestedboards)
    nestedboards = error_check_boards(nestedboards)
    considering = [x for (y,x) in sorted(zip(nestedpreds,nestedboards), key = lambda pair: pair[0],reverse=True)] #these two lines get only the top half of the boards available,
    nested2 = considering[:int(len(considering)/2)+1] #which represents the assumption that players won't do something heinously stupid
    
    predsforconsidering = [y for (y,x) in sorted(zip(nestedpreds,nestedboards), key = lambda pair: pair[0],reverse=True)]
    sendpreds = predsforconsidering[:int(len(predsforconsidering)/2)+1]
    #nested3 = []
    #nested3.append(considering[0])
    #nested3.append(considering[-1]) #in case we just want to use the most and least likely board, for speed
    
    return [nested2],sendpreds

def get_scores(nestedboards): #passes all the boards to the model and gets the resulting scores.
    #print("get scores")
    scoreboards = []
    #print(len(nestedboards),"get scores 1")
    nestedboards = error_check_boards(nestedboards)
    #print(nestedboards[0])    
    for matrix in nestedboards:
        matrix = np.asarray(matrix)
        scoreboards.append(copy(np.interp(matrix, (-1, 31), (-1, +1))))
    m1 = np.zeros((1,10)) #empty matrix row
    m1.fill(-1)
    m1 = m1.astype(int)       
    iterboards = [] 
    for matrix in scoreboards:
        matrix = matrix.astype(int)
        matrix = np.vstack((m1,matrix,m1))
        iterboards.append(copy(matrix))
    allsamples = np.asarray(iterboards)
    allsamples = allsamples.reshape(len(allsamples),10,10,1)
    preds = model.predict(allsamples)          
    return preds
    
def flip_boards(playernumber,nestedboards): #turns all boards with the pieces changed to be from the perspective of the other player.
    #print(len(nestedboards),"flip boards 1")
    #print("flip boards")
    counter900 = 0
    incase = error_check_boards(nestedboards)
    if playernumber > 0:
        for entry in incase:
            #entry = np.asarray(entry)
            counter900=0
            x=0
            for row in entry:
                y=0
                for piece in row:
                    entry[x,y] = md[piece]
                    y+=1
                x+=1
            incase[counter900] = copy(entry)
            counter900+=1
    else:
        pass
    #print(len(incase),"flip boards 2")
    return incase


def error_check_boards(boardlist): #makes sure that all functions are receiving the same input. Could I just fix the functions to produce the same input? Sure. But this was easier :P
    incase = []
    thirdcase = []
    incase = boardlist
    #print(len(incase),"try me?")
    #print(len(incase[0]),"hmm hmm")
    #print(len(incase[0]),"check len PRIOR")
    if len(incase) == 0:
        print("houston, we have a problem...")
        #return []
    if len(incase[0]) != 8 and len(incase) == 1 and len(incase[0]) > len(incase):
        incase = incase[0]   
        #print("error 1")
    #print(len(incase[0]),"check len")
    #if len(incase)
    if len(incase[0]) == 1:
        print("error 2")
        thirdcase = []
        for board in incase:
            thirdcase.append(copy(np.asarray(board[0])))
        incase = copy(thirdcase) 
    if (len(incase[0])) == 2:
        print("error 3")
        thirdcase = []            
        for board in incase:
            thirdcase.append(copy(board[0]))
            thirdcase.append(copy(board[1]))
        incase = copy(thirdcase)
    
    if len(incase[0]) > len(incase) and not len(incase[0]) == 8:
        print("error 4")
        print(len(incase))
        print(incase[0])
        incase = incase[0]
    if len(incase[0][0]) == 8 and type(incase[0][0]) == type(typecheck):
        print("error 5")
        incase = incase[0]
        
    L = {array.tostring(): array for array in incase} #get rid of duplicate boards
    incase = list(L.values()) 
        
    return incase
    


def node_strength(nestedboards,playernumber,boardstrength): #gets the overall strength of the boards given to it, and updates the boardstrength of the parent
    nestedboards = flip_boards(playernumber,nestedboards)
    #print(len(nestedboards),"node strength 1")
    boardfilter, usepreds = worth_considering(nestedboards)
    #print(len(boardfilter),"node strength 2")
    assert len(boardfilter[0]) == len(usepreds)
    #usepreds = get_scores(boardfilter[0])
    #print(sum(usepreds)/len(usepreds),"average")
    #print("     average for preds",(sum(usepreds)/len(usepreds)))
    if playernumber % 2 == 0:
        boardstrength += (sum(usepreds)/len(usepreds)) #+len(usepreds)/1000 #this slightly gives preference to board positions that give us more options down the road
    else:
        boardstrength -= (sum(usepreds)/len(usepreds))/2 
    if type(boardstrength) == [] or type(boardstrength) == type(typecheck):
        return (boardstrength[0], copy(boardfilter))
    return (boardstrength, copy(boardfilter))
    

def top_recursion_func(resultboard,playernumber,recursion_depth): #The meat and potatoes of move selection. Uses node_strength, is hooked into by m_s_u and obergruppen. Goes through the boards from the AI's pov and the other player's.
    boardstrength = 0
    nestedboards = get_all_boards([resultboard])
    nestedboardsalpha = nestedboards[0]
    #terminal_counter = 0
    
    recursion_remainder = recursion_depth
    while recursion_remainder > 0:
        print("depth: ",recursion_remainder)
        container = node_strength(nestedboardsalpha,playernumber,boardstrength)
        boardstrength = container[0] #we don't reassign the boards until AFTER our and our enemy's positions at THESE boards have been counted
        nestedboardsalpha = error_check_boards(nestedboardsalpha)
        #print("passed first")
        playernumber+=1
        container = node_strength(nestedboardsalpha,playernumber,boardstrength)
        boardstrength, nestedboardsalpha = container[0], container[1]
        #print(len(nestedboardsalpha),"top recur 1")
        #print(nestedboardsalpha[0],"alphazero") #yes I named this this so I could make that joke
        nestedboardsalpha = get_all_boards(nestedboardsalpha)
        if nestedboardsalpha[0] == []:
            break
        recursion_remainder -= 1

    if type(boardstrength) == [] or type(boardstrength) == type(typecheck):
        return boardstrength[0]
    return boardstrength


def obergruppen_recurse(strengthlist,move_list,move_value_cutoff,playernumber,recursion_depth,starting_board, consider_depth): #This function is used in m_s_u. It handles recursion and move ordering.
    optioncount = 0    
    for option in move_list:
        if strengthlist[move_list.index(option)] <= move_value_cutoff:
            pass
        else:
            print("considering depth: ",round(optioncount/(len(move_list)),2), consider_depth, strengthlist[optioncount])
            moveboard = do_move(copy(starting_board[0]),option)
            strengthlist[optioncount] = top_recursion_func(copy(moveboard),playernumber,round(recursion_depth/2))
            optioncount+=1
    return strengthlist



def move_strength_ultimate(starting_board,move_list,recursion_depth): #This is the main function. You'll notice it hooks into SAI. It decides what moves to look at.
    optioncount = 0
    playernumber = 0
    strengthlist = [[]]*len(move_list)
    print("number of moves: ", len(move_list))
    for option in move_list:
        moveboard = do_move(copy(starting_board[0]),option)
        #strengthlist[optioncount] = 0
        strengthlist[optioncount] = top_recursion_func(moveboard,playernumber,1)
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




'''
keys = [0,1,2,3,4,5,6,7,8,9,10,11]
no=[(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)]

initialvalues = list()
for i in range(1,12):
    initialvalues.append(round(i/12.0,3))
    
#            flag   spy   2     3      4      5     6     7      8      9     10    bomb
ivsattack = [0.0, 0.166, 0.5, 0.333, 0.333, 0.417, 0.5, 0.583, 0.667, 0.75, 0.833, 0.0917]
    
attack=dict(zip(keys,ivsattack))

#            flag   spy   2     3      4      5     6     7      8      9     10    bomb
ivsdefense = [0.0, 0.266, 0.18, 0.35, 0.333, 0.357, 0.4, 0.483, 0.567, 0.65, 0.733, 0.917]

def manhattan_dist(move): #order doesn't matter
    a = move[0][0]
    b = move[0][1]
    c = move[1][0]
    d = move[1][1]
    mandist = abs(a-c)+abs(b-d)
    
    if (any (abs(a-box[0])+abs(b-box[1])) == mandist for box in no):
        #calculate go-around logic
    
    return mandist

defense=dict(zip(keys,ivsdefense))

def board_threats(starting_board,move_list):
'''      


       
'''
starting_board = [([[ 6, -1, -1,  11, 0,  11, -1,  -1,  -1, -1],
       [-1, -1, -1, -1, -1, -1, -1,  11, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, 1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, 2],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [-1, -1, -1, 20, 31, -1, 25, -1, -1, -1]])]
move_list=[((0,0), (1,0)), ((0,0), (2,0)), ((0, 0), (3, 0)), ((0, 0), (4, 0)), ((0, 0), (5, 0)), ((0, 0), (6, 0)), ((0, 0), (0, 1)), ((0, 0), (0, 2)), ((0, 4), (1, 4)), ((0, 5), (1, 5)), ((0, 6), (1, 6)), ((0, 6), (2, 6)), ((0, 8), (1, 8)), ((0, 8), (0, 9)), ((1, 7), (2, 7)), ((1, 7), (1, 6)), ((1, 7), (1, 8))]
#strengthlist = move_strength_ultimate(starting_board,move_list,3)
#import cProfile
#cProfile.run('move_strength_ultimate(starting_board,move_list,10)')

babo = move_strength_ultimate(starting_board,move_list,4)
print(babo)
'''








