import random as ran
import csv
import sys

# Generates a random adjacency matrix.
# Input: n, the size of the square matrix.
# Output: a randomly generated adjacency matrix; 1 represents a good matchup, -1 a bad one
def unbiasedDet(n):
    matrix = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(i):
            x = ran.randint(0, 1)
            if (x == 0):
                matrix[i][j] = 1
                matrix[j][i] = -1
            else:
                matrix[i][j] = -1
                matrix[j][i] = 1
    # printMatrix(matrix)
    return matrix


# Like the above, except this initialization favors the higher-indexed agent by a certain
# percent, between 0 and 1.
# Input: n, the number of agents/size of the matrix; pct, a value between 0 and 1. Should
# be higher than 0.5 to create bias towards higher agents.
# Output: an adjacecy matrix generated with the given bias.
def weightedTCFGInstanceGeneration(n, pct):
    matrix = [[0 for i in range(n)] for j in range(n)]
    for i in range(n): #higher agent
        for j in range(i): #lower agent
            x = ran.random()
            if (x < pct):
                matrix[i][j] = 1
                matrix[j][i] = -1
            else:
                matrix[i][j] = -1
                matrix[j][i] = 1
    # printMatrix(matrix)
    return matrix


#Adds noise to generate a probabilistic matrix from a 
def addNoiseToMatrix(matrix, noiseValue):
    for i in range(len(matrix)):
        for j in range(i):
            x = ran.random() * noiseValue
            if (matrix[i][j] == -1):
                matrix[i][j] = -1 + x
                matrix[j][i] = 1 - x
#                matrix[i][j] = 0 - x
#                matrix[j][i] = x
            elif (matrix[i][j] == 1):
                matrix[i][j] = 1 - x
                matrix[j][i] = -1 + x
#                matrix[i][j] = x
#                matrix[j][i] = 0 - x
    return matrix

#Generate an unbiased probabilistic win matrix
def unbiasedProb(n):
    return addNoiseToMatrix(unbiasedDet(n), 1)

#Generate a progressive-biased probabilistic win matrix
def progressiveProb(n):
    matrix = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(i):
            x = ((ran.random() * 2) - 1) + (i - j - 1)/n
            x = min(x, 1)
            matrix[i][j] = x
            matrix[j][i] = -1 * x
    return matrix


# Performs Siler's tier list generation procedure.
# Input: matrix, the matchup matrix.
# Output: a, a stable tier list. Every agent will be in its own tier.
def silerSort(matrix):
    n = len(matrix)
    a = []
    for i in range(n):
        a.append(i)
    b = [0 for i in range(n)]
    counter = 0

    while (b != a):
        counter += 1
        b = a.copy()
        for i in range(n):
            current = 0
            max = 0
            maxPos = 0
            k = 0
            for j in range(n):
                k = k + matrix[a[i]][a[j]]
                if (i == j): current = k
                if (k == max):
                    maxPos = j
                elif (k > max):
                    max = k
                    maxPos = j
            if (current < max):
                temp = a[i]
                a.pop(i)
                if(i < maxPos):
                    a.insert(maxPos, temp)
                else:
                    a.insert(maxPos+1, temp)
                break
                
        if counter >= n**2:
            print("uh oh spaghettios")
            print(a)
            with open("uhohspaghettios.csv","w",newline='') as rcsv:
                csvWriter = csv.writer(rcsv, delimiter=',')
                sys.exit(1)
            break
    return a


if __name__ == '__main__':
    import tcfginitialize as tcfg
    T = [[0, 0.9, -0.7],
         [0.9, 0, 1],
         [0.7, -1, 0]]
    print(silerSort(T))
