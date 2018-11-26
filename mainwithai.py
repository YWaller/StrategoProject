# -*- coding: utf-8 -*-
import configparser
import sys, time, pygame
from pygame.locals import *
import random
import re
from SAI import AI_Player


#This code is used for reversing the coordinate lists down below so that x and y are in their proper places  
def sublistreverse(L):
    for sublist in L:
        sublist.reverse()
    return L 

def coordx(cox):
    return 150+25+50*cox
    
def coordy(coy):
    return 50+25+50*coy
    
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
        
def next_turn(turn):
    deselect_all()
    return not turn
    
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error as message:
            raise SystemExit(message)
    #image = image.convert()
    if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
    return image    
    
def update_mouse(mouse_pressed,mouse_down,mouse_released,mouse_up):

    if pygame.mouse.get_pressed()[0] == 1:

        if not mouse_pressed and not mouse_down:
            mouse_up = False
            mouse_released = False
            mouse_pressed = True

        elif mouse_pressed and not mouse_down:
            mouse_pressed = False
            mouse_down = True

    else:

        if not mouse_released and not mouse_up:
            mouse_released = True
            mouse_pressed = False
            mouse_down = False

        else:
            mouse_released = False
            mouse_up = True
    return mouse_pressed,mouse_down,mouse_released,mouse_up
        
def check_unit(mousepos):
    for piece in piecelist:
        if (casx(mousepos[0]),casy(mousepos[1])) == piece.get_pos():
            return piece
        
def check_unit_ai(move):
    for piece in piecelist:
        if (move[0],move[1]) == piece.get_pos():
            return piece

def check_move(mousepos):
    for piece in piecelist:
        # If there is a selected unit, check if it can move
        #show all possible moves
        if piece.selected:
            moves = piece.show_moves()
            for move in moves:
                if (casx(mousepos[0]),casy(mousepos[1])) == (casx(move[0]),casy(move[1])):
                    return move
            break
            
def deselect_all():
    for piece in piecelist:
        piece.selected = False;

def choose_selected():
    for piece in piecelist:
        if piece.selected:
            return piece
            
def do_move(mousepos):
    global board
    unit = choose_selected()
    board[casy(unit.rect.centery)-1][casx(unit.rect.centerx)]='-1' #remove the unit from its old position
    unit.rect.centerx = coordx(casx(mousepos[0]))
    unit.rect.centery = coordy(casy(mousepos[1]))
    updoot = str(unit.level)+unit.team[0]
    board[casy(unit.rect.centery)-1][casx(unit.rect.centerx)]=updoot #put the unit in its new board position so the computer knows

def do_move_ai(move): #Allows the AI to manipulate the board
    #unit = piecelist[0]
    global board
    '''
    p = -1
    q = -1
    EVERYTHING commented out is related to fixing updating the board position. 
    for i in range(len(board)):
        for j in range(len(board[i])):
            if "b" in board[i][j]:
                inter=re.search('\d+',board[i][j])
                rank=inter.group()
                print rank
                print move[2].level
                if int(rank) == move[2].level:
                    p = i
                    q = j
                    print("found it!"
    '''
    #print board[p][q]
    #print("compare"
    #print board[casy(move[2].rect.centery)-1][casx(move[2].rect.centerx)]

    board[casy(move[2].rect.centery)-1][casx(move[2].rect.centerx)]='-1' #remove the unit from its old position
    #print board[casy(move[2].rect.centery)-1][casx(move[2].rect.centerx)]    
    move[2].rect.centerx = coordx(move[1])
    move[2].rect.centery = coordy(move[0])
    updoot = str(move[2].level)+move[2].team[0]
    #print("second pair"
    #print board[move[0]-1][move[1]]
    board[move[0]-1][move[1]]=updoot #put the unit in its new board position so the computer knows
    #print board[move[0]-1][move[1]]
    #print("new oh boy"
        
