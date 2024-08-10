from random import choice
from itertools import product, combinations
import ktcfghelper as helper

#helper function that takes two integers and returns a range from lesser to greater inclusive
def okrange(c, t):
    if (c < t):
        return range(c, t+1)
    else:
        return range(t, c+1)

#helper function that unlists a list of the form list[list, numeric]
def flatten(l):
  out = []
  out.extend(l[0])
  out.append(l[1])
  return out

#computes the utility of a k-tier list
def utility(T, Win, k = 1):
    u = 0
    k = len(T)
    for i in range(k):
        for j in range(len(T[i])):
            for r in range(i+1):
                for s in range(len(T[r])):
                    u = u + Win[T[i][j]][T[r][s]]

    return u


#computes the fun of a k-tier list
def fun(T, k = 1):
    f = 0
    k = len(T)
    for i in range(k):
        if len(T[i]) > 1:
            f = f+1

    return f/k


#Computes the robustness of a k-tier list
def robustness(T, Win):
    r = 0
    k = len(T)
    for i in range(k):
        for j in range(len(T[i])):
            x = 0
            for l in range(len(T[i])):
                x = x + Win[T[i][j]][T[i][l]]
            r = min(r, x)
    return r


#Computes the cost matrix for upward merging
def UpwardMergeCost(T, Win, n):
    Cost = [[0 for i in range(n)] for j in range(n)]
    for i in range(n-1):
        c = 0
        for j in range(1, n):
            c = c + Win[T[i]][T[j]]
            Cost[i][j] = c
    return Cost

#Computes the highest utility order-preserving k-tier list on an instance
def kTierList(Cost, n, k):
    U = [[[float('-inf') for i in range(k)] for j in range(n)] for m in range(n)]
    V = [[[[] for i in range(k)] for j in range(n)] for m in range(n)]

    for i in range(n):
        for j in range(i, n):
            s = 0
            for m in range(i, j+1):
                s = s + Cost[m][j]
            U[i][j][0] = s
            V[i][j][0].append(j)


    for r in range(1, k):
        for i in range(n-r):
            for j in range(i+r, n):
                for m in range(i+r-1, j):
                    mu = U[i][m][r-1] + U[m+1][j][0]
                    if (mu > U[i][j][r]):
                        U[i][j][r] = mu
                        V[i][j][r] = flatten([V[i][m][r-1], j])

    return U[0][n-1][k-1], V[0][n-1][k-1]


#Perform local search on a k tier list to find the best 
def kLocalSearch(T, Win, n, k):
    n2 = n**2
    d = 0
    go = True
    
    while go:
        umax = [-1*n for j in range(n)]
        pmax = [-1 for j in range(n)]
        pcurr = [-1 for j in range(n)]
        ucurr = [-1 for j in range(n)]
        changes = []
        #perform the search itself
        for i in range(k):
            for j in range(len(T[i])):
                #find current and maximum position for an agent
                ulist = [-1 for r in range(k)]
                a = T[i][j]
                u = 0
                pcurr[a] = i
                for r in range(k):
                    #find the utility of a at tier r
                    for s in range(len(T[r])):
                        u = u + Win[a][T[r][s]]
                    #adjust max, where tier i wins all ties
                    ulist[r] = u
                    if (r == i):
                        ucurr[a] = u
                    if (u > umax[a] or (u == umax[a] and r == i)):
                        umax[a] = u
                        pmax[a] = r

                #if the agent wants to move, determine if the move is valid
                um = max(ulist)
                while um > ucurr[a]:
                    pm = ulist.index(um)
                    li = len(T[i])
                    if (i < pm):
