import math
import decimal
from pathlib import Path
import random
from typing import DefaultDict
import time
INT_MAX = 2147483647


class Wyrzazanie():
    def __init__(self, alpha, stop_temperature,epoch,stop_time,matrix,starting_point):
        self.temperature = None
        self.alpha = alpha
        self.best_route = None
        self.best_sum = INT_MAX
        self.stop_i = 10000
        self.stop_time = stop_time
        self.stop_temperature = stop_temperature
        self.i = 1
        self.epoch = epoch
        self.matrix = matrix
        self.starting_point = starting_point

    def start_temperature(self,sum,vertex):
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

    def cooldown(self):
        self.temperature *= self.alpha
       # print(f"Temperatura: {self.temperature:.9f}",end="\r")

    def accept(self, candidate):
        
        candidate_sum = self.calculate_route(candidate)


        if candidate_sum < self.current_sum:
            self.current_sum = candidate_sum
            self.current_route = candidate
            if candidate_sum < self.best_sum:
                print(f"ZMIENIONO SUME Z {self.best_sum} na {candidate_sum} Lepszy Route: {candidate}")
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

    def run_algorythm(self):
        self.start_solution()
        self.start_epoch()
        self.start_temperature(self.current_sum,len(self.current_route))
        while self.temperature >= self.stop_temperature and self.i < self.stop_i:
            for i in range(self.epoch):
                old_candidate = list(self.current_route)

                candidate = self.inverse_solution(old_candidate)

                self.accept(candidate)
            self.cooldown()

            self.i += 1
            
        print(f'Sciezka: {self.best_route}\n Suma {self.best_sum}')

    def benchmark(self,sample):
        data = 0
        for i in range(sample):
            start_time = time.time()
            self.run_algorythm()
            end_time = time.time() - start_time
            data += end_time
        
def benchmark(sample):
    data = 0
    for i in range(sample):
        x = Wyrzazanie(alpha=0.99,stop_temperature=0.000000000001,epoch=5,stop_time=0,matrix=nodes,starting_point=0)
        start_time = time.time()
        x.run_algorythm()
        end_time = time.time()
        data+= end_time - start_time

def save_data():
    pass



# Czytanie pliku ini

def get_ini():
    tsp = {}
    with open("config.ini", 'r') as f:
        t = int(f.readline().strip())
        for i in range(t):
            print(i)
            x = f.readline().strip().split(" ")
            print(x)
            tsp[x[0]] = x[1]

        output = f.readline().strip()

    return tsp, output

# Czytanie plikow txt


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
        return l






if __name__ == '__main__':
    nodes = better_config("17.txt")

    #Wyrzazanie(alpha=0.99,stop_temperature=0.000000000001,epoch=5,stop_time=0,matrix=nodes,starting_point=0).run_algorythm()
    #x.run_algorythm()
    #benchmark(5)
    tsp,output = get_ini()
    print(tsp)
    print(output)
