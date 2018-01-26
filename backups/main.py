import ConfigParser
import sys, time, pygame
from pygame.locals import *
#from SAI import *

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
    except pygame.error, message:
            raise SystemExit, message
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
        unit = choose_selected()
        unit.rect.centerx = coordx(casx(mousepos[0]))
        unit.rect.centery = coordy(casy(mousepos[1]))
    
def do_attack(attacked):
    attacker = choose_selected()
    # spy
    if attacked.level == 10 and attacker.level == 1:
        do_move((attacked.rect.centerx,attacked.rect.centery))
        destroy_unit(attacked)
        print "spy wins"
        return 1
    # miner
    if attacked.level == 11 and attacker.level == 3:
        do_move((attacked.rect.centerx,attacked.rect.centery))
        print "miner wins"
        destroy_unit(attacked)
        return 1
    elif attacked.level < attacker.level:
        do_move((attacked.rect.centerx,attacked.rect.centery))
        print "attacker wins"
        destroy_unit(attacked)
        return 1
    elif attacked.level > attacker.level:
        print "defender wins"
        destroy_unit(attacker)
        return -1
    elif attacked.level == attacker.level:
        print "tie"
        destroy_unit(attacker)
        destroy_unit(attacked)
        return 0
    elif attacked.level == 0:
        flagcap = True
        loserteam = self.team
        #get their team and set it to a variable
    
def destroy_unit(unit):
    piecelist.remove(unit)
    
def check_win():
    if flagcap:
        if loserteam == blue:
            print "Red wins"
            return True
        elif loserteam == red:
            print "Blue wins"
            return True
        
    red = False
    blue = False
    text = Text()
    
    for unit in piecelist:
        if unit.team == "blue":
            blue = True
        else:
            red = True
    
    if red and blue:
        return False
    elif red and not blue:
        print "red wins"
        text.render(screen, "red wins", (255,0,0), (10, 10))
        pygame.display.flip()
        return True
    elif blue and not red:
        print "blue wins"
        text.render(screen, "blue wins",  (0,0,255), (10, 10))
        pygame.display.flip()
        return True
    else:
        print "tie"
        text.render(screen, "tie",  (255,0,0), (10, 10))
        pygame.display.flip()
        return True

def do_end():
    pygame.time.wait(3)
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
                piece.image = load_image("./resources/imgs/red/"+"hidden.png", False)
            else:
                piece.image = load_image("./resources/imgs/blue/"+str(piece.level)+".png", False)
    else:
        turn_text.render(screen, "Red's turn",  (255,0,0), (10, 30))
        for piece in piecelist:
            currentteam = 'red'
            if piece.team != currentteam:
                piece.image = load_image("./resources/imgs/blue/"+"hidden.png", False)
            else:
                piece.image = load_image("./resources/imgs/red/"+str(piece.level)+".png", False)
        
    pygame.display.flip()
    
class pieceinfo(pygame.sprite.Sprite):
    def __init__(self,giventeam,level,cox,coy):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("./resources/imgs/"+str(giventeam)+"/"+str(level)+".png", False)
        self.rect = self.image.get_rect()
        self.rect.centerx = coordx(cox)
        self.rect.centery = coordy(coy)
        self.team = giventeam
        self.level = level
        self.selected = False
        
    def mover(self,cox,coy):
        self.rect.centerx = coordx(cox)
        self.rect.centery = coordy(coy)
        
        
    def show_moves(self):
        if self.level == 11 or 0:
            # bombs and flags can't move
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
            lim_up = (self.rect.centerx - 25, self.rect.centery - 50 - 25)
            lim_down = (self.rect.centerx - 25, self.rect.centery + 50 - 25)
            lim_left = (self.rect.centerx - 50 - 25, self.rect.centery - 25)
            lim_right = (self.rect.centerx + 50 - 25, self.rect.centery - 25)
            
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
        text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size   
            
# global variables
flagcap = False
BluePlayer = 'AI'
RedPlayer = 'Human'

# read the configuration file
conf = ConfigParser.ConfigParser()
if not conf.read(["conf.cfg"]):
    print "Couldn't find the config file, which is an impressive fuck up, all things considered."
    
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
turn = True

# initialize text so we can keep track of shifts
turn_text = Text()

# load them in a list
piecelist = list()
fmap = file(conf.get("resources","default_map"))
pieces_map = fmap.readlines()

for piece in pieces_map:
    if piece != "\n":
        aux = piece.split()
        piecelist.append(pieceinfo(aux[0],int(aux[1]),int(aux[2]),int(aux[3])))



if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Test")
    
    # game loop
    RUNNING = True
    while RUNNING == True:        
        # Events
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            RUNNING = False

        # update mouse position
        mouse_pressed,mouse_down,mouse_released,mouse_up = update_mouse(mouse_pressed,mouse_down,mouse_released,mouse_up)

        # select an pieceinfo object if selected by the mouse
        if mouse_pressed:
            mousepos = pygame.mouse.get_pos()
            unit = check_unit(mousepos)
            move = check_move(mousepos)
            # if there are other units on this team, deselect them
            if unit and ((unit.team == "blue" and turn) or (unit.team == "red" and not turn)):
                shadow_points = unit.sel(turn)
                # if selected, show movement options
                if unit.selected:
                    print "selected unit"
                else:
                    print "unit deselected"
            elif move:
                print "move initiated"
                # if no one is in the box, move there
                if not unit:
                    print "actually moved"
                    do_move(mousepos)
                    turn = next_turn(turn)
                # if an enemy unit is there, run attack logic
                else:
                    print "attack"
                    do_attack(unit)
                    turn = next_turn(turn)
            else:
                print "nothing was done"
                print move
            
                        
        # update the screen    
        draw_frame()
        
        # check if the game is over, code is shitty currently
        if check_win():
            do_end()
        
        # give the computer some time, just in case...
        pygame.time.wait(30)
                
pygame.quit()