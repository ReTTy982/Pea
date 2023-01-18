from __future__ import annotations
import math
from pathlib import Path
import random
import time
import re
import csv
import itertools

# When denominator's precision will bug out to be equal zero.
SMALL_FLOAT = 2.2250738585072014e-308


class AntColony:

    def __init__(self, alpha, beta, evaporation_rate, matrix, qas_value):
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.matrix = matrix
        self.qas_value = qas_value

        self.pheromone_matrix = []
        self.ants_number = len(matrix) # TODO zmienic potem na len(matrix)
        #self.ants_number = 1
        self.N = len(matrix)
        self.colony = []
        self.min_cost = 99999999999999999999
        self.best_path = []

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
        cost = self.calculate_path_cost(vertexes)
        return cost * self.alpha

    def calculate_path_cost(self, path):  # Nie wiem co to robi
        cost = 0
        for i in range(self.N-1):
            cost += self.matrix[path[i]][path[i+1]]
        cost += self.matrix[path[-1]][path[0]]
        return cost

    def visibility(self, start, finish) -> int:

        pass

    def calculate_probability(self):  # Mozliwe ze nie trzba
        pass

    def calculate_denominator(self, ant: Ant):
        denominator = float(0)
        atractivness = dict()
        for i in ant.possible_moves:
            pheromone_ammount = float(
                self.pheromone_matrix[ant.last_visited][i])
            distance = float(matrix[ant.last_visited][i])
            atractivness[i] = pow(
                pheromone_ammount, self.alpha) * pow(1/distance, self.beta)
            denominator += atractivness[i]
        
        return denominator, atractivness

    def change_pheromone(self):
        # Evaporate pheromone from all paths 
        for i in range(self.N):
            for j in range(self.N):
                if i == j:
                    pass
                else:
                    self.pheromone_matrix[i][j] = self.pheromone_matrix[i][j] * self.evaporation_rate

        # Calculate cost of route and put down some pheromone
        for ant in self.colony:
            cost = self.calculate_path_cost(ant.tabu)
            if cost < self.min_cost:
                self.min_cost = cost
                self.best_path = ant.tabu.copy()
            
            for i in range(self.N):
                if i == self.N - 1:
                    self.pheromone_matrix[ant.tabu[i]][ant.tabu[-1]] = float(self.qas_value / cost)
                else:
                    self.pheromone_matrix[ant.tabu[i]][ant.tabu[i+1]] = float(self.qas_value / cost)
            

                
            


    def pick_vertex(self, ant: Ant, denominator: float, atractivness: dict):
        for i in atractivness.keys():
            x = random.random()  # interval [0,1)
            if denominator == 0:
                denominator = SMALL_FLOAT
            y = atractivness[i] / denominator
            if x < y:
                ant.pick_vertex(i)
                return
        # When no path has been chosen
        sorted_list = sorted(atractivness.items(), key=lambda x: x[1])
        
        vertex = sorted_list[0][0]  # (key,value)
        ant.pick_vertex(vertex)


    def run_algorithm(self, iter):

        self.init_pheromone()
        vertexes = []
        vertexes.extend(range(0, self.N))
        starting_vertex = random.choice(vertexes)

        for i in range(self.ants_number):
            self.colony.append(self.Ant(starting_vertex,i))

        for iterations in range(iter):  # number of iterations
            for ant_index in range(len(self.colony)):  # number of ants, itereting objects

                ant = self.colony[ant_index]
                print(ant_index)
                for move in range(self.N-1) :  # number of aviable moves
                    # If first move potem trzeba bedzie zniszczyc liste
                    if ant.first_move:
                        ant.possible_moves = list(
                            set(vertexes.copy()) - set(ant.tabu))
                        ant.first_move = False

                    denominator, atractivness = self.calculate_denominator(ant)
                    self.pick_vertex(ant, denominator, atractivness)

                    # ant.pick_vertex(vertexes)
            self.change_pheromone()

    class Ant():
        def __init__(self, starting_vertex,id):
            self.tabu = [starting_vertex]  # List of visited vertexes
            self.possible_moves = None  # List of possible moves. Set upon using pick_vertex()
            self.first_move = True
            self.last_visited = starting_vertex  # Moze do usuniecia
            self.id = id # do testowania

        # Mozliwe do usuniecia
        """
        def pick_vertex(self, vertexes: list, matrix:list):
            if self.first_move:
                # Fastest way to choose vertex excluding tabu list
                self.possible_moves = vertexes.copy()
                self.last_visited = random.choice(self.possible_moves)
                self.tabu.append(self.last_visited)
                self.first_move = False
                """

        def pick_vertex(self, vertex):
            self.tabu.append(vertex)
            self.possible_moves.remove(vertex)
            self.last_visited = vertex

        def calculate_denominator(self, pheromone_matrix: list, matrix: list):
            sum = float(0)
            for i in self.possible_moves:
                pheromone_ammount = float(
                    pheromone_matrix[self.last_visited][i])
                distance = float(matrix[self.last_visited][i])
                sum += pow(pheromone_ammount,)


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
    qvalue = 100

    files, output = get_ini()
    f = open(output, 'w')
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Plik", "Czas[s]", "Koszt", "Sciezka"])
    for file_name in files.keys():
        matrix = better_config(file_name)
        x = AntColony(alpha, beta, evaporation_rate, matrix,qvalue)
        x.run_algorithm(1)
        print(f"{x.best_path} , {x.min_cost}")


# TODO ZEROWANIE LIST BO DZIALA TERAZ TYLKO DLA JEDNEJ ITERACJI