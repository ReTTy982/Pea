import math
import random
from typing import DefaultDict
INT_MAX = 2147483647

class Wyrzazanie():
    def __init__(self,alpha,temperature):
        self.temperature = temperature
        self.alpha = alpha
        self.best_route = []
        self.stop_i = 10000
        

    def start_solution(self,matrix,starting_point):
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
                    route[counter] = j # oryginal
    
            j += 1
    
            # Check all paths from the
            # ith indexed city
            if j == len(matrix[i]):
                sum += min
                min = INT_MAX
                visitedRouteList[route[counter]] = 1 #tutaj 
                j = 0
                i = route[counter] # tutaj 
                counter += 1
    
        # Update the ending city in array
        # from city which was last visited
        i = route[counter - 1]
        min = matrix[i][starting_point]
        route[counter] = starting_point
        sum += min
    
        # Started from the node where
        # we finished as well.
        print("Minimum Cost is :", sum)
        return route, sum

    def nearest_neighbour(self):
        pass

    def distance(self):
        pass

    def inverse_solution(self,matrix):
        pass
    
    def probability(self):
        pass


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

def inverse(state):
    "Inverses the order of cities in a route between node one and node two"
   
    node_one = random.choice(state)
    new_list = list(filter(lambda city: city != node_one, state)) #route without the selected node one
    node_two = random.choice(new_list)
    state[min(node_one,node_two):max(node_one,node_two)] = state[min(node_one,node_two):max(node_one,node_two)][::-1]
    
    return state

def calculate_route(route,matrix):
    sum = 0
    previous = route[-1]
    for i in range(len(matrix)):
        sum += matrix[previous][route[i]]
        previous = route[i]
    return sum

if __name__ == '__main__':
   nodes=  better_config("6_1.txt")

   x= Wyrzazanie()
   route,sum = x.start_solution(nodes,0)
   print(route)
   print(sum)
   y = inverse(route)
   z = calculate_route(y,nodes)

   print(y)
   print(z)