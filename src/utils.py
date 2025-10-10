import json
from typing import List, Tuple, Dict
from models import *

def load_data_from_json(file_path: str) -> Tuple[List[Course], List[Room], List[Student]]:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return [], [], []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return [], [], []   

    courses = [Course(c['kode'], c['jumlah_mahasiswa'], c['sks']) for c in data['kelas_mata_kuliah']]
    rooms = [Room(r['kode'], r['kuota']) for r in data['ruangan']]
    students = [Student(s['nim'], s['daftar_mk'], s['prioritas']) for s in data['mahasiswa']]

    return courses, rooms, students

def schedule_table_for_room(schedule: Schedule, room_id: str):
    day_to_index: Dict[str, int] = {'Senin': 0, 'Selasa': 1, 'Rabu': 2, 'Kamis': 3, 'Jumat': 4}

    time_to_courses: Dict[int, List[str]] = {}
    for assignment in schedule.assignments:
        if assignment.room.room_id != room_id:
            continue

        hour_index = assignment.time_slot.hour_index()
        course_id = assignment.course.course_id
        if hour_index not in time_to_courses:
            time_to_courses[hour_index] = []
        time_to_courses[hour_index].append(course_id)

    print("              |   Senin    |   Selasa   |    Rabu    |   Kamis    |   Jumat    |")

    for hour in range(8, 17):
        print(80 * '-')
        print(f"{hour:02d}:00 - {hour + 1:02d}:00 ", end="")

        max_course_on_hour = 1
        for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']:
            hour_index = day_to_index[day] * 24 + hour
            if hour_index in time_to_courses:
                max_course_on_hour = max(max_course_on_hour, len(time_to_courses[hour_index]))

        first = True
        for _ in range(max_course_on_hour):
            if not first:
                print()
                print(14 * ' ', end="")
            else:
                first = False

            for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']:
                hour_index = day_to_index[day] * 24 + hour

                if hour_index in time_to_courses:
                    print("|", end="")
                    print(f" {time_to_courses[hour_index][0]} ", end="")
                    
                    time_to_courses[hour_index].pop(0)
                    if len(time_to_courses[hour_index]) == 0:
                        time_to_courses.pop(hour_index)
                else:
                    print("|            ", end="")
            print("|", end="")
        
        print()
        
    print()

def visualize_schedule(schedule: Schedule, rooms: List[Room]):
    for room in rooms:
        print(f"Ruangan {room.room_id}:")
        schedule_table_for_room(schedule, room.room_id)
        print()