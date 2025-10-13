import math
import random
from copy import deepcopy
from scheduler import *

def simulated_annealing(
    initial_schedule,  
    students,          
    time_slots,        
    rooms,             
    initial_temp=1000,
    cooling_rate=0.95,
    min_temp=1
):
    current = deepcopy(initial_schedule)
    current_fitness = objective(current, students)
    best = deepcopy(current)
    best_fitness = current_fitness

    temp = initial_temp
    iteration = 0
    
    acceptance_probabilities = []
    iterations_list = []
    stuck_count = 0
    last_improvement_iter = 0

    while temp > min_temp:
        neighbor = generate_neighbor(current, rooms, time_slots)
        neighbor_fitness = objective(neighbor, students)
        delta = neighbor_fitness - current_fitness

        if delta > 0:
            accept_prob = 1.0
            acceptance_probabilities.append(accept_prob)
        else:
            accept_prob = math.exp(delta / temp)
            acceptance_probabilities.append(accept_prob)
        
        iterations_list.append(iteration)

        if delta > 0 or random.random() < math.exp(delta / temp):
            current = neighbor
            current_fitness = neighbor_fitness
            if current_fitness > best_fitness:
                best = deepcopy(current)
                best_fitness = current_fitness
                last_improvement_iter = iteration

        if iteration - last_improvement_iter >= 100:
            stuck_count += 1
            last_improvement_iter = iteration

        temp *= cooling_rate
        iteration += 1

    return best, best_fitness, acceptance_probabilities, iterations_list, stuck_count