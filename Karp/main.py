import itertools


def config_import(file):
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        l = [[int(num) for num in line.strip().split(' ')] for line in f]
    return l

def better_config(file):
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        l=[]
        for i in range(t):
            l.append([])
        row = 0
        column =0
        liczba = ""
        read = f.read()
        for i in read:
            if i == " " or i == "\n":
                l[row].append(int(liczba))
                liczba=""
                column+=1
                if column == t:
                    column = 0
                    row+=1
            else:
                liczba +=i
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

    opt, parent = min(temp)

    path = []
    for i in range(n-1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        dummy, parent = dict[(bits, parent)]
        bits = new_bits

    path.append(0)
    path = list(reversed(path))
    path.append(0)
    return opt, path

# Back tracking


def menu():
    print("""
    1. TSP - poprawnosc algorytmu.
    2. TSP - pomiar czasu wykonania algorytmu
    """)
    user_choice = input()
    global nodes

    match user_choice:
        case "1":
            file = input("Podaj nazwe pliku (wraz z .txt)\n")
            nodes = better_config(file)
            global routes
            routes = [0, 999999]
            cost, route = karp(nodes)
            print(f"Route: {route}, Suma: {cost}\n")
            menu()
        case _:
            file = "6_1.txt"
            nodes = better_config(file)
            routes = [0, 999999]
            cost, route = karp(nodes)
            print(f"Route: {route}, Suma: {cost}\n")
            menu()
            menu()

def benchmark(sample):
    pass


if __name__ == '__main__':
    menu()
    input("NIE KLIKAJ NICZEGO")

"""
 0 20 30 31 28 40
30  0 10 14 20 44
40 20  0 10 22 50
41 24 20  0 14 42
38 30 32 24  0 28
50 54 60 52 38  0
"""