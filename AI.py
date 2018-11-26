# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 21:52:40 2017

@author: Yale
"""

class AI:
      #random AI
		#Override method "MakeMove" for more complex moves
        
	def __init__(self):	
		#Constructs the BasicAI agent, and starts it playing the game
		self.turn = 0
		self.board = []
		self.units = []
		self.enemyUnits = []

		self.totalAllies = {'11':6,'10':1,'9':1,'8':2,'7':3,'6':4,'5':4,'4':4,'3':5,'2':8,'1':1,'0':1}
		self.totalEnemies = {'11':6,'10':1,'9':1,'8':2,'7':3,'6':4,'5':4,'4':4,'3':5,'2':8,'1':1,'0':1}
		self.hiddenEnemies = {'11':6,'10':1,'9':1,'8':2,'7':3,'6':4,'5':4,'4':4,'3':5,'2':8,'1':1,'0':1}
		self.hiddenAllies = {'11':6,'10':1,'9':1,'8':2,'7':3,'6':4,'5':4,'4':4,'3':5,'2':8,'1':1,'0':1}
		self.lastMoved = None

		
'''
	def Setup(self):
		""" Implements Setup part of protocol. Always uses the same setup. Override to create custom setups """
		#sys.stderr.write("BasicAI Setup here...\n");
		setup = sys.stdin.readline().split(' ')
		if len(setup) != 4:
			sys.stderr.write("BasicAI setup fails, expected 4 tokens, got " + str(len(setup)) + " "+str(setup) + "\n")
		self.colour = setup[0]
		self.opponentName = setup[1]
		self.width = int(setup[2])
		self.height = int(setup[3])
		for x in range(0, self.width):
			self.board.append([])
			for y in range(0, self.height):		
				self.board[x].append(None)
		if self.colour == "RED":
			print "FB8sB479B8\nBB31555583\n6724898974\n967B669999"
		elif self.colour == "BLUE":
			print "967B669999\n6724898974\nBB31555583\nFB8sB479B8"
		return True
'''
	def MoveCycle(self):
		#BasicAI MakeMove here...
		if self.InterpretResult() == False or self.ReadBoard() == False or self.MakeMove() == False:
			return False
		self.turn += 1
		return self.InterpretResult()

	def MakeMove(self):
		#Randomly moves any moveable piece, or prints "NO_MOVE" if there are none
		#TODO: Over-ride this function in base classes with more complex move behavior

		if len(self.units) <= 0:
			return False

		index = random.randint(0, len(self.units)-1)
		startIndex = index

		directions = ("UP", "DOWN", "LEFT", "RIGHT")
		while True:
			piece = self.units[index]
			if piece != None and piece.mobile():
				dirIndex = random.randint(0, len(directions)-1)
				startDirIndex = dirIndex
				
				while True:
					#sys.stderr.write("Trying index " + str(dirIndex) + "\n")
					p = move(piece.x, piece.y, directions[dirIndex],1)
					if p[0] >= 0 and p[0] < self.width and p[1] >= 0 and p[1] < self.height:
						target = self.board[p[0]][p[1]]
						if target == None or (target.colour != piece.colour and target.colour != "NONE" and target.colour != "BOTH"):	
							print str(piece.x) + " " + str(piece.y) + " "+directions[dirIndex]
							return True
					dirIndex = (dirIndex + 1) % len(directions)
					if startDirIndex == dirIndex:
						break

			index = (index + 1) % len(self.units)
			if startIndex == index:
				print "NO_MOVE"
				return True
							
			
	def ReadBoard(self):
		""" Reads in the board. 
			On the very first turn, sets up the self.board structure
			On subsequent turns, the board is simply read, but the self.board structure is not updated here.
		"""
		#sys.stderr.write("BasicAI ReadBoard here...\n");
		for y in range(0,self.height):
			row = sys.stdin.readline().strip()
			if len(row) < self.width:
				sys.stderr.write("Row has length " + str(len(row)) + " vs " + str(self.width) + "\n")
				return False
			for x in range(0,self.width):
				if self.turn == 0:
					if row[x] == '.':
						pass
					elif row[x] == '#':
						self.board[x][y] = Piece(oppositeColour(self.colour), '?',x,y)
						self.enemyUnits.append(self.board[x][y])
					elif row[x] == '+':
						self.board[x][y] = Piece("NONE", '+', x, y)
					else:
						self.board[x][y] = Piece(self.colour, row[x],x,y)
						self.units.append(self.board[x][y])
				else:
					pass
		return True
		

	def InterpretResult(self):
		""" Interprets the result of a move, and updates the board. 
			The very first move is ignored. 
			On subsequent moves, the self.board structure is updated
		"""
		#sys.stderr.write("BasicAI InterpretResult here...\n")
		result = sys.stdin.readline().split(' ')
		#sys.stderr.write("	Read status line \"" + str(result) + "\"\n")
		if self.turn == 0:
			return True

		if result[0].strip() == "QUIT": #Make sure we exit when the manager tells us to!
			return False

		if result[0].strip() == "NO_MOVE": #No move was made, don't need to update anything
			return True

		if len(result) < 4: #Should be at least 4 tokens (X Y DIRECTION OUTCOME) in any other case
			return False

		x = int(result[0].strip())
		y = int(result[1].strip())


		#sys.stderr.write("	Board position " + str(x) + " " + str(y) + " is OK!\n")		

		direction = result[2].strip()

		multiplier = 1
		outcome = result[3].strip()
		outIndex = 3
		if is_integer(outcome):
			multiplier = int(outcome)
			outcome = result[4].strip()
			outIndex = 4
		
		p = move(x,y,direction, multiplier)

		#Determine attacking piece
		attacker = self.board[x][y]
		self.board[x][y] = None

		if attacker == None:
			return False

		lastMoved = attacker

		defender = self.board[p[0]][p[1]]

		#Update attacker's position (Don't overwrite the board yet though)

		attacker.x = p[0]
		attacker.y = p[1]
		attacker.positions.insert(0, (attacker.x, attacker.y))

		
		#Determine ranks of pieces if supplied
		if len(result) >= outIndex + 3:
			if defender == None:
				return False
			attacker.rank = result[outIndex+1].strip()
			if attacker.beenRevealed == False:
				if attacker.colour == self.colour:
					self.hiddenAllies[attacker.rank] -= 1
				elif attacker.colour == oppositeColour(self.colour):
					self.hiddenEnemies[attacker.rank] -= 1
			attacker.beenRevealed = True
			defender.rank = result[outIndex+2].strip()
			if defender.beenRevealed == False:
				if defender.colour == self.colour:
					self.hiddenAllies[defender.rank] -= 1
				elif defender.colour == oppositeColour(self.colour):
					self.hiddenEnemies[defender.rank] -= 1

			defender.beenRevealed = True

			
		
		if outcome == "OK":
			self.board[p[0]][p[1]] = attacker
			
		elif outcome == "KILLS":
			self.board[p[0]][p[1]] = attacker

			if defender.colour == self.colour:
				self.totalAllies[defender.rank] -= 1
				self.units.remove(defender)
			elif defender.colour == oppositeColour(self.colour):
				self.totalEnemies[defender.rank] -= 1
				self.enemyUnits.remove(defender)
	
		elif outcome == "DIES":
			if attacker.colour == self.colour:
				self.totalAllies[attacker.rank] -= 1
				self.units.remove(attacker)
			elif attacker.colour == oppositeColour(self.colour):
				self.totalEnemies[attacker.rank] -= 1
				self.enemyUnits.remove(attacker)

		elif outcome == "BOTHDIE":
			self.board[p[0]][p[1]] = None

			if defender.colour == self.colour:
				self.totalAllies[defender.rank] -= 1
				self.units.remove(defender)
			elif defender.colour == oppositeColour(self.colour):
				self.totalEnemies[defender.rank] -= 1
				self.enemyUnits.remove(defender)

			if attacker.colour == self.colour:
				self.totalAllies[attacker.rank] -= 1
				self.units.remove(attacker)
			elif attacker.colour == oppositeColour(self.colour):
				self.totalEnemies[attacker.rank] -= 1
				self.enemyUnits.remove(attacker)

		elif outcome == "FLAG":
			#sys.stderr.write("	Game over!\n")
			return False
		elif outcome == "ILLEGAL":
			#sys.stderr.write("	Illegal move!\n")
			return False
		else:
			#sys.stderr.write("	Don't understand outcome \"" + outcome + "\"!\n");
			return False

		#sys.stderr.write("	Completed interpreting move!\n");		
		return True