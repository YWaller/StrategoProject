# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:16:26 2018

@author: ylwaller
"""

from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))