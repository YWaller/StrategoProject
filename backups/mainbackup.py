# Clon de Stratego para python
import ConfigParser
import sys, time, pygame
from pygame.locals import *


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
	for zeta in record:
		if (casx(mousepos[0]),casy(mousepos[1])) == zeta.get_pos():
			return zeta

def check_move(mousepos):
	for zeta in record:
        # If there is a selected unit, check if it can move
        #show all possible moves
		if zeta.selected:
			moves = zeta.show_moves()
			for move in moves:
				if (casx(mousepos[0]),casy(mousepos[1])) == (casx(move[0]),casy(move[1])):
					return move
			break
			
def deselect_all():
	for zeta in record:
		zeta.selected = False;

def choose_selected():
	for zeta in record:
		if zeta.selected:
			return zeta
			
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
	
def destroy_unit(unit):
	record.remove(unit)
	
def check_win():
	red = False
	blue = False
	text = Text()
	
	for unit in record:
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
		print "red wins"
		text.render(screen, "red wins",  (255,0,0), (10, 10))
		pygame.display.flip()
		return True
	else:
		print "tie"
		text.render(screen, "tie",  (255,0,0), (10, 10))
		pygame.display.flip()
		return True

def do_end():
	pygame.time.wait(3000)
	sys.exit(0)
		
		
def draw_frame():
# show the board
	screen.blit(table, (0, 0))
	
	# record the board
	for zeta in record:
		screen.blit(zeta.image,zeta.rect)
		if zeta.selected:
			moves = zeta.show_moves()
			for point in moves:
				img_shadow = load_image("./resources/imgs/"+zeta.get_data()[0]+"/shadow.png")
				screen.blit(img_shadow,point)
				
	# show text
	if turn:
		turn_text.render(screen, "Blue's turn",  (0,0,255), (10, 30))
	else:
		turn_text.render(screen, "Red's turn",  (255,0,0), (10, 30))
		
	pygame.display.flip()
	
class mfile(pygame.sprite.Sprite):
	def __init__(self,objects,level,cox,coy):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("./resources/imgs/"+str(objects)+"/"+str(level)+".png", False)
		self.rect = self.image.get_rect()
		self.rect.centerx = coordx(cox)
		self.rect.centery = coordy(coy)
		self.team = objects
		self.level = level
		self.selected = False
		
	def mover(self,cox,coy):
		self.rect.centerx = coordx(cox)
		self.rect.centery = coordy(coy)
		
	def show_moves(self):
		# draw color over places where you can move
		lim_up = (self.rect.centerx - 25, self.rect.centery - 50 - 25)
		lim_down = (self.rect.centerx - 25, self.rect.centery + 50 - 25)
		lim_left = (self.rect.centerx - 50 - 25, self.rect.centery - 25)
		lim_right = (self.rect.centerx + 50 - 25, self.rect.centery - 25)
		
		limits = [lim_up, lim_down, lim_left, lim_right]
		good_limits = list()
		
		for limit in limits:
			counter = 0
			if limit[0] >= 150 and limit[0] < 650 and limit[1] >= 50 and limit [1] < 550:
				for zeta in record:
					if zeta.get_pos() == (casx(limit[0]),casy(limit[1])):
						if zeta.team != self.team:
							good_limits.append(limit)
						break
					else:
						counter += 1
					if counter == len(record):
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

# True: mfile selected, False, mfile has not been selected
mfile_sel = False

# load the board
pygame.display.set_caption(conf.get("general","name"))
screen = pygame.display.set_mode((x_res, y_res))
table = load_image(conf.get("resources","default_table"))

# True: blue team, False, red team
turn = True

# initialize text so we can keep track of shifts
turn_text = Text()

# load them in a list
record = list()
fmap = file(conf.get("resources","default_map"))
zetas_map = fmap.readlines()

for zeta in zetas_map:
	if zeta != "\n":
		aux = zeta.split()
		record.append(mfile(aux[0],int(aux[1]),int(aux[2]),int(aux[3])))



if __name__ == "__main__":
	pygame.init()
	pygame.display.set_caption("Test")
	
	# game loop
	while True:		
		# Events
		event = pygame.event.poll()
		#~ pygame.event.pump()

		# Provisional: a piece was moved
		keys = pygame.key.get_pressed()
		
		if keys[K_SPACE]:
			turn = next_turn(turn)
			print "turno",turn					
		
		# update mouse position
		mouse_pressed,mouse_down,mouse_released,mouse_up = update_mouse(mouse_pressed,mouse_down,mouse_released,mouse_up)

		# select an mfile object if selected by the mouse
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
				# si hay un enemigo, atacamos
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
				
