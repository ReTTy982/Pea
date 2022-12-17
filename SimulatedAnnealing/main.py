import math
import decimal
from pathlib import Path
import random
from typing import DefaultDict
import time
import csv
import re
INT_MAX = 2147483647


class Wyrzazanie():
    def __init__(self, alpha, stop_temperature, epoch, stop_time, matrix, starting_point):
        self.temperature = None
        self.alpha = alpha
        self.best_route = None
        self.best_sum = INT_MAX
        self.stop_i = 10000
        self.stop_time = stop_time # czas podany w sekundach 
        self.stop_temperature = 10 ** (-stop_temperature) # stop_temperature to ilosc miejsc po przecinku 
        self.i = 1
        self.epoch = epoch
        self.matrix = matrix
        self.starting_point = starting_point

    def start_temperature(self, sum, vertex):
        self.temperature = sum*vertex

    def start_epoch(self):
        self.epoch *= len(self.matrix)

    def start_solution(self):
        sum = 0
        counter = 0
        j = 0
        i = 0
        min = INT_MAX
        visitedRouteList = DefaultDict(int)

        # Starting from the 0th indexed
        # city i.e., the first city
        visitedRouteList[self.starting_point] = 1
        route = [0] * len(self.matrix)

        # Traverse the adjacency
        # matrix tsp[][]
        while i < len(self.matrix) and j < len(self.matrix[i]):

            # Corner of the Matrix
            if counter >= len(self.matrix[i]) - 1:
                break

            # If this path is unvisited then
            # and if the cost is less then
            # update the cost
            if j != i and (visitedRouteList[j] == 0):
                if self.matrix[i][j] < min:
                    min = self.matrix[i][j]
                    route[counter] = j  # oryginal

            j += 1

            # Check all paths from the
            # ith indexed city
            if j == len(self.matrix[i]):
                sum += min
                min = INT_MAX
                visitedRouteList[route[counter]] = 1  # tutaj
                j = 0
                i = route[counter]  # tutaj
                counter += 1

        # Update the ending city in array
        # from city which was last visited
        i = route[counter - 1]
        min = self.matrix[i][self.starting_point]
        route[counter] = self.starting_point
        sum += min
        self.best_route = route
        self.best_sum = sum
        self.current_route = route
        self.current_sum = sum

        # Started from the node where
        # we finished as well.
        print("Minimum Cost is :", sum, route)

    def nearest_neighbour(self):
        pass

    def distance(self):
        pass

    def inverse_solution(self, solution):
        node_one = random.choice(solution)
        new_list = list(filter(lambda ver: ver != node_one, solution))
        node_two = random.choice(new_list)
        solution[min(node_one, node_two):max(node_one, node_two)] = solution[min(
            node_one, node_two):max(node_one, node_two)][::-1]

        return solution

    def probability_accept(self, candidate_sum):
        delta = candidate_sum - self.current_sum
        return math.exp(-(delta) / self.temperature)

    def cooldown_geo(self):
        self.temperature *= self.alpha
       # print(f"Temperatura: {self.temperature:.9f}",end="\r")

    def accept(self, candidate):

        candidate_sum = self.calculate_route(candidate)

        if candidate_sum < self.current_sum:
            self.current_sum = candidate_sum
            self.current_route = candidate
            if candidate_sum < self.best_sum:
                print(
                    f"ZMIENIONO SUME Z {self.best_sum} na {candidate_sum} Lepszy Route: {candidate}")
                self.best_sum = candidate_sum
                self.best_route = candidate
        else:
            x = random.random()
            y = self.probability_accept(candidate_sum)
            if x < y:
                self.current_sum = candidate_sum
                self.current_route = candidate

    def calculate_route(self, route):
        sum = 0
        previous = route[-1]
        for i in range(len(self.matrix)):
            sum += self.matrix[previous][route[i]]
            previous = route[i]
        return sum

    def run_algorythm(self,cooling,neighbour_algorithm,start_time):
        self.start_solution()
        self.start_epoch()
        self.start_temperature(self.current_sum, len(self.current_route))
        while self.temperature >= self.stop_temperature and time.time() - start_time < self.stop_time:
            for i in range(self.epoch):
                old_candidate = list(self.current_route)
                candidate = self.inverse_solution(old_candidate)
                self.accept(candidate)
                print(f"{(time.time() - start_time):.3f} ===  {self.stop_time}",end='\r')

            match cooling:
                case "geo":
                    self.cooldown_geo()
                case "log":
                    pass
            

        print(f'Sciezka: {self.best_route}\n Suma {self.best_sum}')

    def benchmark(self, sample):
        data = 0
        for i in range(sample):
            start_time = time.time()
            self.run_algorythm()
            end_time = time.time() - start_time
            data += end_time


def benchmark(alpha, stop_temperature, epoch, stop_time, matrix, starting_point, cooling,neighbour_algorithm):
    time_ms = 0
    x = Wyrzazanie(alpha=alpha, stop_temperature=stop_temperature,
                   epoch=epoch, stop_time=stop_time, matrix=matrix, starting_point=starting_point)
    start_time = time.time()
    x.run_algorythm(cooling,neighbour_algorithm, start_time)
    end_time = time.time()
    time_ms += end_time - start_time
    return time_ms, x.best_sum, x.best_route


# Czytanie pliku ini

def get_ini():
    tsp = {}
    with open("config.ini", 'r') as f:
        files_nr = int(f.readline().strip())
        algorithms = f.readline().strip().split(" ")
        for i in range(files_nr):
            x = f.readline().strip().split(" ")
            tsp[x[0]] = x[1:7]

        #output = f.readline().strip()
        content = f.read()
        output = re.findall(r'#\w+',content)
        output = output[0]
        output = output[1:] + ".csv"

        

    return tsp, output,algorithms

# Czytanie plikow txt


def better_config(file):
    folder = Path('Dane')
    file = folder / file
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        print(f" CO TO JEST {t}")
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
        return l


if __name__ == '__main__':
    

    # Wyrzazanie(alpha=0.99,stop_temperature=0.000000000001,epoch=5,stop_time=0,matrix=nodes,starting_point=0).run_algorythm()
    # x.run_algorythm()
    # benchmark(5)

    files, output, algorithms = get_ini()
    print(f"AAAAAAAAAAAAAAAAAAAAAAA {output}")
    f = open(output, 'w')
    writer = csv.writer(f, delimiter=";")
    for file_name in files.keys():
        writer.writerow(["Plik", "Czas[s]", "Koszt", "Sciezka"])
        
        atributes = files[file_name]
        print(atributes)
        alpha = float(atributes[0])
        stop_temperature = int(atributes[1])
        epoch = int(atributes[2])
        stop_time = int(atributes[3])
        starting_point = int(atributes[4])
        sample = int(atributes[5])
        cooling = algorithms[0]
        neighbor = algorithms[1]
        matrix = better_config(file_name)

        

        for j in range(sample):
            timer_ms, cost, route = benchmark(alpha, stop_temperature, epoch,
                    stop_time, matrix, starting_point,cooling,neighbor)
            writer.writerow([file_name,timer_ms,cost,route])

