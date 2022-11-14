import itertools


def config_import(file):
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        print(t)
        l = [[int(num) for num in line.strip().split(' ')] for line in f]
    return l


def karp(matrix):
    """
        matrix = [
            [0, 20, 30, 31, 28, 40],
            [30, 0, 10, 14, 20, 44],
            [40, 20,  0, 10, 22, 50],
            [41, 24, 20, 0, 14, 42],
            [38, 30, 32, 24, 0, 28],
            [50, 54, 60, 52, 38, 0]]

        matrix = [
            [0  2  9 10],
            [1  0  6  4],
            [7, 8, 0, 9],
            [10, 8, 6, 0]
        ]

    """
    n = len(matrix[0])
    dict = {}

    for k in range(1, n):
        dict[(1 << k, k)] = (matrix[0][k], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):

            bits = 0
            for bit in subset:
                bits |= 1 << bit  # (1,2,3) = 1110
            for i in subset:

                prev = bits & ~(1 << i)

                temp = []
                for j in subset:
                    if j == 0 or j == i:
                        continue
                    temp.append((dict[(prev, j)][0] + matrix[j][i], j))

                dict[(bits, i)] = min(temp)

        # dictprev.update({format(bits, 'b'): format(prev, 'b')})

    # Usuwamwierzchołek zero bo jest to wierzchołek startowy
    bits = (2**n-1) - 1
    # Tutaj sprawdzam przedostatni wierzcholek

    temp = []
    for k in range(1, n):

        temp.append((dict[(bits, k)][0] + matrix[k][0], k))
        print(dict[(bits, k)][0] + matrix[k][0], k)

    opt, parent = min(temp)

    path = []
    for i in range(n-1):
        print(parent)
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        dummy, parent = dict[(bits, parent)]
        bits = new_bits

    path.append(0)
    path = list(reversed(path))
    path.append(0)
    return opt, path