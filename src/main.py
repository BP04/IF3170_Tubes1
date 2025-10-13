import time
import matplotlib.pyplot as plt
from utils import *
from models import *
from scheduler import *
from hill_climbing import (
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    hill_climbing_with_sideways_moves,
    random_restart_hill_climbing
)
from genetic import genetic_algorithm
from simulated_annealing import simulated_annealing

def plot_objective_history(objective_history, title, xlabel="Iteration", ylabel="Objective Value"):
    plt.figure(figsize=(10, 6))
    plt.plot(objective_history, linewidth=2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_acceptance_probability(iterations, probabilities, title):
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, probabilities, linewidth=2, alpha=0.7)
    plt.xlabel("Iteration")
    plt.ylabel("Acceptance Probability (e^(ΔE/T))")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_genetic_statistics(max_fitness, avg_fitness, title):
    plt.figure(figsize=(10, 6))
    generations = list(range(len(max_fitness)))
    plt.plot(generations, max_fitness, label='Max Fitness', linewidth=2)
    plt.plot(generations, avg_fitness, label='Average Fitness', linewidth=2, alpha=0.7)
    plt.xlabel("Generation")
    plt.ylabel("Fitness Value")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def run_steepest_ascent(courses, rooms, time_slots, students):
    print("\n1. Steepest-Ascent Hill-Climbing")
    final_schedule, obj_history, iters, duration = steepest_ascent_hill_climbing(
        courses, rooms, time_slots, students, max_iterations=1000, neighbors_to_check=50
    )
    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Iterations until stop: {iters}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_objective_history(obj_history, "Steepest-Ascent Hill-Climbing: Objective vs Iteration")

def run_stochastic(courses, rooms, time_slots, students):
    print("\n2. Stochastic Hill-Climbing")
    final_schedule, obj_history, iters, duration = stochastic_hill_climbing(
        courses, rooms, time_slots, students, max_iterations=2000
    )
    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Iterations until stop: {iters}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_objective_history(obj_history, "Stochastic Hill-Climbing: Objective vs Iteration")

def run_sideways_moves(courses, rooms, time_slots, students):
    print("\n3. Hill-Climbing with Sideways Moves")
    final_schedule, obj_history, iters, duration = hill_climbing_with_sideways_moves(
        courses, rooms, time_slots, students, max_iterations=1000, max_sideways_moves=100
    )
    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Iterations until stop: {iters}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_objective_history(obj_history, "Hill-Climbing with Sideways Moves: Objective vs Iteration")
    
def run_random_restart(courses, rooms, time_slots, students):
    print("\n4. Random-Restart Hill-Climbing")
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

def run_genetic_algorithm(courses, rooms, time_slots, students):
    print("\n5. Genetic Algorithm")

    start_time = time.time()
    final_schedule, statistics = genetic_algorithm(
        courses, rooms, time_slots, students, population_size=100, generations=100
    )
    duration = time.time() - start_time

    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Population Size: 100, Generations: 100")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    plot_genetic_statistics(statistics['max_fitness'], statistics['avg_fitness'],
                           "Genetic Algorithm: Max and Average Fitness vs Generation")

def run_simulated_annealing(courses, rooms, time_slots, students):
    print("\n6. Simulated Annealing")
    initial_schedule = generate_initial_schedule(courses, rooms, time_slots)
    
    start_time = time.time()
    final_schedule, final_fitness, accept_probs, iterations, stuck_count = simulated_annealing(
        initial_schedule, students, time_slots, rooms, 
        initial_temp=1000, cooling_rate=0.95, min_temp=1
    )
    duration = time.time() - start_time

    print(f"\nFinal Result:")
    print(f"  - Final objective: {final_fitness:.2f}")
    print(f"  - Frequency of 'stuck' at local optima: {stuck_count}")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)
    
    plot_acceptance_probability(iterations, accept_probs, 
                                "Simulated Annealing: Acceptance Probability (e^(ΔE/T)) vs Iteration")

def main():
    courses, rooms, students = load_data_from_json('../data/input.json')
    time_slots = [TimeSlot(day, hour) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] 
                  for hour in range(8, 17)]
    
    while True:
        initial_schedule = generate_initial_schedule(courses, rooms, time_slots)
        
        print("\n" + "~"*75)
        print(" Solving the Weekly Class Scheduling Problem with Local Search Algorithms")
        print("         Developed by: Tubes1 - K1 (13523019, 13523059, 13523067)")
        print("~"*75)
        print("  1. Steepest-Ascent Hill-Climbing")
        print("  2. Stochastic Hill-Climbing")
        print("  3. Hill-Climbing with Sideways Moves")
        print("  4. Random-Restart Hill-Climbing")
        print("  5. Genetic Algorithm")
        print("  6. Simulated Annealing")
        print("  7. Run All Algorithms Sequentially")
        print("  8. Exit")
        print("~"*75)
        
        print()
        print("Initial State:")
        print(f"Initial Objective: {objective(initial_schedule, students):.2f}")
        visualize_schedule(initial_schedule, rooms)
        print()

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            run_steepest_ascent(courses, rooms, time_slots, students)
        elif choice == '2':
            run_stochastic(courses, rooms, time_slots, students)
        elif choice == '3':
            run_sideways_moves(courses, rooms, time_slots, students)
        elif choice == '4':
            run_random_restart(courses, rooms, time_slots, students)
        elif choice == '5':
            run_genetic_algorithm(courses, rooms, time_slots, students)
        elif choice == '6':
            run_simulated_annealing(courses, rooms, time_slots, students)
        elif choice == '7':
            run_steepest_ascent(courses, rooms, time_slots, students)
            run_stochastic(courses, rooms, time_slots, students)
            run_sideways_moves(courses, rooms, time_slots, students)
            run_random_restart(courses, rooms, time_slots, students)
            run_genetic_algorithm(courses, rooms, time_slots, students)
            run_simulated_annealing(courses, rooms, time_slots, students)
        elif choice == '8':
            print("Thank you for using this program. See you next time!" + "\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()