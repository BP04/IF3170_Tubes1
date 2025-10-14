from typing import List
from utils import load_data_from_json, visualize_schedule
from models import *
from scheduler import objective, generate_initial_schedule
from runners import (
    run_steepest_ascent,
    run_stochastic,
    run_sideways_moves,
    run_random_restart,
    run_genetic_algorithm,
    run_simulated_annealing
)

def main() -> None:
    courses: List[Course]
    rooms: List[Room]
    students: List[Student]
    courses, rooms, students = load_data_from_json('./data/input.json')
    time_slots: List[TimeSlot] = [TimeSlot(day, hour) for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'] 
                  for hour in range(8, 17)]
    
    while True:
        initial_schedule: Schedule = generate_initial_schedule(courses, rooms, time_slots)

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

        choice: str = input("Enter your choice (1-8): ")

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

        print("KELAR")

if __name__ == "__main__":
    main()