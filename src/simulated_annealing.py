import math
import random
from copy import deepcopy
from scheduler import fitness

def make_neighbor(schedule):
    new_assignments = schedule.assignments.copy()
    a1_idx, a2_idx = random.sample(range(len(new_assignments)), 2)
    
    new_assignments[a1_idx].time_slot, new_assignments[a2_idx].time_slot = (
        new_assignments[a2_idx].time_slot,
        new_assignments[a1_idx].time_slot,
    )

    from models import Schedule
    return Schedule(new_assignments)

def simulated_annealing(initial_schedule, students, time_slots, rooms,
                        initial_temp=1000, cooling_rate=0.95, min_temp=1):
    
    current_schedule = deepcopy(initial_schedule)
    current_fitness = fitness(current_schedule, students)
    best_schedule = deepcopy(current_schedule)
    best_fitness = current_fitness

    temperature = initial_temp
    iteration = 0

    print(f"Initial fitness: {current_fitness}")

    while temperature > min_temp:
        # Membuat tetangga random
        neighbor = make_neighbor(current_schedule)

        neighbor_fitness = fitness(neighbor, students)
        delta = neighbor_fitness - current_fitness

        # Aturan penerimaan, hitung peluang dulu, lalu random pilih 0-1 buat bandingin
        if delta > 0 or random.random() < math.exp(delta / temperature):
            current_schedule = neighbor
            current_fitness = neighbor_fitness

            if current_fitness > best_fitness:
                best_schedule = deepcopy(current_schedule)
                best_fitness = current_fitness

        temperature *= cooling_rate
        iteration += 1

        if iteration % 100 == 0:
            print(f"Iter {iteration} | Temp={temperature:.2f} | BestFitness={best_fitness}")

    print(f"Final best fitness: {best_fitness}")
    return best_schedule, best_fitness
