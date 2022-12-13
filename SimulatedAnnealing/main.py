import math
import decimal
import random
from typing import DefaultDict
INT_MAX = 2147483647


class Wyrzazanie():
    def __init__(self, alpha, stop_temperature,epoch):
        self.temperature = None
        self.alpha = alpha
        self.best_route = None
        self.best_sum = INT_MAX
        self.stop_i = 10000
        self.stop_temperature = stop_temperature
        self.i = 1
        self.epoch = epoch

    def start_temperature(self,sum,vertex):
        self.temperature = sum*vertex
        
        


    def start_solution(self, matrix, starting_point):
        sum = 0
        counter = 0
        j = 0
        i = 0
        min = INT_MAX
        visitedRouteList = DefaultDict(int)

        # Starting from the 0th indexed
        # city i.e., the first city
        visitedRouteList[starting_point] = 1
        route = [0] * len(matrix)

        # Traverse the adjacency
        # matrix tsp[][]
        while i < len(matrix) and j < len(matrix[i]):

            # Corner of the Matrix
            if counter >= len(matrix[i]) - 1:
                break

            # If this path is unvisited then
            # and if the cost is less then
            # update the cost
            if j != i and (visitedRouteList[j] == 0):
                if matrix[i][j] < min:
                    min = matrix[i][j]
                    route[counter] = j  # oryginal

            j += 1

            # Check all paths from the
            # ith indexed city
            if j == len(matrix[i]):
                sum += min
                min = INT_MAX
                visitedRouteList[route[counter]] = 1  # tutaj
                j = 0
                i = route[counter]  # tutaj
                counter += 1

        # Update the ending city in array
        # from city which was last visited
        i = route[counter - 1]
        min = matrix[i][starting_point]
        route[counter] = starting_point
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

    def accept(self, candidate,matrix):
        
        candidate_sum = self.calculate_route(candidate,matrix)
        test = self.best_route


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

    def calculate_route(self, route, matrix):
        sum = 0
        previous = route[-1]
        for i in range(len(matrix)):
            sum += matrix[previous][route[i]]
            previous = route[i]
        return sum

    def run_algorythm(self, matrix, starting_poing):
        self.start_solution(matrix, starting_poing)
        self.start_temperature(self.current_sum,len(self.current_route))
        while self.temperature >= self.stop_temperature and self.i < self.stop_i:
            for i in range(self.epoch):
                old_candidate = list(self.current_route)

                candidate = self.inverse_solution(old_candidate)

                self.accept(candidate,matrix)
            self.cooldown()

            self.i += 1
                

            
            
            

        
        print(f'Sciezka: {self.best_route}\n Suma {self.best_sum}')
        


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




def calculate_route(route, matrix):
    sum = 0
    previous = route[-1]
    for i in range(len(matrix)):
        sum += matrix[previous][route[i]]
        previous = route[i]
    return sum


if __name__ == '__main__':
    nodes = better_config("33.txt")

    x = Wyrzazanie(0.99,0.000000001,4000)
    x.run_algorythm(nodes,3)
    
