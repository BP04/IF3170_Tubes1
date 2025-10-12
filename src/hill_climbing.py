import time
from models import *
from scheduler import fitness, generate_initial_schedule, generate_neighbor
from typing import List, Tuple

def steepest_ascent_hill_climbing(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student], max_iterations: int, neighbors_to_check: int) -> Tuple[Schedule, List[float], int, float]:
    start_time = time.time()
    
    current_schedule = generate_initial_schedule(courses, rooms, time_slots)
    current_fitness = fitness(current_schedule, students)
    fitness_history = [current_fitness]
    
    iterations = 0
    for i in range(max_iterations):
        iterations = i + 1
        best_neighbor = None
        best_neighbor_fitness = -float('inf')

        for _ in range(neighbors_to_check):
            neighbor = generate_neighbor(current_schedule, rooms, time_slots)
            neighbor_fitness = fitness(neighbor, students)
            if neighbor_fitness > best_neighbor_fitness:
                best_neighbor = neighbor
                best_neighbor_fitness = neighbor_fitness
        
        if best_neighbor_fitness > current_fitness:
            current_schedule = best_neighbor
            current_fitness = best_neighbor_fitness
            fitness_history.append(current_fitness)
        else:
            print(f"-> Steepest-Ascent: Local optimum reached at iteration {iterations}.")
            break

    duration = time.time() - start_time
    return current_schedule, fitness_history, iterations, duration

def stochastic_hill_climbing(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student], max_iterations: int) -> Tuple[Schedule, List[float], int, float]:
    start_time = time.time()

    current_schedule = generate_initial_schedule(courses, rooms, time_slots)
    current_fitness = fitness(current_schedule, students)
    fitness_history = [current_fitness]

    iterations = 0
    for i in range(max_iterations):
        iterations = i + 1
        
        neighbor = generate_neighbor(current_schedule, rooms, time_slots)
        neighbor_fitness = fitness(neighbor, students)

        if neighbor_fitness > current_fitness:
            current_schedule = neighbor
            current_fitness = neighbor_fitness
            fitness_history.append(current_fitness)

    duration = time.time() - start_time
    return current_schedule, fitness_history, iterations, duration

def hill_climbing_with_sideways_moves(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student], max_iterations: int, max_sideways_moves: int) -> Tuple[Schedule, List[float], int, float]:
    start_time = time.time()

    current_schedule = generate_initial_schedule(courses, rooms, time_slots)
    current_fitness = fitness(current_schedule, students)
    fitness_history = [current_fitness]
    
    sideways_moves_count = 0
    iterations = 0
    for i in range(max_iterations):
        iterations = i + 1
        best_neighbor = None
        best_neighbor_fitness = -float('inf')

        for _ in range(50):
            neighbor = generate_neighbor(current_schedule, rooms, time_slots)
            neighbor_fitness = fitness(neighbor, students)
            if neighbor_fitness > best_neighbor_fitness:
                best_neighbor = neighbor
                best_neighbor_fitness = neighbor_fitness
        
        if best_neighbor_fitness > current_fitness:
            current_schedule = best_neighbor
            current_fitness = best_neighbor_fitness
            fitness_history.append(current_fitness)
            sideways_moves_count = 0
        elif best_neighbor_fitness == current_fitness and sideways_moves_count < max_sideways_moves:
            current_schedule = best_neighbor
            current_fitness = best_neighbor_fitness
            fitness_history.append(current_fitness)
            sideways_moves_count += 1
        else:
            print(f"-> Sideways-Move: Optimum reached or sideways limit exceeded at iteration {iterations}.")
            break

    duration = time.time() - start_time
    return current_schedule, fitness_history, iterations, duration

def random_restart_hill_climbing(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student], num_restarts: int, max_iter_per_restart: int) -> Tuple[Schedule, List[float], int, float, int]:
    start_time = time.time()
    
    global_best_schedule = None
    global_best_fitness = -float('inf')
    total_iterations = 0
    
    print(f"Starting Random-Restart Hill-Climbing with {num_restarts} restarts.")
    for i in range(num_restarts):
        print(f"  -> Restart #{i + 1}/{num_restarts}...")
        
        schedule, _, iterations, _ = steepest_ascent_hill_climbing(
            courses, rooms, time_slots, students, 
            max_iterations=max_iter_per_restart, 
            neighbors_to_check=50
        )
        
        current_fitness = fitness(schedule, students)
        total_iterations += iterations
        
        if current_fitness > global_best_fitness:
            global_best_fitness = current_fitness
            global_best_schedule = schedule
            print(f"  -> New global best found with fitness: {global_best_fitness:.2f}")
    
    duration = time.time() - start_time
    return global_best_schedule, [], total_iterations, duration, num_restarts