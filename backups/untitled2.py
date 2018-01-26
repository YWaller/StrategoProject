# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 19:25:06 2017

@author: Yale
"""
import re



w, h = 8, 10;
board = [[-1 for x in range(h)] for y in range(w)]

thefile = open('empty.txt', 'w')

thefile.writelines(["%s\n" % item  for item in board])

thefile.close()

number=[]

aux=[]

piecelist = list()

f = open('testtest.txt')

for line in f:
    y+=1
    number.append(line.split())

for i in range(len(number)):
    for j in range(len(number[i])):
        board[i][j] = number[i][j]
        if "r" in number[i][j]:
            inter=re.search('\d+',number[i][j])
            rank=inter.group()
            aux=["red"]+[int(rank)]+[i]+[j]
            piecelist.append(aux)
        elif "b" in number[i][j]:
            inter=re.search('\d+',number[i][j])
            rank=inter.group()
            aux=["blue"]+[int(rank)]+[i]+[j]
            piecelist.append(aux)

'''
for piece in pieces_map:
    if piece != "\n":
        aux = piece.split()
        if int(aux[2]) > 3:
            aux = ["red"] + aux
            piecelist.append(pieceinfo(aux[0],int(aux[1]),int(aux[2]),int(aux[3])))
        else:
            aux = ["blue"] + aux
            piecelist.append(pieceinfo(aux[0],int(aux[1]),int(aux[2]),int(aux[3])))
'''

#for updating board, do something like "make empty list and put all found elements in it with rankteam and fill all empty spots with -1


