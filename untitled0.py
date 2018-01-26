# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 20:58:43 2018

@author: Yale
"""

hh=[1,2,2,2,11,0]
cnt=0
for item in hh:
    if item not in [11,0] and type(item) == int:
        cnt+=1

print cnt