def do_attack_ai(move,attacked):
    global flagcap
    global loserteam
    global board
    attacker=move[2]
    
    # spy
    if attacked.level == 10 and attacker.level == 1:
        #do_move_ai(move)
        destroy_unit(attacked)
        print("spy wins")
        updoot = str(move[2].level)+move[2].team[0]
        board[move[0]-1][move[1]]=updoot
        attacker.rect.centerx = coordx(move[1])
        attacker.rect.centery = coordy(move[0])
        board[casy(attacked.rect.centery)-1][casx(attacked.rect.centerx)]='-1'        
        return 1
    # miner
    if attacked.level == 11 and attacker.level == 3:
        #do_move_ai(move)
        print("miner wins")
        updoot = str(move[2].level)+move[2].team[0]
        board[move[0]-1][move[1]]=updoot
        attacker.rect.centerx = coordx(move[1])
        attacker.rect.centery = coordy(move[0])
        board[casy(attacked.rect.centery)-1][casx(attacked.rect.centerx)] = '-1'         
        destroy_unit(attacked)
        return 1
    elif attacked.level < attacker.level:
        #do_move_ai(move)
        print("attacker wins")
        destroy_unit(attacked)
        updoot = str(move[2].level)+move[2].team[0]
        board[move[0]-1][move[1]]=updoot
        attacker.rect.centerx = coordx(move[1])
        attacker.rect.centery = coordy(move[0])
        board[casy(attacked.rect.centery)-1][casx(attacked.rect.centerx)] = '-1'
        if attacked.level == 0:
            flagcap = True
            loserteam = attacked.team
        return 1
    elif attacked.level > attacker.level:
        print("defender wins")
        destroy_unit(attacker)
        board[move[0]-1][move[1]]='-1'
        return -1
    elif attacked.level == attacker.level:
        print("tie")
        destroy_unit(attacker)
        destroy_unit(attacked)
        board[move[0]-1][move[1]]='-1'
        board[casy(attacked.rect.centery)-1][casx(attacked.rect.centerx)] = '-1'
        return 0    
    
def do_attack(attacked):
    global flagcap
    global loserteam
    global board
    attacker = choose_selected()
    updoot='x'
    # spy
    if attacked.level == 10 and attacker.level == 1:
        do_move((attacked.rect.centerx,attacked.rect.centery))
        updoot=board[casy(attacker.rect.centery)-1][casx(attacker.rect.centerx)]
        board[casy(attacker.rect.centery)-1][casx(attacker.rect.centerx)]='-1'
        board[casy(attacked.rect.centery)-1][casx(attacked.rect.centerx)]=updoot  
        destroy_unit(attacked)
        print("spy wins")
        return 1
    # miner
    if attacked.level == 11 and attacker.level == 3:
        do_move((attacked.rect.centerx,attacked.rect.centery))
        updoot=board[casy(attacker.rect.centery)-1][casx(attacker.rect.centerx)]
        board[casy(attacker.rect.centery)-1][casx(attacker.rect.centerx)]='-1'
        board[casy(attacked.rect.centery)-1][casx(attacked.rect.centerx)]=updoot 
        print("miner wins")
        destroy_unit(attacked)
        return 1
    elif attacked.level < attacker.level:
        do_move((attacked.rect.centerx,attacked.rect.centery))
        updoot=board[casy(attacker.rect.centery)-1][casx(attacker.rect.centerx)]
        board[casy(attacker.rect.centery)-1][casx(attacker.rect.centerx)]='-1'
        board[casy(attacked.rect.centery)-1][casx(attacked.rect.centerx)]=updoot
        print("attacker wins")
        destroy_unit(attacked)
        if attacked.level == 0:
            flagcap = True
            loserteam = attacked.team
        return 1
    elif attacked.level > attacker.level:
        print("defender wins")
        destroy_unit(attacker)
        return -1
    elif attacked.level == attacker.level:
        print("tie")
        destroy_unit(attacker)
        destroy_unit(attacked)
        return 0

    
def destroy_unit(unit):
    piecelist.remove(unit)
    board[casy(unit.rect.centery)-1][casx(unit.rect.centerx)]='-1'
    
