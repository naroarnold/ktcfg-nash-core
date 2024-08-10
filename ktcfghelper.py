import math


def bitfield(i, n):
    x = [int(digit) for digit in bin(i)[2:]]
    x.reverse()
#    y = (n**2 - 3*n + 2) / 2
    while (len(x) < n):
        x.append(0)
    return x

def subsetnumber(Set, x):
    l = len(Set)
    if x > 2**l:
        print("subsetnumber called with too large a number for the set.")
        raise SystemExit(0)
    bf = bitfield(x, l)
    result = []
    for i in range(l):
        if (bf[i] == 1):
            result.append(Set[i])
    return result
    

def generate_instance(i, n):
    matrix = [[0 for j in range(n)] for k in range(n)]
    #generate bitfield of length (n^2 - 3n + 2) / 2
    bf = bitfield(i, (n**2 - 3*n +2) / 2)
    x = 0
    for j in range(n):
        for k in range(j-1):
            if (bf[x] == 0):
                matrix[j][k] = 1
                matrix[k][j] = -1
            else:
                matrix[j][k] = -1
                matrix[k][j] = 1
            x += 1
        if j > 0:
            matrix[j-1][j] = 1
            matrix[j][j-1] = -1
    return matrix

def sorted_k_partitions(seq, k):
    """Returns a list of all unique k-partitions of `seq`.

    Each partition is a list of parts, and each part is a tuple.

    The parts in each individual partition will be sorted in shortlex
    order (i.e., by length first, then lexicographically).

    The overall list of partitions will then be sorted by the length
    of their first part, the length of their second part, ...,
    the length of their last part, and then lexicographically.
    """
    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()

            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    result = generate_partitions(0)

    # Sort the parts in each partition in shortlex order
    result = [sorted(ps, key = lambda p: (len(p), p)) for ps in result]
    # Sort partitions by the length of each part, then lexicographically.
    result = sorted(result, key = lambda ps: (*map(len, ps), ps))

    return result


def kTierify(T, k, n, mode = "e"):
    Tk = []

    #tiers approximately equal in size
    if mode == "e":
        s = math.floor(n/k)
        u = n%k
        j = 0
        for i in range(0, u):
            Tk.append(T[j:(j+s+1)])
            j = j+s+1
        for i in range(u, k):
            Tk.append(T[j:(j+s)])
            j = j+s
        
    
    #first n-k+1 elements together, all others singleton
    if mode == "f":
        Tk.append(T[0:(n-k+1)])
        for i in range(n-k+1, n):
            Tk.append([T[i]])


    #last n-k+1 elements together, all others singleton
    if mode == "l":
        for i in range(k-1):
            Tk.append([T[i]])
        Tk.append(T[(k-1):n])


    #middle n-k+1 elements together, all others singleton
    if mode == "m":
        l = math.ceil((k-1)/2)
        u = l+n-k+1
        Tk.append(T[0:l])
        for i in range(l, u):
            Tk.append([T[i]])
        Tk.append(T[u:n])

    
    return Tk
