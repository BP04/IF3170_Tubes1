from utils import *
from models import *
from scheduler import *

def main():
    courses, rooms, students = load_data_from_json('../data/input.json')

    time_slots = [
        TimeSlot('Senin', 8, 'Senin', 10),
        TimeSlot('Senin', 10, 'Senin', 12),
        TimeSlot('Senin', 13, 'Senin', 15),
        TimeSlot('Senin', 15, 'Senin', 17),
        TimeSlot('Selasa', 8, 'Selasa', 10),
        TimeSlot('Selasa', 10, 'Selasa', 12),
        TimeSlot('Selasa', 13, 'Selasa', 15),
        TimeSlot('Selasa', 15, 'Selasa', 17),
        TimeSlot('Rabu', 8, 'Rabu', 10),
        TimeSlot('Rabu', 10, 'Rabu', 12),
        TimeSlot('Rabu', 13, 'Rabu', 15),
        TimeSlot('Rabu', 15, 'Rabu', 17),
        TimeSlot('Kamis', 8, 'Kamis', 10),
        TimeSlot('Kamis', 10, 'Kamis', 12),
        TimeSlot('Kamis', 13, 'Kamis', 15),
        TimeSlot('Kamis', 15, 'Kamis', 17),
        TimeSlot('Jumat', 8, 'Jumat', 10),
        TimeSlot('Jumat', 10, 'Jumat', 12),
        TimeSlot('Jumat', 13, 'Jumat', 15),
        TimeSlot('Jumat', 15, 'Jumat', 17),
    ]

    initial_schedule = generate_initial_schedule(courses, rooms, time_slots)
    initial_fitness = fitness(initial_schedule, students)

    print(f"Initial Schedule Fitness: {initial_fitness}")

if __name__ == "__main__":
    main()