def check_win():
    text = Text()
    if flagcap:
        if loserteam == 'blue':
            print("Red wins by flag")
            text.render(screen, "red wins", (255,0,0), (10, 10))
            pygame.display.flip()            
            return True
        elif loserteam == 'red':
            print("Blue wins by flag")
            text.render(screen, "blue wins", (0,0,255), (10, 10))
            pygame.display.flip()            
            return True
    
    #T1 this needs a serious rework
    red = True
    blue = True
    
    bluedoomcnt = 0
    reddoomcnt = 0
    for piece in piecelist:
        if piece not in [11,0] and piece.team == 'blue':
            bluedoomcnt+=1
        elif piece not in [11,0] and piece.team == 'red':
            reddoomcnt+=1
            
    #if either of the above are zero, that team has lost
    if reddoomcnt == 0:
        red = False
    elif bluedoomcnt == 0:
        blue = False #blue has no pieces other than bombs and the flag

    #do some checks to see if the game is over. Remember we do the check to see if all moves is empty elsewhere
    if red and blue:
        return False
    elif red and not blue:
        print("red wins by no moves")
        text.render(screen, "red wins", (255,0,0), (10, 10))
        pygame.display.flip()
        return True
    elif blue and not red:
        print("blue wins by no moves")
        text.render(screen, "blue wins",  (0,0,255), (10, 10))
        pygame.display.flip()
        return True
    else:
        print("tie")
        text.render(screen, "tie",  (255,0,0), (10, 10))
        pygame.display.flip()
        return True

def do_end():
    print(board)
    time.sleep(3)
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
        
        
def draw_frame():
# show the board
    screen.blit(table, (0, 0))
    
    #put pieces on the board
    for piece in piecelist:
        screen.blit(piece.image,piece.rect)
        if piece.selected:
            moves = piece.show_moves()
            for point in moves:
                img_shadow = load_image("./resources/imgs/"+piece.get_data()[0]+"/shadow.png")
                screen.blit(img_shadow,point)
                
    # show text
    if turn:
        turn_text.render(screen, "Blue's turn",  (0,0,255), (10, 30))
        for piece in piecelist:
            currentteam = 'blue'
            if piece.team != currentteam:
                #piece.image = load_image("./resources/imgs/red/"+"hidden.png", False)
                piece.image = load_image("./resources/imgs/red/"+str(piece.level)+".png", False)
            else:
                piece.image = load_image("./resources/imgs/blue/"+str(piece.level)+".png", False)
    else:
        turn_text.render(screen, "Red's turn",  (255,0,0), (10, 30))
        for piece in piecelist:
            currentteam = 'red'
            if piece.team != currentteam:
                #piece.image = load_image("./resources/imgs/blue/"+"hidden.png", False)
                piece.image = load_image("./resources/imgs/blue/"+str(piece.level)+".png", False)
            else:
                piece.image = load_image("./resources/imgs/red/"+str(piece.level)+".png", False)
        
    pygame.display.flip()
    
def initializesetup(pieces_map):
    localcounter = 10
    #turn optimization_setup into a function and pass it all the weights as inputs
    if makesetups:
        for piece in pieces_map:
            if piece != "\n":
                aux = piece.split()
                if turn:
                    aux = ["blue"] + aux + [localcounter]
                    piecelist.append(pieceinfo(aux[0],int(aux[1]),int(aux[2]),int(aux[3]),int(aux[4])))
                    localcounter+=1
                else:
                    aux = ["red"] + aux + [localcounter]
                    piecelist.append(pieceinfo(aux[0],int(aux[1]),int(aux[2]),int(aux[3]),int(aux[4])))
                    localcounter+=1
    else:    
        #loaded board state
        global RedBot
        global BlueBot
        ldb=[]
        aux=[]
        rank=0
        
        for line in pieces_map:
            ldb.append(line.split())
        
        for i in range(len(ldb)):
            for j in range(len(ldb[i])):
                if "r" in ldb[i][j]:
                    board[i][j] = ldb[i][j]
                    inter=re.search('\d+',ldb[i][j])
                    rank=inter.group()
                    aux=["red"]+[int(rank)]+[i+1]+[j] + [localcounter]
                    piecelist.append(pieceinfo(aux[0],int(aux[1]),int(aux[3]),int(aux[2]),int(aux[3])))
                    localcounter+=1
                elif "b" in ldb[i][j]:
                    board[i][j] = ldb[i][j]
                    inter=re.search('\d+',ldb[i][j])
                    rank=inter.group()
                    aux=["blue"]+[int(rank)]+[i+1]+[j] + [localcounter]
                    piecelist.append(pieceinfo(aux[0],int(aux[1]),int(aux[3]),int(aux[2]),int(aux[3])))
                    localcounter+=1
                else:
                    board[i][j] = '-1'
                   
    if RedPlayer == 'AI': #Give the AI the piecelist
        RedBot.initializepiecelist(piecelist,board)
    if BluePlayer == 'AI':
        BlueBot.initializepiecelist(piecelist,board)
        
