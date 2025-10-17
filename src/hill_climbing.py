import time
from models import *
from scheduler import objective, generate_initial_schedule, generate_neighbor
from typing import List, Tuple, Dict

def steepest_ascent_hill_climbing(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], 
                                  students: List[Student], lecturers: List[Lecturer],
                                  students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]],
                                  max_iterations: int, neighbors_to_check: int) -> Tuple[Schedule, List[float], int, float]:
    start_time: float = time.time()
    
    current_schedule: Schedule
    current_objective: float
    current_schedule, current_objective = generate_initial_schedule(courses, rooms, time_slots, students, lecturers, students_in_course, lecturers_in_course)
    objective_history: List[float] = [current_objective]
    
    iterations: int = 0
    for i in range(max_iterations):
        iterations = i + 1
        best_neighbor: Schedule | None = None
        best_neighbor_objective: float = -float('inf')

        for _ in range(neighbors_to_check):
            neighbor: Schedule
            neighbor_objective: float
            neighbor, neighbor_objective = generate_neighbor(current_schedule, rooms, time_slots, current_objective, students, lecturers, students_in_course, lecturers_in_course)
            if neighbor_objective > best_neighbor_objective:
                best_neighbor = neighbor
                best_neighbor_objective = neighbor_objective
        
        if best_neighbor_objective > current_objective:
            current_schedule = best_neighbor  # type: ignore
            current_objective = best_neighbor_objective
            objective_history.append(current_objective)
        else:
            print(f"-> Steepest-Ascent: Local optimum reached at iteration {iterations}.")
            break

    duration: float = time.time() - start_time
    return current_schedule, objective_history, iterations, duration

def stochastic_hill_climbing(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], 
                            students: List[Student], lecturers: List[Lecturer],
                            students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]],
                            max_iterations: int, max_stuck_iterations: int) -> Tuple[Schedule, List[float], int, float]:
    start_time: float = time.time()

    current_schedule: Schedule
    current_objective: float
    current_schedule, current_objective = generate_initial_schedule(courses, rooms, time_slots, students, lecturers, students_in_course, lecturers_in_course)
    objective_history: List[float] = [current_objective]

    iterations: int = 0
    stuck_count: int = 0

    for i in range(max_iterations):
        iterations = i + 1
        
        neighbor: Schedule
        neighbor_objective: float
        neighbor, neighbor_objective = generate_neighbor(current_schedule, rooms, time_slots, current_objective, students, lecturers, students_in_course, lecturers_in_course)

        if neighbor_objective > current_objective:
            current_schedule = neighbor
            current_objective = neighbor_objective
            objective_history.append(current_objective)
            stuck_count = 0
        else:
            stuck_count += 1

        if stuck_count >= max_stuck_iterations:
            print(f"-> Stochastic: Local optimum reached after {stuck_count} iterations without improvement.")
            break

    duration: float = time.time() - start_time
    return current_schedule, objective_history, iterations, duration

def hill_climbing_with_sideways_moves(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], 
                                     students: List[Student], lecturers: List[Lecturer],
                                     students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]],
                                     max_iterations: int, max_sideways_moves: int) -> Tuple[Schedule, List[float], int, float]:
    start_time: float = time.time()

    current_schedule: Schedule
    current_objective: float
    current_schedule, current_objective = generate_initial_schedule(courses, rooms, time_slots, students, lecturers, students_in_course, lecturers_in_course)
    objective_history: List[float] = [current_objective]
    
    sideways_moves_count: int = 0
    iterations: int = 0
    for i in range(max_iterations):
        iterations = i + 1
        best_neighbor: Schedule | None = None
        best_neighbor_objective: float = -float('inf')

        for _ in range(50):
            neighbor: Schedule
            neighbor_objective: float
            neighbor, neighbor_objective = generate_neighbor(current_schedule, rooms, time_slots, current_objective, students, lecturers, students_in_course, lecturers_in_course)
            if neighbor_objective > best_neighbor_objective:
                best_neighbor = neighbor
                best_neighbor_objective = neighbor_objective
        
        if best_neighbor_objective > current_objective:
            assert best_neighbor is not None # make sure best_neighbor is not None before use
            current_schedule = best_neighbor
            current_objective = best_neighbor_objective
            objective_history.append(current_objective)
            sideways_moves_count = 0
        elif best_neighbor_objective == current_objective and sideways_moves_count < max_sideways_moves:
            assert best_neighbor is not None # make sure best_neighbor is not None before use
            current_schedule = best_neighbor
            current_objective = best_neighbor_objective
            objective_history.append(current_objective)
            sideways_moves_count += 1
        else:
            print(f"-> Sideways-Move: Optimum reached or sideways limit exceeded at iteration {iterations}.")
            break

    duration: float = time.time() - start_time
    return current_schedule, objective_history, iterations, duration

def random_restart_hill_climbing(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], 
                                students: List[Student], lecturers: List[Lecturer],
                                students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]],
                                num_restarts: int, max_iter_per_restart: int) -> Tuple[Schedule, List[float], int, float, int]:
    start_time: float = time.time()
    
    global_best_schedule: Schedule | None = None
    global_best_objective: float = -float('inf')
    total_iterations: int = 0
    objective_history_per_restart: List[float] = []
    
    print(f"Starting Random-Restart Hill-Climbing with {num_restarts} restarts.")
    for i in range(num_restarts):
        print(f"  -> Restart #{i + 1}/{num_restarts}...")
        
        schedule: Schedule
        _: List[float]
        iterations: int
        schedule, _, iterations, _ = steepest_ascent_hill_climbing(
            courses, rooms, time_slots, students, lecturers, students_in_course, lecturers_in_course,
            max_iterations=max_iter_per_restart, 
            neighbors_to_check=50
        )
        
        current_objective: float = objective(schedule, students, lecturers, students_in_course, lecturers_in_course)
        total_iterations += iterations
        
        if current_objective > global_best_objective:
            global_best_objective = current_objective
            global_best_schedule = schedule
            print(f"  -> New global best found with objective: {global_best_objective:.2f}")
            
        objective_history_per_restart.append(global_best_objective)
    
    duration: float = time.time() - start_time
    return global_best_schedule, objective_history_per_restart, total_iterations, duration, num_restarts