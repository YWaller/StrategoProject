# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:52:17 2018

@author: ylwaller
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 12:05:19 2018

@author: Yale
"""

import os
os.chdir('C:\\Users\\ylwaller\\Desktop\\staging')

from copy import copy, deepcopy

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

import numpy as np

#e = et.parse('classic-2006.4-3649.xml')

#root = e.getroot()

#root.tag
#for child in root:
#    print child.tag, child.attrib
#root[0].tag
#for elem in e.iter():
#    print elem.tag, elem.attrib
#e.find('field')
#for elem in e.iter(tag='move'):
#   print elem.tag, elem.attrib  
   
#for elem in e.iter(tag='field'): #get the initial field
#    bb = elem.attrib
       
#gg = bb['content']

#gg = gg[::-1] #so we have the field string. Let's initialize the matrix...

#for c in gg:
#    print c

#the number in the move is the row, 1-9, with : being 10 for some ungodly reason
#the letter is the column

pd = {} #this is for pieces
pd['C'] = 1
pd['D'] = 2
pd['E'] = 3
pd['F'] = 4
pd['G'] = 5
pd['H'] = 6
pd['I'] = 7
pd['J'] = 8
pd['K'] = 9
pd['L'] = 10
pd['M'] = 0
pd['B'] = 11
pd['_'] = -1
pd['A'] = -1

pd['O'] = 21
pd['P'] = 22
pd['Q'] = 23
pd['R'] = 24
pd['S'] = 25
pd['T'] = 26
pd['U'] = 27
pd['V'] = 28
pd['W'] = 29
pd['X'] = 30
pd['Y'] = 20
pd['N'] = 31

#pass it the move, and the board.
#The move should be (source, target), and source and target should each be locations on the matrix so it can reference them
    
ld = {} 
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
#need to replicate them so we can just use ld
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

#move[0] is target, move[1] is source 
def update_board(move):
    global m1
    if ld[m1[move[0]]] == 10 and ld[m1[move[1]]] == 1: #spy
        m1[move[0]] = m1[move[1]]
        m1[move[1]] = -1
    elif ld[m1[move[0]]] == 11 and ld[m1[move[1]]] == 3: #miner
        m1[move[0]] = m1[move[1]]
        m1[move[1]] = -1
    elif ld[m1[move[0]]] < ld[m1[move[1]]]: #win
        m1[move[0]] = m1[move[1]]
        m1[move[1]] = -1    
    elif ld[m1[move[0]]] > ld[m1[move[1]]]: #lose
        m1[move[1]] = -1
    elif ld[m1[move[0]]] == ld[m1[move[1]]]: #tie
        m1[move[1]] = -1
        m1[move[0]] = -1 

bd = {} #so we can convert the move positions to their appropriate dealios
bd['A'] = 1
bd['B'] = 2
bd['C'] = 3
bd['D'] = 4
bd['E'] = 5
bd['F'] = 6
bd['G'] = 7
bd['H'] = 8
bd['I'] = 9
bd['K'] = 10

bd['1'] = 1
bd['2'] = 2
bd['3'] = 3
bd['4'] = 4
bd['5'] = 5
bd['6'] = 6
bd['7'] = 7
bd['8'] = 8
bd['9'] = 9
bd[':'] = 10

allmoves=[]
whowon=[]

from os import listdir
onlyfiles = [f for f in listdir('C:\\Users\\ylwaller\\Desktop\\staging')]

printcounter = 0
for xml in onlyfiles:
    e = et.parse(xml)
    root = e.getroot()
    for elem in e.iter(tag='result'): #get the initial field
        kk=elem.attrib
        tt = kk['type']
    if tt != '3':
        continue
    
    for elem in e.iter(tag='field'): #get the initial field
        bb = elem.attrib
           
    gg = bb['content']
    
    for elem in e.iter(tag='result'): #get the initial field
        kk=elem.attrib
        tt = kk['winner'] 
    #m1
    m1 = np.zeros((10,10)) #get the matrix all set up
    m1.fill(-1)
    m1 = m1.astype(int)
    
    #get the matrix in its proper place
    x=0
    y=0
    for c in gg:
        m1[y,x] = pd[c]
        x+=1
        if x > 9:
            x = 0
            y+=1
        if y > 9:
            y = 0
            
    #this is a simple way of attaching the winner to an equally numbered list of boards        
    if kk['winner'] == '1':
        winner = 1
    else:
        winner = 0
          
    #complete the matrix
    #allmoves=[]
    #whowon=[]
    jjjjj = 0
    for elem in e.iter(tag='move'): #go element by element and make a new matrix for it
       noy = elem.attrib
       s = noy['source']
       t = noy['target']
       pos1 = (bd[s[1]]-1,bd[s[0]]-1)
       pos2 = (bd[t[1]]-1,bd[t[0]]-1)
       move = (pos2, pos1)
       update_board(move)
       m2 = copy(m1)
       allmoves.append(m2)
       whowon.append(winner)
   
    
os.chdir('C:\\Users\\ylwaller\\Desktop')

#import csv
#with open("stratdata.csv","wb") as f:
#    writer = csv.writer(f)
#    writer.writerows(allmoves)


#with open("stratvictor.csv","w") as f:
#    writer = csv.writer(f)
#    writer.writerows([whowon])

#wing = []
#with open("stratvictor.csv", 'rb') as f:
#    reader = csv.reader(f)
#    for row in reader:
#        wing.append(row)

#wing=wing[0]
#wing = map(int, wing)