def check_all_moves(color,othercolor):
    global chasecounterred
    global chasecounterblue
    global loserteam
    global endtime
    global all_moves
    
    all_moves = []
    
    for piece in piecelist:
        if piece.team == 'blue' and color == 'blue':
            if piece.show_moves():
                for sublist in piece.show_moves():
                    try:
                        if previous_move_red[turncount-2] != (sublist,piece): #can't move between the same place for two consecutive turns
                            all_moves.append((sublist,piece))
                        elif previous_move_blue[turncount-1][0] == previous_move_red[turncount-2][0]: #prevents chasing
                            chasecounterblue += 1
                            if chasecounterblue < 7:
                                all_moves.append((sublist,piece))
                            else:
                                chasecounterblue = 0
                    except:
                        all_moves.append((sublist,piece))
        elif piece.team == 'red' and color == 'red':
            if piece.show_moves():
                for sublist in piece.show_moves():
                    try:
                        if previous_move_red[turncount-2] != (sublist,piece): #can't move between the same place for two consecutive turns
                            all_moves.append((sublist,piece))
                        elif previous_move_blue[turncount-1][0] == previous_move_red[turncount-2][0]: #prevents chasing
                            chasecounterblue += 1
                            if chasecounterblue < 7:
                                all_moves.append((sublist,piece))
                            else:
                                chasecounterred = 0
                    except:
                        all_moves.append((sublist,piece))                            
                        
    #time.sleep(1)
    if not all_moves: #if we can't make any moves, that means we've lost.
        loserteam = color
        text.render(screen, "%s wins" % othercolor, (50,255,50), (10, 10))
        check_win()
        pygame.display.flip() 
        do_end()
        endtime = True
                    
def turn_logic(color):
    #this does all the turn stuff
    global turncount
    global mouse_pressed
    global mouse_down
    global mouse_released
    global mouse_up
    global previous_move_blue
    global previous_move_red
    global turn
    global chasecounterblue
    global chasecounterred
    global shadow_points
    global loserteam
    global board_version_moves
    global endtime
    global board
    
    if color == 'blue':
        othercolor = 'red'
        Player = BluePlayer
    else:
        othercolor = 'blue'
        Player = RedPlayer
        
    if Player == 'Human':
        #human blue player goes
        # update mouse position
        turncount += 1
        
        check_all_moves(color,othercolor)
        
        mouse_pressed,mouse_down,mouse_released,mouse_up = update_mouse(mouse_pressed,mouse_down,mouse_released,mouse_up)
        # select an pieceinfo object if selected by the mouse
        if mouse_pressed:
            mousepos = pygame.mouse.get_pos()
            unit = check_unit(mousepos)
            move = check_move(mousepos)
            # if there are other units on this team, deselect them
            print(othercolor)
            print(turn)
            if unit and (unit.team == "%s" % color):
                shadow_points = unit.sel(turn)
                # if selected, show movement options
                if unit.selected:
                    print("selected unit")
                else:
                    print("unit deselected")
            elif move:
                print("move initiated")
                # if no one is in the box, move there
                if not unit:
                    print("actually moved")
                    do_move(mousepos)
                    if color == 'blue':
                        human_move = list((move,choose_selected()))                       
                        previous_move_blue.append(human_move)
                    if color == 'red':
                        human_move = list((move,choose_selected()))                      
                        previous_move_red.append(human_move)            
                    turn = next_turn(turn)
                # if an enemy unit is there, run attack logic
                else:
                    print("attack")
                    do_attack(unit)
                    turn = next_turn(turn)
            else:
                print("nothing was done")
                print(move)    
    else:
        #random player... for now
        print("%s is an AI, on your toes" % color)
        turncount += 1
        
        check_all_moves(color,othercolor)

        #make all the moves into the board version so the AI can understand them
        board_version_moves=[]
        for move in all_moves:
            board_version_moves.append([casy(move[0][1]),casx(move[0][0]),move[1]])
           
        if turncount < 2: #fill the 0th slot of the previous move deals with nothing
            if color == 'red':
                previous_move_blue.append([-1,-1,'okay'])
            if color == 'blue':
                previous_move_red.append([-1,-1,'okay'])
        
        if color == 'blue':
            BlueBot.board = board
            ai_move = BlueBot.read_in_go(board_version_moves,turncount,previous_move_red[-1],board,piecelist)
        elif color == 'red':
            RedBot.board = board    
            ai_move = RedBot.read_in_go(board_version_moves,turncount,previous_move_blue[-1],board,piecelist)   
        
        #ai_move = sys_random.choice(all_moves)
        #ai_move = [coordx(ai_move[0]),coordy(ai_move[1]),ai_move[2]]
        if color == 'blue':
            previous_move_blue.append(ai_move)
        if color == 'red':
            previous_move_red.append(ai_move)            
        attackcount = 0
        for piece in piecelist:
            if check_unit_ai((ai_move[1],ai_move[0])) == piece:
                if piece.team == othercolor:
                    do_attack_ai(ai_move,piece)              
                    attackcount = 1
        if attackcount == 0:
            do_move_ai(ai_move)                
        turn = next_turn(turn)
        endtime = False
    
