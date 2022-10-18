import time
import csv


def find_path(starting_node, cost_sum, visited):
    visited.append(starting_node)

    if len(visited) > 1:
        cost_sum += nodes[visited[-2]][starting_node]

    if len(visited) == len(nodes):
        global routes
        cost_sum += nodes[starting_node][visited[0]]
        visited.append(visited[0])
        if cost_sum < routes[1]:
            routes[0] = visited
            routes[1] = cost_sum
        return

    for i in range(len(nodes)):
        if starting_node == i:
            continue
        if routes[1] < cost_sum:
            break
        if i not in visited:
            find_path(i, cost_sum, list(visited))


def config_import(file):
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        print(t)
        l = [[int(num) for num in line.strip().split(' ')] for line in f]
    return l


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
            point = int(input("Podaj numer wierzcholka poczatkowego\n"))

            nodes = config_import(file)
            global routes
            routes = [0, 999999]
            find_path(point, 0, [])
            print(f"Route: {routes[0]}, Suma: {routes[1]}\n")
            menu()
        case "2":
            f = open("wyniki.csv", 'w')
            writer = csv.writer(f)
            writer.writerow(["Plik","Czas[s]","Sciezka"])

            # 6
            nodes = config_import("6_1.txt")
            data = benchmark(100)
            writer.writerow(["6_1.txt", data,routes[0]])

            # 10
            nodes = config_import("10.txt")
            data = benchmark(100)
            writer.writerow(["10.txt", data,routes[0]])

            # 12
            nodes = config_import("12.txt")
            data = benchmark(20)
            writer.writerow(["12.txt", data,routes[0]])

            # 13
            nodes = config_import("13.txt")
            data = benchmark(10)
            writer.writerow(["13.txt", data,routes[0]])

            # 14
            nodes = config_import("14.txt")
            data = benchmark(4)
            writer.writerow(["14.txt", data,routes[0]])

            #15 
            nodes = config_import("15.txt")
            data = benchmark(1)
            writer.writerow(["15.txt",data,routes[0]])

        case _:
            menu()


def benchmark(sample):
    data = 0
    global routes
    routes = [0, 999999]
    for i in range(sample):
        start_time = time.time()
        find_path(0, 0, [])
        end_time = time.time() - start_time
        data += end_time
        print(routes)
    return data/sample


if __name__ == "__main__":
    menu()
    input("COS SIE STALO")

"""
    file = input("Wpisz nazwe pliku: ")
    nodes = config_import(file)
    
    start_time = time.time()
    find_path(0, 0, [])
    print(time.time() - start_time)
    print(f"Route: {routes[0]}, Suma: {routes[1]}\n")
"""