#                        if li == 1:
#                            pm += 1
                        uleave = 0
                        for r in range(i, pm):
                            for s in range(len(T[r])):
                                uleave = uleave + Win[T[r][s]][a]
                        if (uleave <= 0):
                            changes.append([a, li])
                            umax[a] = um
                            pmax[a] = pm
                            um = -1 * n
                    elif (i > pm):
                        if li == 1:
                            pm += 1
                        if pm != i:
                            uarrive = 0
                            for r in range(pm, i):
                                for s in range(len(T[r])):
                                    uarrive = uarrive + Win[T[r][s]][a]
                            if (uarrive >= 0):
                                changes.append([a, li])
                                umax[a] = um
                                pmax[a] = pm
                                um = -1 * n
                    if um > (-1 * n):
                        ulist[pm] = -1*n
                        um = max(ulist)


        #if no agents have a valid and desired move, the search is done
        if (len(changes) == 0):
            go = False
        else:
            #increment number of changes
            d = d + 1
            #if the number of changes exceeds n**2, something very bad has happened
            if (d == n2+1):
                print("Uh oh spagghettios")
                print(Win)
                raise SystemExit(0)
            Td = T
            #Move agents. That is, move the first agent, and any subsequent agents whose
            #     utility is not affected by previous moves
            ok = [0 for i in range(k)]
##            for a in changes:
##                curr = pcurr[a]
##                targ = pmax[a]
##                if (ok[curr] == 0 and ok[targ] == 0):
##                    #move the agent
##                    Td[curr].remove(a)
##                    Td[targ].append(a)
##                    #update ok
##                    for j in okrange(curr, targ):
##                        ok[j] = 1
            while len(changes) > 0:
                ali = choice(changes)
                a = ali[0]
                li = ali[1]
                curr = pcurr[a]
                targ = pmax[a]
                try:
                    if (ok[curr] == 0 and ok[targ] == 0):
                        if li > 1:
                            Td[curr].remove(a)
                            Td[targ].append(a)
                        elif li == 1:
                            t = Td.pop(curr)
                            Td.insert(targ, t)
                            #####
                            #d = -1 * n2
                            #####
                        for j in okrange(curr, targ):
                            ok[j] = 1
                except IndexError:
                    print(curr, targ, k)
                    raise SystemExit(0)
                changes.remove(ali)
            
            #update T to new version
            T = Td
    return T, d                


#manages local search repeated several times
def kLocalSearchCaller(T, Win, n, k):
    Tk, d = kLocalSearch(T, Win, n, k)
    umax = utility(Tk, Win, k)
    #take these out later
    ulist = [umax]
    ########
    for j in range(r-1):
        TkA, dA = kLocalSearch(Tk, Win, n, k)
        ucurr = utility(TkA, Win, k)
        if (ucurr > umax):
            Tk = TkA
            d = dA
            umax = ucurr
        ########
        ulist.append(ucurr)
        ########
        
    ########
    if (umax != ulist[0]):
        print(k, i, y)
        print("First:", ulist[0])
        print("Max:", umax)
        print("Average:", sum(ulist)/r)
        print("")
    ########
    
    return Tk, d


#finds a socially consciously stable k tier list
#Input: T (Siler's stable tier list), Win (matchup matrix),
#       n (number of agents), k (number of desired tiers)
def kStableTierList(T, Win, n, k, r=1, x=0, y=''):
    Cost = UpwardMergeCost(T, Win, n)
    U, V = kTierList(Cost, n, k)
    #perform merges according to the values stored at V
    Tk = []
    low = 0
    for i in range(k):
        high = V[i]+1
        Tk.append(T[low:high])
        low = high

    Tk, d = kLocalSearch(Tk, Win, n, k)
    
    return Tk, d