class pieceinfo(pygame.sprite.Sprite):
    def __init__(self,giventeam,level,cox,coy,identifier):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("./resources/imgs/"+str(giventeam)+"/"+str(level)+".png", False)
        self.rect = self.image.get_rect()
        self.rect.centerx = coordx(cox)
        self.rect.centery = coordy(coy)
        self.team = giventeam
        self.level = level
        self.selected = False
        self.identifier = identifier
        
    #we need to make sure the hashes are unique...    
    def __hash__(self):
        return hash((self.team, self.level, self.identifier))
        
    def mover(self,cox,coy):
        self.rect.centerx = coordx(cox)
        self.rect.centery = coordy(coy)
        
        
    def show_moves(self):
        if self.level == 11:
            # bombs can't move
            good_limits = list()
            
        elif self.level == 0:
            #flags can't move
            good_limits = list()
            
        elif self.level == 2:
            # draw color over places where you can move as a scout
            lim = [self.rect.centerx - 25, self.rect.centery - 25]
            stepper = 50
            negstepper = -50
            
            cellintervals=range(lim[1],0,negstepper)
            staticxy=lim[0]
            up = [[a]+[staticxy] for a in cellintervals]
            up = sublistreverse(up)
            
            cellintervals=range(lim[1],550,stepper)
            down = [[a]+[staticxy] for a in cellintervals]
            down = sublistreverse(down)
            
            cellintervals=range(lim[0],50,negstepper)
            staticxy=lim[1]
            left = [[a]+[staticxy] for a in cellintervals]
            
            cellintervals=range(lim[0],700,stepper)
            right = [[a]+[staticxy] for a in cellintervals]
            
            target_indexa=up.index(up[-1]) 
            target_indexb=down.index(down[-1])
            target_indexc=left.index(left[-1])
            target_indexd=right.index(right[-1])
            counter = 0
            closestpieceup = (self.get_pos()[0]-10,self.get_pos()[1]-10)
            closestpiecedown = (self.get_pos()[0]+10,self.get_pos()[1]+10) 
            closestpieceleft = (self.get_pos()[0]-10,self.get_pos()[1]-10)
            closestpieceright = (self.get_pos()[0]+10,self.get_pos()[1]+10)
            
            for item in up: #make the limits stop at units
                if counter == 0: #prevent it from stopping at itself
                    counter += 1 
                    next
                else: #make it stop at the appropriate unit
                    for piece in piecelist: 
                        if piece.get_pos()[0] == self.get_pos()[0]: #if the piece has the same x value as the current item, it is an option
                            if piece.get_pos()[1] != self.get_pos()[1]: #if it has the same y too, don't consider it
                                if piece.get_pos()[1] < self.get_pos()[1]:
                                    if (self.get_pos()[1]-piece.get_pos()[1]) < (self.get_pos()[1]-closestpieceup[1]):
                                        #^ if the difference between this piece's location and the target's location is less than the difference between this piece and the current closest piece's location...
                                        closestpieceup = piece.get_pos()
                                        if piece.team == self.team:
                                            target_indexa = up.index(list((item[0],piece.get_pos()[1]*50+50))) #undo casy (casx would be *50+150) and use index of this one as target
                                        else:
                                            target_indexa = up.index(list((item[0],piece.get_pos()[1]*50+50)))+1
            try: #target_index only exists when assigned inside the if loop, so if it does, we know to stop the direction there
                target_indexa
            except NameError:
                gg = 1
            else:
                up = up[1:target_indexa]
            counter = 0
            
            for item in down: #make the limits stop at units
                if counter == 0:
                    counter += 1
                    next
                else:
                    for piece in piecelist: 
                        if piece.get_pos()[0] == self.get_pos()[0]: 
                            if piece.get_pos()[1] != self.get_pos()[1]:
                                if piece.get_pos()[1] > self.get_pos()[1]:
                                    if (self.get_pos()[1]-piece.get_pos()[1]) > (self.get_pos()[1]-closestpiecedown[1]):
                                        closestpiecedown = piece.get_pos()
                                        if piece.team == self.team: #can't attack self so make sure not included in list
                                            target_indexb = down.index(list((item[0],piece.get_pos()[1]*50+50)))
                                        else:
                                            target_indexb = down.index(list((item[0],piece.get_pos()[1]*50+50)))+1
            try:
                target_indexb
            except NameError:
                gg = 1
            else:
                down = down[1:target_indexb]
            counter = 0
            
            for item in left: #make the limits stop at units
                if counter == 0:
                    counter += 1
                    next
                else:
                    for piece in piecelist: 
                        if piece.get_pos()[1] == self.get_pos()[1]: #same y, consider it
                            if piece.get_pos()[0] != self.get_pos()[0]: #same x too, toss it it's self
                                if piece.get_pos()[0] < self.get_pos()[0]: #make sure it's actually to the left...
                                    if (self.get_pos()[0]-piece.get_pos()[0]) < (self.get_pos()[0]-closestpieceleft[0]):
                                        closestpieceleft = piece.get_pos()
                                        if piece.team == self.team:
                                            target_indexc = left.index(list((piece.get_pos()[0]*50+150,item[1])))
                                        else:
                                            target_indexc = left.index(list((piece.get_pos()[0]*50+150,item[1])))+1
            try:
                target_indexc
            except NameError:
                gg = 1
            else:
                left = left[1:target_indexc]
            counter = 0
            for item in right: #make the limits stop at units
                if counter == 0:
                    counter += 1
                    next
                else:
                    for piece in piecelist: 
                        if piece.get_pos()[1] == self.get_pos()[1]:
                            if piece.get_pos()[0] != self.get_pos()[0]:
                                if piece.get_pos()[0] > self.get_pos()[0]:
                                    if (self.get_pos()[0]-piece.get_pos()[0]) > (self.get_pos()[0]-closestpieceright[0]):
                                        closestpieceright = piece.get_pos()
                                        if piece.team == self.team:
                                            target_indexd = right.index(list((piece.get_pos()[0]*50+150,item[1])))
                                        else:
                                            target_indexd = right.index(list((piece.get_pos()[0]*50+150,item[1])))+1
            try:
                target_indexd
            except NameError:
                gg = 1
            else:
                right = right[1:target_indexd]     
                  
            for item in up:
                if (casx(item[0]),casy(item[1])) in [(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)]:
                    lakestop = up.index(list((item[0],item[1])))
                    up = up[:lakestop]
                    break
            for item in down:
                if (casx(item[0]),casy(item[1])) in [(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)]:
                    lakestop = down.index(list((item[0],item[1])))
                    down = down[:lakestop]
                    break
            for item in left:
                if (casx(item[0]),casy(item[1])) in [(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)]:
                    lakestop = left.index(list((item[0],item[1])))
                    left = left[:lakestop]
                    break
            for item in right:
                if (casx(item[0]),casy(item[1])) in [(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)]:
                    lakestop = right.index(list((item[0],item[1])))
                    right = right[:lakestop]
                    break                

            consider_limits = up+down+left+right
            good_limits = consider_limits
            
        else: # draw color over places where you can move
            lim_up = list((self.rect.centerx - 25, self.rect.centery - 50 - 25))
            lim_down = list((self.rect.centerx - 25, self.rect.centery + 50 - 25))
            lim_left = list((self.rect.centerx - 50 - 25, self.rect.centery - 25))
            lim_right = list((self.rect.centerx + 50 - 25, self.rect.centery - 25))
            
            limits = [lim_up, lim_down, lim_left, lim_right]
            good_limits = list()
            #lake squares: 4,2&4,3; 5,2&5,3; 4,6&4,7; 5,6&5,7
            
            for limit in limits:
                counter = 0
                if limit[0] >= 150 and limit[0] < 650 and limit[1] >= 100 and limit[1] < 500:
                    if (casx(limit[0]),casy(limit[1])) not in [(2,4),(3,4),(6,4),(7,4),(2,5),(3,5),(6,5),(7,5)]:
                        for piece in piecelist:
                            if piece.get_pos() == (casx(limit[0]),casy(limit[1])):
                                if piece.team != self.team:
                                    good_limits.append(limit)
                                break
                            else:
                                counter += 1
                            if counter == len(piecelist):
                                good_limits.append(limit)  
                
        return good_limits
        
    def sel(self,turn):
        if (turn == True and self.team == "red") or (turn == False and self.team == "blue"):
            pass
        else:
            self.selected = not self.selected
            # if the unit is selected
            if self.selected:
                # deselect everything but this one
                deselect_all()
                self.selected = True
                            
    def get_pos(self):
        return (casx(self.rect.centerx),casy(self.rect.centery))
    
    def get_data(self):
        return (self.team, self.level)
        
    def muerto(self):
        # remove the sprite from the game
        pass

