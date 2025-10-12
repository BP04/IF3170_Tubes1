import copy
import random
from typing import Tuple, List
from models import *
from scheduler import *

def selection(population_fitness: List[Tuple[Schedule, float]]) -> Schedule:
    # using roulette wheel selection
    
    fitness_scores = [fit for _, fit in population_fitness]
    min_fitness = min(fitness_scores)
    adjusted_scores = [(score - min_fitness) + 1 for score in fitness_scores]
    total_fitness = sum(adjusted_scores)

    if total_fitness == 0:
        return random.choice(population_fitness)[0]

    pick = random.uniform(0, total_fitness)
    current = 0
    for i, schedule_fitness in enumerate(population_fitness):
        current += adjusted_scores[i]
        if current > pick:
            return schedule_fitness[0]
    
    return population_fitness[-1][0]

def crossover(parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    num_assignments = len(parent1.assignments)

    if num_assignments < 2:
        return child1, child2

    crossover_point = random.randint(1, num_assignments - 1)

    for i in range(crossover_point):
        child1.assignments[i], child2.assignments[i] = child2.assignments[i], child1.assignments[i]
    
    return Schedule(child1.assignments), Schedule(child2.assignments)

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