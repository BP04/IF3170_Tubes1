from typing import List
from utils import load_data_from_json, visualize_schedule
from models import *
from scheduler import objective, generate_initial_schedule
from runners import (
    run_steepest_ascent,
    run_steepest_ascent_full,
    run_stochastic,
    run_sideways_moves,
    run_sideways_moves_full,
    run_random_restart,
    run_genetic_algorithm,
    run_simulated_annealing
)

def main() -> None:
    courses: List[Course]
    rooms: List[Room]
    students: List[Student]
    lecturers: List[Lecturer]
    
    while True:
        file_options = {
            '1': '../data/input.json',
            '2': '../data/semi_large_test.json',
            '3': '../data/large_test.json'
        }
        
        print("\n" + "~"*75)
        print(" Please select the input file to use for this session:")
        print("~"*75)
        print("  1. Standard Test (input.json)")
        print("  2. Semi-Large Test (semi_large_test.json)")
        print("  3. Large Test (large_test.json)")
        print("  4. Enter a custom file path")
        print("  5. Exit Program")
        print("~"*75)
        
        file_choice = input("Enter your choice (1-5): ")

        file_to_load = ""
        if file_choice in file_options:
            file_to_load = file_options[file_choice]
        elif file_choice == '4':
            print("  Add '../data/' as the beginning of the path if the file is in the data folder.")
            file_to_load = input("  Enter the custom file path: ")
        elif file_choice == '5':
            print("Exiting program.")
            return
        else:
            print("Invalid choice. Please try again.")
            continue

        courses, rooms, students, lecturers = load_data_from_json(file_to_load)

        if courses:
            print(f"-> File '{file_to_load}' loaded successfully.\n")
            break
        else:
            print("Please check the path and try again.")

    time_slots: List[TimeSlot] = [TimeSlot(day, hour) for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'] 
                                   for hour in range(8, 17)]
    initial_schedule: Schedule = generate_initial_schedule(courses, rooms, time_slots)
    
    while True:
        print("\n" + "~"*75)
        print(" Solving the Weekly Class Scheduling Problem with Local Search Algorithms")
        print("         Developed by: Tubes1 - K1 (13523019, 13523059, 13523067)")
        print("~"*75)
        print("  1. Steepest-Ascent Hill-Climbing (Sampling)")
        print("  2. Steepest-Ascent Hill-Climbing (Full)")
        print("  3. Stochastic Hill-Climbing")
        print("  4. Hill-Climbing with Sideways Moves (Sampling)")
        print("  5. Hill-Climbing with Sideways Moves (Full)")
        print("  6. Random-Restart Hill-Climbing")
        print("  7. Genetic Algorithm")
        print("  8. Simulated Annealing")
        print("  9. Run All Algorithms Sequentially")
        print(" 10. Exit")
        print("~"*75)
        
        print()
        print("Initial State:")
        print(f"Initial Objective: {objective(initial_schedule, students, lecturers):.2f}")
        visualize_schedule(initial_schedule, rooms)
        print()

        algo_choice: str = input("Enter your choice (1-10): ")

        if algo_choice == '1':
            run_steepest_ascent(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '2':
            run_steepest_ascent_full(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '3':
            run_stochastic(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '4':
            run_sideways_moves(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '5':
            run_sideways_moves_full(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '6':
            run_random_restart(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '7':
            run_genetic_algorithm(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '8':
            run_simulated_annealing(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '9':
            run_steepest_ascent(courses, rooms, time_slots, students, lecturers)
            run_steepest_ascent_full(courses, rooms, time_slots, students, lecturers)
            run_stochastic(courses, rooms, time_slots, students, lecturers)
            run_sideways_moves(courses, rooms, time_slots, students, lecturers)
            run_sideways_moves_full(courses, rooms, time_slots, students, lecturers)
            run_random_restart(courses, rooms, time_slots, students, lecturers)
            run_genetic_algorithm(courses, rooms, time_slots, students, lecturers)
            run_simulated_annealing(courses, rooms, time_slots, students, lecturers)
        elif algo_choice == '10':
            print("Thank you for using this program. See you next time!" + "\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()