class Text:
    def __init__(self, FontName = None, FontSize = 30):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        text = text
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size   
            
# global variables
flagcap = False
BluePlayer = 'AI'
RedPlayer = 'Human'
makesetups = False
endtime = False

previous_move_red = []
previous_move_blue = []
board_version_moves = []

chasecounterred = 0
chasecounterblue = 0

turncount = 0

#this is for when we do setup creation stuff
w, h = 8, 10;
board = [['-1' for x in range(h)] for y in range(w)] 
#thefile = open('empty.txt', 'w')

#thefile.writelines(["%s\n" % item  for item in board])

#thefile.close()

# read the configuration file
conf = configparser.ConfigParser()
if not conf.read(["conf.cfg"]):
    print("Couldn't find the config file, which is an impressive fuck up, all things considered.")
    
x_res = int(conf.get("general","width"))
y_res = int(conf.get("general","height"))
    

# auxiliary mouse variables, self explanatory
mouse_pressed = False
mouse_down = False
mouse_released = False
mouse_up = True

# True: pieceinfo selected, False, pieceinfo has not been selected
pieceinfo_sel = False

# load the board
pygame.display.set_caption(conf.get("general","name"))
screen = pygame.display.set_mode((x_res, y_res))
table = load_image(conf.get("resources","default_table"))

