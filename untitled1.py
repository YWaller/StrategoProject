# -*- coding: utf-8 -*-
"""
Created on Tue Jan 02 21:50:08 2018

@author: Yale
"""

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

	def ReadBoard(self):
		#Reads in the board. 
		#On the first turn, sets up the self.board structure
		#On subsequent turns, the board is simply read, but the self.board structure is not updated here.
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
    '''   