import math
from pathlib import Path
import random
import time
import re
import csv
import itertools


class AntColony:

    def __init__(self, alpha, beta, evaporation_rate, matrix):
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.matrix = matrix

        self.pheromone_matrix = []
        self.ants_number = len(matrix)
        self.N = len(matrix)
        self.colony = []

    def init_pheromone(self):
        tau_zero = self.ants_number / self.init_distance()

        for i in range(self.N):
            self.pheromone_matrix.append([])
        for i in range(self.N):
            for j in range(self.N):
                self.pheromone_matrix[i].append(tau_zero)

    def init_distance(self):
        vertexes = []
        vertexes.extend(range(0, self.N))
        random.shuffle(vertexes)
        cost = self.calculate_cost(vertexes)
        return cost * self.alpha

    def calculate_cost(self, path):
        cost = 0
        print(path)
        for i in range(self.N-1):
            cost += self.matrix[path[i]][path[i+1]]
        cost += self.matrix[path[-1]][path[0]]
        return cost

    def evaporate_pheromone(self):
        pass

    def run_algorithm(self, iter):

        self.init_pheromone()

        for i in range(self.ants_number):
            vertexes = []
            vertexes.extend(range(0, self.N))
            starting_vertex = random.choice(vertexes)
            self.colony.append(self.Ant(starting_vertex))

        for iterations in range(iter):  # number of iterations
            for ant in self.colony:  # number of ants, itereting objects
                for move in range(self.N):  # number of aviable moves
                    # Choose vertex
                    ant.pick_vertex()
        
        self.evaporate_pheromone()
        

    class Ant():
        def __init__(self, starting_vertex):
            self.starting_vertex = starting_vertex
            self.tabu = []

        def pick_vertex(self):
            pass


def better_config(file):
    folder = Path('Dane')
    file = folder / file
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        l = []
        for i in range(t):
            l.append([])
        row = 0
        column = 0
        liczba = ""
        read = f.read()
        read = ' '.join(read.split())
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
        l[row].append(int(liczba))
        return l

# Czytanie pliku ini


def get_ini():
    tsp = {}
    with open("config.ini", 'r') as f:
        files_nr = int(f.readline().strip())
        for i in range(files_nr):
            x = f.readline().strip().split(" ")
            tsp[x[0]] = x[1:7]

        content = f.read()
        output = re.findall(r'#\w+', content)
        output = output[0]
        output = output[1:] + ".csv"

    return tsp, output


def benchmark(object: AntColony):
    pass


if __name__ == '__main__':

    # For purpose of testing
    alpha = 1
    beta = 3
    evaporation_rate = 0.5

    files, output = get_ini()
    f = open(output, 'w')
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Plik", "Czas[s]", "Koszt", "Sciezka"])
    for file_name in files.keys():
        matrix = better_config(file_name)
        x = AntColony(alpha, beta, evaporation_rate, matrix)
        x.run_algorithm(1)
