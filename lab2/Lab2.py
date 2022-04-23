import random
import os
import lab
import sys
import pickle
import unittest
N = random.randint(5, 10)
k = random.randint(4, 7)
def random_number_list(L, i=1):
    o = list(range(i*100000, i*100000+L))
    random.shuffle(o)
    return o
def make_bacon_tree(L, n=10):
    id_set = 2
    path = [4724] + random_number_list(L, i=1)
    n -= 1
    out = set((i,j) for i,j in zip(path, path[1:]))
    while n > 0:
        point = random.choice(range(len(path)-1))
        d = L - point
        if d == 0:
            continue
        newpath = random_number_list(d, i=id_set)
        p = [path[point]] + newpath
        out |= set((i,j) for i,j in zip(p, p[1:]))
        id_set += 1
        n -= 1
    return [(i, j, 0) for i,j in out]
def dictionarify(data):
    actor_book={}
    for i in range(len(data)):
        if data[i][0] not in actor_book:
            actor_book[data[i][0]]=set()
        if data[i][1] not in actor_book:
            actor_book[data[i][1]]=set()
        actor_book[data[i][0]].add(data[i][1])
        actor_book[data[i][1]].add(data[i][0])
    return actor_book
print(dictionarify(make_bacon_tree(N, k)))