#Performs the new epsilon local search
def eLocalSearch(T, Win, n, e):
    n2 = n**2
    d = 0
    go = True
    
    while go:
        d += 1
        changes = 0
        #perform the search itself
        for i in range(len(T)):
            #flag for if iteration needs to stop
            quiti = False
            for j in reversed(range(len(T[i]))):
                #find current and maximum position for an agent
                a = T[i][j]
                ulist = []
                flist = []
                u = 0
                for r in range(len(T)):
                    f = 0
                    #find the utility of a at tier r
                    for s in range(len(T[r])):
                        f = f + Win[a][T[r][s]]
                    #add fitness to list
                    flist.append(f)
                    #update utility
                    u = u + f
                    ulist.append(u)

                umax = max(ulist)
                targ = ulist[i] + e
                if umax < 0:
                    T.insert(0, [a])
                    umax = -1*n
                    quiti = True
                    changes = changes + 1
                #if the agent wants to move, determine if the move is valid
                ulist2 = []
                for u in ulist:
                    ulist2.append(u)
                moved = False
                while umax > targ:
                    pmax = ulist.index(umax)
                    if (i < pmax):
                        #the agent is trying to move up.
                        uleave = 0
                        for r in range(i, pmax):
                            uleave = uleave + flist[r]
                        #if it can move to the existing tier
                        if uleave >= 0:
                            T[i].remove(a)
                            T[pmax].append(a)
                            moved = True
                    elif (i > pmax):
                        #the agent is trying to move down.
                        uleave = 0
                        for r in range(pmax, i):
                            uleave = uleave - flist[r]
                        #if it can move to the existing tier
                        if uleave >= 0:
                            T[i].remove(a)
                            T[pmax].append(a)
                            moved = True
                    if moved:
                        umax = -1*n
                        changes = changes+1
                    else:
                        ulist[pmax] = -1*n
                        umax = max(ulist)
                if not moved and not quiti:
                    umax = max(ulist2)
                    while umax > targ:
                        pmax = ulist2.index(umax)
                        if (i < pmax):
                            #the agent is trying to move up
                            uleave = 0
                            for r in range(i, pmax+1):
                                uleave = uleave + flist[r]
                            #if it can move to the tier above
                            if uleave >= 0:
                                T[i].remove(a)
                                T.insert(pmax+1, [a])
                                moved = True
                        elif (i > pmax):
                            #the agent is trying to move down
                            uleave = 0
                            for r in range(pmax+1, i):
                                uleave = uleave - flist[r]
                            #if it can move to the tier above
                            if uleave >= 0:
                                T[i].remove(a)
                                T.insert(pmax+1, [a])
                                i = i+1
                                quiti = True
                                moved = True
                        if moved:
                            umax = -1*n
                            changes = changes+1
                        else:
                            ulist2[pmax] = -1*n
                            umax = max(ulist2)
                if quiti:
                    break
            if quiti:
                break
        #if no agents have moved, the search is done
        if (changes == 0):
            go = False
        
    return T, d





#finds an epsilon stable tier list based on a k tier list
#Input: T (Siler's stable tier list), Win (matchup matrix),
#       n (number of agents), k (number of desired tiers), e (epsilon)
def eStableTierList(T, Win, n, k, e):
    Cost = UpwardMergeCost(T, Win, n)
    U, V = kTierList(Cost, n, k)
    #perform merges according to the values stored at V
    Tk = []
    low = 0
    for i in range(k):
        high = V[i]+1
        Tk.append(T[low:high])
        low = high

    Tk, d = eLocalSearch(Tk, Win, n, e)
    Tkf = [ele for ele in Tk if ele != []]
    
    return Tkf, d


#Does the coalition weakly block under these conditions?
#Input: C (Coalition attempting to block)
#       Seen (a possible set of seen agents)
#       Win (a Win matrix)
def weakBlockIfSeen(C, Seen, Win, utility):
    atLeastOneLikes = False
    for i in C:
        u = 0
        for j in Seen:
            u += Win[i][j]
        if u < utility[i]:
            return False
        elif u > utility[i]:
            atLeastOneLikes = True
    return atLeastOneLikes


#Does the coalition strongly block under these conditions?
#Input: C (Coalition attempting to block)
#       Seen (a possible set of seen agents)
#       Win (a Win matrix)
def strongBlockIfSeen(C, Seen, Win, utility):
    for i in C:
        u = 0
        for j in Seen:
            u += Win[i][j]
        if u <= utility[i]:
            return False
    return True



