import itertools
import time
import csv

# Czytanie pliku ini
def get_ini():
    tsp = {}
    with open("config.ini", 'r') as f:
        t = int(f.readline().strip())
        for i in range(t):
            x = f.readline().strip().split(" ")
            tsp[x[0]] = x[1]

        output = f.readline().strip()

    return tsp, output

# Czytanie plikow txt
def better_config(file):
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        l = []
        for i in range(t):
            l.append([])
        row = 0
        column = 0
        liczba = ""
        read = f.read()
        for i in read:
            if i == " " or i == "\n":
                l[row].append(int(liczba))
                liczba = ""
                column += 1
                if column == t:
                    column = 0
                    row += 1
            else:
                liczba += i
        return l


"""
1. Wczytaj macierz
2. Zainicjuj pierwsze podzbiory
3. Zacznij iterować zbuory od najmniejszego do najwiekszego
4. Ustaw maske kazdego zbioru
5. Do każdego podzbioru oblicz najkrotsza droge korzystajac z poprzednich podzbiorow.
"""


def karp(matrix):
    n = len(matrix[0])
    subset_data = {}

    # Mapowanie pierwszych zbiorów. Format { (bity, wierzchołek) : (koszt, poprzednik) }
    for vertex in range(1, n):
        subset_data[(1 << vertex, vertex)] = (matrix[0][vertex], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):

            bits = 0
            for bit in subset:
                bits |= 1 << bit  # (1,2,3) = 1110
            for i in subset:

                prev = bits & ~(1 << i)
                # wyszukanie poprzednich podzbiorow i wybranie minimalnego
                patch_cost = []
                for j in subset:
                    if j == 0 or j == i:
                        continue
                    patch_cost.append(
                        (subset_data[(prev, j)][0] + matrix[j][i], j))

                subset_data[(bits, i)] = min(patch_cost)

    # Usuwamwierzchołek zero bo jest to wierzchołek startowy
    bits = (2**n-1) - 1  # = n=6 to bits  = 111110
    

    patch_cost = []
    for k in range(1, n):
        patch_cost.append((subset_data[(bits, k)][0] + matrix[k][0], k))

    opt, parent = min(patch_cost)

    path = []
    for i in range(n-1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        dummy, parent = subset_data[(bits, parent)]
        bits = new_bits

    path.append(0)
    path = list(reversed(path))
    path.append(0)
    return opt, path


def menu():
    print("""
    1. TSP - Wczytaj pojedynczy plik
    2. TSP - Uruchom program przez config.ini
    """)
    user_choice = input()
    global nodes

    match user_choice:
        case "1":
            file = input("Podaj nazwe pliku (wraz z .txt)\n")
            nodes = better_config(file)
            cost, route = karp(nodes)
            print(f"Route: {route}, Suma: {cost}\n")
            menu()
        case "2":
            files, output = get_ini()
            f = open(output, 'w')
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Plik", "Czas[s]", "Sciezka", "Koszt"])

            for i in files.keys():
                nodes = better_config(i)
                data, cost, route = benchmark(int(files[i]))
                writer.writerow([i, data, route, cost])
                print(f"Done: {i}")
        case _:
            menu()

# Liczenie czasu
def benchmark(sample):
    data = 0
    for i in range(sample):
        start_time = time.time()
        cost, route = karp(nodes)
        end_time = time.time() - start_time
        data += end_time
    return data/sample, cost, route


if __name__ == '__main__':
    menu()
    input("Zakończono działanie programu")
