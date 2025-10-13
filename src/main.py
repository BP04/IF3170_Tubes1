import time
from utils import *
from models import *
from scheduler import *
from simulated_annealing import simulated_annealing

def main():
    courses, rooms, students = load_data_from_json('../data/input.json')

    start_time = time.time()
    final_schedule = genetic_algorithm(courses, rooms, time_slots, students, population_size=100, generations=100)
    duration = time.time() - start_time

    print(f"\nFinal Result:")
    print(f"  - Final objective: {objective(final_schedule, students):.2f}")
    print(f"  - Population Size: 100, Generations: 100")
    print(f"  - Search Duration: {duration:.4f} seconds")
    visualize_schedule(final_schedule, rooms)

def main():
    courses, rooms, students = load_data_from_json('../data/input.json')
    time_slots = [TimeSlot(day, hour) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] for hour in range(8, 17)]
    initial_schedule = generate_initial_schedule(courses, rooms, time_slots)
    
    while True:
        print("\n" + "~"*75)
        print(" Solving the Weekly Class Scheduling Problem with Local Search Algorithms")
        print("         Developed by: Tubes1 - K1 (13523019, 13523059, 13523067)")
        print("~"*75)
        print("  1. Steepest-Ascent Hill-Climbing")
        print("  2. Stochastic Hill-Climbing")
        print("  3. Hill-Climbing with Sideways Moves")
        print("  4. Random-Restart Hill-Climbing")
        print("  5. Genetic Algorithm")
        print("  6. Run All Algorithms Sequentially")
        print("  7. Exit")
        print("~"*75)
        
        print()
        print("Initial State:")
        visualize_schedule(initial_schedule, rooms)
        print()

        choice = input("Enter your choice (1-7): ")

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
            run_steepest_ascent(courses, rooms, time_slots, students)
            run_stochastic(courses, rooms, time_slots, students)
            run_sideways_moves(courses, rooms, time_slots, students)
            run_random_restart(courses, rooms, time_slots, students)
            run_genetic_algorithm(courses, rooms, time_slots, students)
        elif choice == '7':
            print("Thank you for using this program. See you next time!" + "\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

    print("\nPilih algoritma:")
    print("1. Hill Climbing")
    print("2. Simulated Annealing")
    print("3. Genetic Algorithm")

    choice = input("Masukkan nomor algoritma: ")

    if choice == "1":
        print("Hill Climbing belum diimplementasikan.")
    elif choice == "2":
        simulated_annealing(initial_schedule, students, time_slots, rooms)
    elif choice == "3":
        print("Genetic Algorithm belum diimplementasikan.")
    else:
        print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