#finds whether a k tier list is strictly core stable
def isStrictCoreStable(T, Win, n, k):
    utility = [0 for i in range(n)]
    Subsets = []
    stesbuS = []
    for i in range(k):
        subset = []
        tesbus = 0
        for j in range(len(T[i])):
            #Get all strict subsets of each tier
            for s in combinations(T[i], j):
                subset.append(list(s))
                tesbus += 1
            #get each agent's current utility
            u = 0
            for r in range(i+1):
                for s in range(len(T[r])):
                    u = u + Win[T[i][j]][T[r][s]]
            utility[T[i][j]] = u
        Subsets.append(subset)
        stesbuS.append(range(tesbus))
    #
    for i in range(k):
        stesbuS_i = []
        AlreadySeen = []
        for j in range(i+1):
            AlreadySeen.extend(T[j])
        for j in range(k):
            if j == i:
                stesbuS_i.append([0])
            else:
                stesbuS_i.append(stesbuS[j])
        for picks in product(*stesbuS_i):
            #Form each blocking coalition
            C = []
            C.extend(T[i])
            for j in range(k):
                C.extend(Subsets[j][picks[j]])
            #find each utility of each agent at each level
            Seen = []
            Seen.extend(C)
            if set(AlreadySeen) != set(Seen):
                if weakBlockIfSeen(C, Seen, Win, utility):
                    #the tier blocks by moving to tier 1
                    return False, C, 0
            for j in range(k):
                changed = False
                for a in T[j]:
                    if a not in Seen:
                        changed = True
                        Seen.append(a)
                if changed:
                    if set(AlreadySeen) != set(Seen):
                        if weakBlockIfSeen(C, Seen, Win, utility):
                            return False, C, j+1
    #If we got this far, there are no blocking coalitions
    return True, -1, -1    
    #for each tier, iterate over possible blocking coalitions containing that tier
    #find utility of each agent at each level.
            #if all are neutral+ and at least one approves, it blocks. return false
    #if nobody blocks, return true



#finds whether a k tier list is  core stable
def isCoreStable(T, Win, n, k):
    #get each agent's current utility
    #also, get the number of strict subsets of each set
    utility = [0 for i in range(n)]
    stesbuS = []
    for i in range(k):
        for a in T[i]:
            u = 0
            for r in range(i+1):
                for b in T[r]:
                    u += Win[a][b]
            utility[a] = u
        stesbuS.append(range(2**len(T[i])))
    
    
    for i in range(k):
        print('.')
        stesbuS_i = []
        AlreadySeen = []
        for j in range(i+1):
            AlreadySeen.extend(T[j])
        for j in range(k):
            if j == i:
                stesbuS_i.append([0])
            else:
                stesbuS_i.append(stesbuS[j])
        for picks in product(*stesbuS_i):
            #Form each blocking coalition
            C = []
            C.extend(T[i])
            for j in range(k):
                C.extend(helper.subsetnumber(T[j], picks[j]))
            #find each utility of each agent at each level
            Seen = []
            Seen.extend(C)
            if set(AlreadySeen) != set(Seen):
                if strongBlockIfSeen(C, Seen, Win, utility):
                    #the tier blocks by moving to tier 1
                    return False, C, 0
            for j in range(k):
                changed = False
                for a in T[j]:
                    if a not in Seen:
                        changed = True
                        Seen.append(a)
                if changed:
                    if set(AlreadySeen) != set(Seen):
                        if strongBlockIfSeen(C, Seen, Win, utility):
                            return False, C, j+1
    #If we got this far, there are no blocking coalitions
    return True, -1, -1




def isNashStable(T, Win, n, k):
    umax = [-1*n for j in range(n)]
    pmax = [-1 for j in range(n)]
    pcurr = [-1 for j in range(n)]
    #perform the search itself
    for i in range(k):
        for j in range(len(T[i])):
            #find current and maximum position for an agent
            a = T[i][j]
            u = 0
            pcurr[a] = i
            if len(T[i]) == 1:
                umax[a] = 0
                pmax[a] = 0
            for r in range(k):
                #find the utility of a at tier r
                for s in range(len(T[r])):
                    u = u + Win[a][T[r][s]]
                #adjust max, where tier i wins all ties
                if (u > umax[a] or (u == umax[a] and r == i)):
                    umax[a] = u
                    pmax[a] = r

            #if the agent wants to move, determine if the move is valid
            pm = pmax[a]
            pc = pcurr[a]
            if pm != pc:
                return False
    #if we have gotten this far, the list is stable
    return True

