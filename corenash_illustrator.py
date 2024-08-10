import tcfginitialize as tcfg
import kTierList as ktl
import ktcfghelper as helper
import csv
from itertools import permutations



n = 10
ks = [2,3,4,5,6,7,8,9,10]
opt = [0,0,15,22,24,26,27,28,29,30]
Ta = [*range(n)]

Win = [[0, -1, -1, 1, -1, 1, 1, -1, -1, 1], [1, 0, -1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1, -1, -1, 1, -1], [-1, -1, -1, 0, -1, -1, -1, -1, 1, 1], [1, -1, -1, 1, 0, -1, -1, -1, -1, 1], [-1, -1, -1, 1, 1, 0, -1, 1, -1, 1], [-1, -1, 1, 1, 1, 1, 0, 1, -1, 1], [1, -1, 1, 1, 1, -1, -1, 0, -1, 1], [1, -1, -1, -1, 1, 1, 1, 1, 0, -1], [-1, -1, 1, -1, -1, -1, -1, -1, 1, 0]]

for k in ks:
    totacount = 0
    corecount = 0
    nashcount = 0
    bothcount = 0

    nashmin = 100
    nashmax = -100
    coremin = 100
    coremax = -100
    totamax = -100
    

    #result = set()

    sorts = helper.sorted_k_partitions(Ta, k)
    for s in sorts:
        go = True
        for x in range(len(s)):
            if len(s[x]) == 0:
                go = False
        if go:
            Tk = []
            for x in range(k):
                Tk.append(list(s[x]))
            if len(Tk) == k:
                perms = list(permutations(Tk))
                for p in perms:
                    totacount += 1
                    r1,r2,r3 = ktl.isCoreStable(list(p), Win, n, k)
                    #r1, r2 = ktl.isCoreAndNash(list(p), Win, n, k)
                    u = ktl.utility(list(p), Win)
                    if u == opt[k]:
                        print(r1)
##                    if r1:
##                        corecount += 1
##                        if u < coremin:
##                            coremin = u
##                        if u > coremax:
##                            coremax = u
##                    if r2:
##                        nashcount += 1
##                        print(p)
##                        if u < nashmin:
##                            nashmin = u
##                        if u > nashmax:
##                            nashmax = u
##                    if r1 and r2:
##                        bothcount += 1
##                    if u > totamax:
##                        totamax = u

##    print(k, totacount, corecount, nashcount, bothcount)
##    print(k, nashmin, nashmax, coremin, coremax, totamax)
    print(".")

