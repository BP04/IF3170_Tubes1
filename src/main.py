from utils import *
from models import *
from scheduler import *
from simulated_annealing import simulated_annealing

def main():
    courses, rooms, students = load_data_from_json('../data/input.json')

    time_slots = [TimeSlot(day, hour) for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'] for hour in range(8, 17)]

    initial_schedule = generate_initial_schedule(courses, rooms, time_slots)
    initial_fitness = fitness(initial_schedule, students)

    print(f"Initial Schedule Fitness: {initial_fitness}")

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