def isCoreAndNash(T, Win, n, k):
    r1, C, j = isCoreStable(T, Win, n, k)
    r2 = isNashStable(T, Win, n, k)
    return r1, r2

##def etStableTierList(T, Win, n, k, e):
##    Cost = UpwardMergeCost(T, Win, n)
##    U, V = kTierList(Cost, n, k)
##    #perform merges according to the values stored at V
##    Tk = []
##    low = 0
##    for i in range(k):
##        high = V[i]+1
##        Tk.append(T[low:high])
##        low = high
##
##    Tk, d = etLocalSearch(Tk, Win, n, -1*e)
##    Tkf = [ele for ele in Tk if ele != []]
##    
##    return Tkf, d



def NashDeviations(T, Win, n, k):
    devs = []
    for i in range(k):
        for a in T[i]:
            u = 0
            us = []
            for j in range(k):
                for b in T[j]:
                    u += Win[a][b]
                us.append(u)
            ucurr = us[i]
            if ucurr != max(us):
                row = [a]
                for x in us:
                    row.append(x - ucurr)
                devs.append(row)
    return devs


if __name__ == '__main__':
    import tcfginitialize as tcfg
##    T = [[0, -1, 0.7],
##         [1, 0, -0.9],
##         [-0.7, 0.9, 0]]
##
##    Cost = UpwardMergeCost(T, 3)
##    print(Cost)
##    print(kTierList(Cost, 3, 2))

##    Win = [[0, -1, 0.7],
##           [1, 0, -0.9],
##           [-0.7, 0.9, 0]]
##    T = tcfg.silerSort(Win)
##    Tk = kStableTierList(T, Win, 3, 2)
##    print(Tk)

    n = 10
    k = 3
    e = 1
    for i in range(1):
        Win = tcfg.unbiasedProb(n)
        T = tcfg.silerSort(Win)
        Tk, d = kStableTierList(T, Win, n, k)
        stable, C, targ = isCoreStable(Tk, Win, n, k)
        #print(Tk)
        #print(Win)
##        Tk, d = eStableTierList(T, Win, n, k, e)
##        print(Tk)
##        print(k, ", ", d)
##        print(utility(Tk, Win, len(Tk)))
##        print(fun(Tk, len(Tk)))
##        print(robustness(Tk, Win))
##        print("")
#        Tk, d = kStableTierList(T, Win, n, k+1)
    Win = [[0, 1, 1, 1], [-1, 0, 1, -1], [-1, -1, 0, -1], [-1, 1, 1, 0]]
    T = [[2], [1, 3], [0]]
    stable, C, targ = isCoreStable(T, Win, 4, 3)
    print(stable)
    print(C)
    print(targ)
    
##    Win = [[0, -1, 1, -1, 1, 1, -1, 1, 1, 1], [1, 0, -1, 1, 1, -1, -1, -1, 1, 1], [-1, 1, 0, 1, -1, 1, -1, -1, 1, 1], [1, -1, -1, 0, 1, 1, -1, 1, -1, -1], [-1, -1, 1, -1, 0, -1, 1, -1, -1, 1], [-1, 1, -1, -1, 1, 0, -1, -1, 1, 1], [1, 1, 1, 1, -1, 1, 0, -1, 1, -1], [-1, 1, 1, -1, 1, 1, 1, 0, -1, -1], [-1, -1, -1, 1, 1, -1, -1, 1, 0, -1], [-1, -1, -1, 1, -1, -1, 1, 1, 1, 0]]
##    T = tcfg.silerSort(Win)
##    Tk = kStableTierList(T, Win, n, k)
##    Tk = kStableTierList(T, Win, n, k+1)


