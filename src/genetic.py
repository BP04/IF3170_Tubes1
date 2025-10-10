import copy
import random
from typing import Tuple, List
from models import *
from scheduler import *

def selection(population_fitness: List[Tuple[Schedule, int]]) -> Schedule:
    # using roulette wheel selection

    max_absolute_fitness = 0
    fitness_scores = []
    for _, fitness in population_fitness:
        max_absolute_fitness = max(max_absolute_fitness, abs(fitness))
        fitness_scores.append(fitness)
    
    total_fitness = 0
    for i in range(len(fitness_scores)):
        fitness_scores[i] += max_absolute_fitness + 1
        total_fitness += fitness_scores[i]

    pick = random.random()

    sum = 0
    for i in range(len(fitness_scores)):
        sum += fitness_scores[i]
        if sum >= pick * total_fitness:
            return population_fitness[i][0]

    assert False

def crossover(parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    crossover_point = random.randint(0, len(parent1.assignments) - 1)

    for i in range(crossover_point):
        child1.assignments[i].room, child2.assignments[i].room = child2.assignments[i].room, child1.assignments[i].room
        child1.assignments[i].time_slot, child2.assignments[i].time_slot = child2.assignments[i].time_slot, child1.assignments[i].time_slot
    
    return child1, child2

def mutation(schedule: Schedule, rooms: List[Room], time_slots: List[TimeSlot]) -> Schedule:
    return generate_neighbor(schedule, rooms, time_slots)

def genetic_algorithm(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student], population_size: int, generations: int) -> Schedule:
    population = initialize_population(courses, rooms, time_slots, population_size)
    population_fitness = evaluate_population(population, students)

    for _ in range(generations):
        new_population = []

        for _ in range(population_size // 2):
            parent1 = selection(population_fitness)
            parent2 = selection(population_fitness)

            child1, child2 = crossover(parent1, parent2)

            child1 = mutation(child1, rooms, time_slots)
            child2 = mutation(child2, rooms, time_slots)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population
        population_fitness = evaluate_population(population, students)

    max_fitness_index = 0
    for i in range(len(population_fitness)):
        if population_fitness[i][1] > population_fitness[max_fitness_index][1]:
            max_fitness_index = i

    return population_fitness[max_fitness_index][0]