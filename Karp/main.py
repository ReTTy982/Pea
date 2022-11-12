import itertools
import random
import sys

table = [1, 2, 3]

comb_set = itertools.combinations(table, 3)
dict = {}
dictprev = {}

matrix = [
    [0, 20, 30, 31, 28, 40],
    [30, 0, 10, 14, 20, 44],
    [40, 20,  0, 10, 22, 50],
    [41, 24, 20, 0, 14, 42],
    [38, 30, 32, 24, 0, 28],
    [50, 54, 60, 52, 38, 0]]

matrix = [
    [0,10,20,30],
    [5,0,4,6],
    [7,8,0,9],
    [10,8,6,0]
]

"""
 0 20 30 31 28 40
30  0 10 14 20 44
40 20  0 10 22 50
41 24 20  0 14 42
38 30 32 24  0 28
50 54 60 52 38  0
    """


n = len(matrix[0])

for k in range(1, n):
    dict[(1 << k, k)] = (matrix[0][k], 0)

for subset_size in range(2, n):
    for subset in itertools.combinations(range(1, n), subset_size):
        
        bits = 0
        for bit in subset:
            bits |= 1 << bit # (1,2,3) = 1110 
        for i in subset:
            
            prev = bits & ~(1 << i)
           
            temp = []
            for j in subset:
                if j == 0 or j == i:
                    continue
                temp.append((dict[(prev, j)][0] + matrix[j][i], j))
                print(temp)
                
            dict[(bits, i)] = min(temp)

       # dictprev.update({format(bits, 'b'): format(prev, 'b')})

bits  = (2**n-1) - 1 # Usuwamwierzchołek zero bo jest to wierzchołek startowy
# Tutaj sprawdzam przedostatni wierzcholek
print(dict)
temp = []
for k in range (1,n):
    print(bits)
    temp.append((dict[(bits,k)][0] + matrix[k][0]))
    print(dict[(bits,k)][0])
    print(matrix[k][0])
    print(temp)
opt,parent = min(temp)


# Back tracking



if __name__ == '__main__':
    #print(dictprev)
    #print("XD")
    #print(dict)
    # print(dict)
    pass
    


"""
 0 20 30 31 28 40
30  0 10 14 20 44
40 20  0 10 22 50
41 24 20  0 14 42
38 30 32 24  0 28
50 54 60 52 38  0
"""
