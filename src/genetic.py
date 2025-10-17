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

def crossover(parent1: Schedule, parent2: Schedule, students: List[Student], lecturers: List[Lecturer]) -> Tuple[Schedule, Schedule]:
    child1: Schedule = copy.deepcopy(parent1)
    child2: Schedule = copy.deepcopy(parent2)

    crossover_point: int = random.randint(0, len(parent1.assignments) - 1)

    for i in range(crossover_point):
        child1.assignments[i].room, child2.assignments[i].room = child2.assignments[i].room, child1.assignments[i].room
        child1.assignments[i].time_slot, child2.assignments[i].time_slot = child2.assignments[i].time_slot, child1.assignments[i].time_slot
    
    child1 = Schedule(child1.assignments, students, lecturers)
    child2 = Schedule(child2.assignments, students, lecturers)
    
    return child1, child2

def mutation(schedule: Schedule, rooms: List[Room], time_slots: List[TimeSlot],
             current_objective: float, students: List[Student], lecturers: List[Lecturer],
             students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]]) -> Tuple[Schedule, float]:
    return generate_neighbor(schedule, rooms, time_slots, current_objective, students, lecturers, students_in_course, lecturers_in_course)

def genetic_algorithm(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], 
                     students: List[Student], lecturers: List[Lecturer],
                     students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]],
                     population_size: int, generations: int) -> Tuple[Schedule, Dict[str, List[float]]]:
    population_objective: List[Tuple[Schedule, float]] = initialize_population(courses, rooms, time_slots, students, lecturers, students_in_course, lecturers_in_course, population_size)

    max_objective_history: List[float] = []
    avg_objective_history: List[float] = []

    best_schedule: Tuple[Schedule, float] = population_objective[0]

    for _ in range(generations):
        # Track statistics
        objective_values: List[float] = [obj for _, obj in population_objective]
        max_objective_history.append(max(objective_values))
        avg_objective_history.append(sum(objective_values) / len(objective_values))

        new_population_objective: List[Tuple[Schedule, float]] = []

        for _ in range(population_size // 2):
            parent1: Schedule = selection(population_objective)
            parent2: Schedule = selection(population_objective)

            child1: Schedule
            child2: Schedule
            child1, child2 = crossover(parent1, parent2, students, lecturers)

            child1_obj: float = objective(child1, students, lecturers, students_in_course, lecturers_in_course)
            child2_obj: float = objective(child2, students, lecturers, students_in_course, lecturers_in_course)

            child1, child1_obj = mutation(child1, rooms, time_slots, child1_obj, students, lecturers, students_in_course, lecturers_in_course)
            child2, child2_obj = mutation(child2, rooms, time_slots, child2_obj, students, lecturers, students_in_course, lecturers_in_course)

            new_population_objective.append((child1, child1_obj))
            if len(new_population_objective) < population_size:
                new_population_objective.append((child2, child2_obj))

        population_objective = new_population_objective

        for i in range(len(population_objective)):
            if best_schedule[1] < population_objective[i][1]:
                best_schedule = population_objective[i]

    statistics: Dict[str, List[float]] = {
        'max_objective': max_objective_history,
        'avg_objective': avg_objective_history
    }

    return best_schedule[0], statistics