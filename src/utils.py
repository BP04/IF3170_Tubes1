import json
from typing import List, Tuple, Dict, Any, Set
from models import *

def load_data_from_json(file_path: str) -> Tuple[List[Course], List[Room], List[Student], List[Lecturer]]:
    try:
        with open(file_path, 'r') as f:
            data: Dict[str, Any] = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return [], [], [], []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return [], [], [], []   

    courses: List[Course] = [Course(c['kode'], c['jumlah_mahasiswa'], c['sks']) for c in data['kelas_mata_kuliah']]
    rooms: List[Room] = [Room(r['kode'], r['kuota']) for r in data['ruangan']]
    students: List[Student] = [Student(s['nim'], s['daftar_mk'], s['prioritas']) for s in data['mahasiswa']]
    lecturers: List[Lecturer] = [Lecturer(l['dosen_id'], l['course_list']) for l in data.get('dosen', [])]

    return courses, rooms, students, lecturers

def schedule_table_for_room(schedule: Schedule, room_id: str) -> None:
    day_to_index: Dict[str, int] = {'Senin': 0, 'Selasa': 1, 'Rabu': 2, 'Kamis': 3, 'Jumat': 4}

    time_to_courses: Dict[int, List[str]] = {}
    for assignment in schedule.assignments:
        if assignment.room.room_id != room_id:
            continue

        hour_index: int = assignment.time_slot.hour_index()
        course_id: str = assignment.course.course_id
        if hour_index not in time_to_courses:
            time_to_courses[hour_index] = []
        time_to_courses[hour_index].append(course_id)

    print("              |   Senin    |   Selasa   |    Rabu    |   Kamis    |   Jumat    |")

    for hour in range(8, 17):
        print(80 * '-')
        print(f"{hour:02d}:00 - {hour + 1:02d}:00 ", end="")

        max_course_on_hour: int = 1
        for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']:
            hour_idx: int = day_to_index[day] * 24 + hour
            if hour_idx in time_to_courses:
                max_course_on_hour = max(max_course_on_hour, len(time_to_courses[hour_idx]))

        first: bool = True
        for _ in range(max_course_on_hour):
            if not first:
                print()
                print(14 * ' ', end="")
            else:
                first = False

            for day in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']:
                hour_idx_2: int = day_to_index[day] * 24 + hour

                if hour_idx_2 in time_to_courses:
                    print("|", end="")
                    print(f" {time_to_courses[hour_idx_2][0]} ", end="")
                    
                    time_to_courses[hour_idx_2].pop(0)
                    if len(time_to_courses[hour_idx_2]) == 0:
                        time_to_courses.pop(hour_idx_2)
                else:
                    print("|            ", end="")
            print("|", end="")
        
        print()
        
    print()

def visualize_schedule(schedule: Schedule, rooms: List[Room]) -> None:
    room_used: Set[str] = set()

    for assignment in schedule.assignments:
        room_used.add(assignment.room.room_id)

    for room in rooms:
        if room.room_id not in room_used:
            continue

        print(f"Ruangan {room.room_id}:")
        schedule_table_for_room(schedule, room.room_id)
        print()