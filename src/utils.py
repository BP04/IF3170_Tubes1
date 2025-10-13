import json
import sys
from typing import List, Tuple, Dict
from models import *

def load_data_from_json(file_path: str) -> Tuple[List[Course], List[Room], List[Student]]:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"\nError: File '{file_path}' is not found.")
        print("Make sure the location of the 'input.json' file is correct within main.py.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
        sys.exit(1)

    courses = [Course(c['kode'], c['jumlah_mahasiswa'], c['sks']) for c in data['kelas_mata_kuliah']]
    rooms = [Room(r['kode'], r['kuota']) for r in data['ruangan']]
    students = [Student(s['nim'], s['daftar_mk'], s['prioritas']) for s in data['mahasiswa']]

    return courses, rooms, students

def schedule_table_for_room(schedule: Schedule, room_id: str):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    day_to_index = {day: i for i, day in enumerate(days)}

    schedule_data: Dict[int, List[str]] = {}
    for assignment in schedule.assignments:
        if assignment.room.room_id == room_id:
            hour_index = assignment.time_slot.hour_index()
            course_id = assignment.course.course_id
            if hour_index not in schedule_data:
                schedule_data[hour_index] = []
            schedule_data[hour_index].append(course_id)

    print(f"              | {days[0]:^10} | {days[1]:^10} | {days[2]:^10} | {days[3]:^10} | {days[4]:^10} |")
    print("-" * 80)

    for hour in range(8, 17):
        max_courses_in_hour = 1
        for day in days:
            hour_index = day_to_index[day] * 24 + hour
            if hour_index in schedule_data:
                max_courses_in_hour = max(max_courses_in_hour, len(schedule_data[hour_index]))

        for line_num in range(max_courses_in_hour):
            time_label = f"{hour:02d}:00 - {hour+1:02d}:00" if line_num == 0 else ""
            row_str = f"{time_label:<14}|"

            for day in days:
                hour_index = day_to_index[day] * 24 + hour
                cell_content = ""
                if hour_index in schedule_data and line_num < len(schedule_data[hour_index]):
                    cell_content = schedule_data[hour_index][line_num]
                
                row_str += f" {cell_content:<11}|"
            
            print(row_str)
        print("-" * 80)

def visualize_schedule(schedule: Schedule, rooms: List[Room]):
    if not rooms:
        print("There is no room data to visualize.")
        return
            
    for room in rooms:
        is_room_used = False
        for assignment in schedule.assignments:
            if assignment.room.room_id == room.room_id:
                is_room_used = True
                break

        if is_room_used:
            print(f"\nRoom Code: {room.room_id} (Capacity: {room.capacity})")
            schedule_table_for_room(schedule, room.room_id)            
