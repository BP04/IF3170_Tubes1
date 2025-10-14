import time
import matplotlib.pyplot as plt
from typing import List, Dict
from models import *
from scheduler import objective, generate_initial_schedule
from utils import visualize_schedule
from hill_climbing import (
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    hill_climbing_with_sideways_moves,
    random_restart_hill_climbing
)
from genetic import genetic_algorithm
from simulated_annealing import simulated_annealing


def plot_objective_history(objective_history: List[float], title: str, xlabel: str = "Iteration", ylabel: str = "Objective Value") -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(objective_history, linewidth=2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_acceptance_probability(iterations: List[int], probabilities: List[float], title: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, probabilities, linewidth=2, alpha=0.7)
    plt.xlabel("Iteration")
    plt.ylabel("Acceptance Probability (e^(ΔE/T))")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_genetic_statistics(max_objective: List[float], avg_objective: List[float], title: str) -> None:
    plt.figure(figsize=(10, 6))
    generations: List[int] = list(range(len(max_objective)))
    plt.plot(generations, max_objective, label='Max Objective', linewidth=2)
    plt.plot(generations, avg_objective, label='Average Objective', linewidth=2, alpha=0.7)
    plt.xlabel("Generation")
    plt.ylabel("Objective Value")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def run_steepest_ascent(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student]) -> None:
    print("\n1. Steepest-Ascent Hill-Climbing")
    final_schedule: Schedule
    obj_history: List[float]
    iters: int
    duration: float
    final_schedule, obj_history, iters, duration = steepest_ascent_hill_climbing(
        courses, rooms, time_slots, students, max_iterations=1000, neighbors_to_check=50
    )
    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Iterations until stop: {iters}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_objective_history(obj_history, "Steepest-Ascent Hill-Climbing: Objective vs Iteration")

def run_stochastic(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student]) -> None:
    print("\n2. Stochastic Hill-Climbing")
    final_schedule: Schedule
    obj_history: List[float]
    iters: int
    duration: float
    final_schedule, obj_history, iters, duration = stochastic_hill_climbing(
        courses, rooms, time_slots, students, max_iterations=2000
    )
    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Iterations until stop: {iters}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_objective_history(obj_history, "Stochastic Hill-Climbing: Objective vs Iteration")

def run_sideways_moves(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student]) -> None:
    print("\n3. Hill-Climbing with Sideways Moves")
    final_schedule: Schedule
    obj_history: List[float]
    iters: int
    duration: float
    final_schedule, obj_history, iters, duration = hill_climbing_with_sideways_moves(
        courses, rooms, time_slots, students, max_iterations=1000, max_sideways_moves=100
    )
    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Iterations until stop: {iters}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_objective_history(obj_history, "Hill-Climbing with Sideways Moves: Objective vs Iteration")
    
def run_random_restart(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student]) -> None:
    print("\n4. Random-Restart Hill-Climbing")
    final_schedule: Schedule
    obj_history: List[float]
    total_iters: int
    duration: float
    num_restarts: int
    final_schedule, obj_history, total_iters, duration, num_restarts = random_restart_hill_climbing(
        courses, rooms, time_slots, students, num_restarts=5, max_iter_per_restart=200
    )
    print(f"\nFinal Result:")
    print(f"  - Global Best objective: {objective(final_schedule, students):.2f}")
    print(f"  - Number of Restarts: {num_restarts}")
    print(f"  - Total Iterations (sum over all restarts): {total_iters}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_objective_history(obj_history, "Random-Restart Hill-Climbing: Best Objective per Restart", 
                          xlabel="Restart Number")

def run_genetic_algorithm(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student]) -> None:
    print("\n5. Genetic Algorithm")

    start_time: float = time.time()
    final_schedule: Schedule
    statistics: Dict[str, List[float]]
    final_schedule, statistics = genetic_algorithm(
        courses, rooms, time_slots, students, population_size=100, generations=100
    )
    duration: float = time.time() - start_time

    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Population Size: 100, Generations: 100")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_genetic_statistics(statistics['max_objective'], statistics['avg_objective'],
                           "Genetic Algorithm: Max and Average Objective vs Generation")

def run_simulated_annealing(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], students: List[Student]) -> None:
    print("\n6. Simulated Annealing")
    initial_schedule: Schedule = generate_initial_schedule(courses, rooms, time_slots)
    
    start_time: float = time.time()
    final_schedule: Schedule
    final_objective: float
    accept_probs: List[float]
    iterations: List[int]
    stuck_count: int
    final_schedule, final_objective, accept_probs, iterations, stuck_count = simulated_annealing(
        initial_schedule, students, time_slots, rooms, 
        initial_temp=1000, cooling_rate=0.95, min_temp=1
    )
    duration: float = time.time() - start_time

    print(f"\nFinal Result:")
    print(f"  - Final objective: {final_objective:.2f}")
    print(f"  - Frequency of 'stuck' at local optima: {stuck_count}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    
    plot_acceptance_probability(iterations, accept_probs, 
                                "Simulated Annealing: Acceptance Probability (e^(ΔE/T)) vs Iteration")
