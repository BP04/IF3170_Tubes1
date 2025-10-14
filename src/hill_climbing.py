import copy
import random
from typing import Tuple, List, Dict
from models import *
from scheduler import *

def selection(population_objective: List[Tuple[Schedule, float]]) -> Schedule:
    # using roulette wheel selection

    max_absolute_objective: float = 0.0
    objective_scores: List[float] = []
    for _, objective_value in population_objective:
        max_absolute_objective = max(max_absolute_objective, abs(objective_value))
        objective_scores.append(objective_value)
    
    total_objective: float = 0.0
    for i in range(len(objective_scores)):
        objective_scores[i] += max_absolute_objective + 1
        total_objective += objective_scores[i]

    pick: float = random.random()

    sum: float = 0.0
    for i in range(len(objective_scores)):
        sum += objective_scores[i]
        if sum >= pick * total_objective:
            return population_objective[i][0]

    assert False

def crossover(parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
    child1: Schedule = copy.deepcopy(parent1)
    child2: Schedule = copy.deepcopy(parent2)

    crossover_point: int = random.randint(0, len(parent1.assignments) - 1)

    for i in range(crossover_point):
        child1.assignments[i].room, child2.assignments[i].room = child2.assignments[i].room, child1.assignments[i].room
        child1.assignments[i].time_slot, child2.assignments[i].time_slot = child2.assignments[i].time_slot, child1.assignments[i].time_slot
    
    return child1, child2

def mutation(schedule: Schedule, rooms: List[Room], time_slots: List[TimeSlot]) -> Schedule:
    return generate_neighbor(schedule, rooms, time_slots)

def genetic_algorithm(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student], population_size: int, generations: int) -> Tuple[Schedule, Dict[str, List[float]]]:
    population: List[Schedule] = initialize_population(courses, rooms, time_slots, population_size)
    population_objective: List[Tuple[Schedule, float]] = evaluate_population(population, students)

    max_objective_history: List[float] = []
    avg_objective_history: List[float] = []

    for _ in range(generations):
        # Track statistics
        objective_values: List[float] = [obj for _, obj in population_objective]
        max_objective_history.append(max(objective_values))
        avg_objective_history.append(sum(objective_values) / len(objective_values))

        new_population: List[Schedule] = []

        for _ in range(population_size // 2):
            parent1: Schedule = selection(population_objective)
            parent2: Schedule = selection(population_objective)

            child1: Schedule
            child2: Schedule
            child1, child2 = crossover(parent1, parent2)

            child1 = mutation(child1, rooms, time_slots)
            child2 = mutation(child2, rooms, time_slots)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population
        population_objective = evaluate_population(population, students)

    max_objective_index: int = 0
    for i in range(len(population_objective)):
        if population_objective[i][1] > population_objective[max_objective_index][1]:
            max_objective_index = i

    statistics: Dict[str, List[float]] = {
        'max_objective': max_objective_history,
        'avg_objective': avg_objective_history
    }

    return population_objective[max_objective_index][0], statistics