# True: blue team, False, red team
possibleturns=['True','False']
sys_random = random.SystemRandom()
turn = sys_random.choice(possibleturns) #who goes first is random

# initialize text so we can keep track of shifts
turn_text = Text()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Test, now in three flavors")
    text = Text()
    #Setup logic
    
    if BluePlayer == 'AI':
        BlueBot = AI_Player('blue',board) #should've taken the blue pill
    elif RedPlayer == 'AI':
        RedBot = AI_Player('blue',board) 
        
    if makesetups:
        if turn:
            #Blue setup
            setupmap = open(conf.get("resources","bluesetup"))
            pieces_map = setupmap.readlines()
            initializesetup(pieces_map)   
            
        else: 
            #red setup
            setupmap = open(conf.get("resources","redsetup"))
            pieces_map = setupmap.readlines()
            initializesetup(pieces_map)
    
    # load them in a list
    else:
        piecelist = list()
        fmap = open(conf.get("resources","default_map"))
        pieces_map = fmap.readlines()
        initializesetup(pieces_map)
    
    # game loop
    RUNNING = True
    while RUNNING == True:        
        # Events
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            RUNNING = False
            pygame.display.quit()
            pygame.quit()

        #check if the player in charge of the current turn is an AI and if not, let the human do their thing
        if turn:
            color = 'blue'
            turn_logic(color)
            if endtime:
                do_end()
        else:
            color = 'red'
            turn_logic(color)
            if endtime:
                do_end()
        # update the screen    
        draw_frame()      
        # check if the game is over, code is shitty currently
        if check_win():
            print("we made it here 3")
            do_end()
                
#pygame.quit()