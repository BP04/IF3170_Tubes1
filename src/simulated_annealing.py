import math
import random
from copy import deepcopy
from scheduler import *
from typing import List, Tuple, Dict

def simulated_annealing(initial_schedule: Schedule, initial_objective: float,
                        students: List[Student], lecturers: List[Lecturer],
                        students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]],
                        time_slots: List[TimeSlot], rooms: List[Room], 
                        initial_temp: float = 1000, cooling_rate: float = 0.95,
                        min_temp: float = 1) -> Tuple[Schedule, float, List[float], List[int], int]:
    current: Schedule = deepcopy(initial_schedule)
    current_objective: float = initial_objective
    best: Schedule = deepcopy(current)
    best_objective: float = current_objective

    temp: float = initial_temp
    iteration: int = 0
    
    acceptance_probabilities: List[float] = []
    iterations_list: List[int] = []
    stuck_count: int = 0
    last_improvement_iter: int = 0

    while temp > min_temp:
        neighbor: Schedule
        neighbor_objective: float
        neighbor, neighbor_objective = generate_neighbor(current, rooms, time_slots, current_objective, students, lecturers, students_in_course, lecturers_in_course)
        delta: float = neighbor_objective - current_objective

        accept_prob: float
        if delta > 0:
            accept_prob = 1.0
            acceptance_probabilities.append(accept_prob)
        else:
            accept_prob = math.exp(delta / temp)
            acceptance_probabilities.append(accept_prob)
        
        iterations_list.append(iteration)

        if delta > 0 or random.random() < math.exp(delta / temp):
            current = neighbor
            current_objective = neighbor_objective
            if current_objective > best_objective:
                best = deepcopy(current)
                best_objective = current_objective
                last_improvement_iter = iteration

        if iteration - last_improvement_iter >= 100:
            stuck_count += 1
            last_improvement_iter = iteration

        temp *= cooling_rate
        iteration += 1

    return best, best_objective, acceptance_probabilities, iterations_list, stuck_count