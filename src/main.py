from utils import *
from models import *
from scheduler import *

def main():
    courses, rooms, students = load_data_from_json('data/input.json')

    time_slots = [TimeSlot(day, hour) for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'] for hour in range(8, 17)]

    initial_schedule = generate_initial_schedule(courses, rooms, time_slots)
    initial_fitness = fitness(initial_schedule, students)

    print(f"Initial Schedule Fitness: {initial_fitness}")

if __name__ == "__main__":
    main()