from utils import *
from models import *
from scheduler import *
from genetic import *

def main():
    courses, rooms, students = load_data_from_json('data/input.json')

    time_slots = [TimeSlot(day, hour) for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'] for hour in range(8, 17)]
    # time_slots = [TimeSlot(day, hour) for day in ['Senin', 'Selasa'] for hour in range(8, 9)]

    final_schedule = genetic_algorithm(courses, rooms, time_slots, students, 100, 100)

    visualize_schedule(final_schedule, rooms)

if __name__ == "__main__":
    main()