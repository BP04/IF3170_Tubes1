from typing import List, Tuple, Dict, Any
import random
from models import *
import json

def generate_time_slots(days: List[str], hours: List[int]) -> List[TimeSlot]:
    time_slots: List[TimeSlot] = []
    for day in days:
        for hour in hours:
            time_slots.append(TimeSlot(day, hour))

    return time_slots

def generate_test_data(num_courses: int, num_rooms: int, num_students: int, num_lecturers: int) -> Tuple[List[Course], List[Room], List[Student], List[Lecturer]]:

    courses: List[Course] = []
    for i in range(num_courses):
        course_id: str = f"IF{3000 + i}_K{random.randint(1, 3):02d}"
        num_students: int = random.randint(20, 100)
        credits: int = random.randint(2, 4)
        courses.append(Course(course_id, num_students, credits))

    rooms: List[Room] = []
    for i in range(num_rooms):
        room_id: str = f"R-{7600 + i}"
        capacity: int = random.choice([40, 50, 60, 80, 100, 120])
        rooms.append(Room(room_id, capacity))

    min_credits: int = 2
    max_credits: int = 24

    students: List[Student] = []

    for i in range(num_students):
        student_id: str = f"13523{i:03d}"
        
        student_course_ids: List[str] = []
        current_credits: int = 0
        
        available_courses: List[Course] = random.sample(courses, len(courses))
        
        for course in available_courses:
            if current_credits + course.credits <= max_credits:
                student_course_ids.append(course.course_id)
                current_credits += course.credits
        
        while current_credits < min_credits:
            extra_course: Course = random.choice(available_courses)
            if extra_course.course_id not in student_course_ids and current_credits + extra_course.credits <= max_credits:
                student_course_ids.append(extra_course.course_id)
                current_credits += extra_course.credits

        priorities: List[int] = list(range(1, len(student_course_ids) + 1))
        random.shuffle(priorities)
        
        students.append(Student(student_id, student_course_ids, priorities))

    lecturers: List[Lecturer] = []
    for i in range(num_lecturers):
        lecturer_id: str = f"Dosen_{i + 1}"
        courses_taught: int = random.randint(1, min(num_courses, 5))
        lecturer_course_ids: List[str] = [c.course_id for c in random.sample(courses, courses_taught)]
        lecturers.append(Lecturer(lecturer_id, lecturer_course_ids))

    return courses, rooms, students, lecturers

def save_data_to_json(courses: List[Course], rooms: List[Room], students: List[Student], lecturers: List[Lecturer], file_path: str) -> None:
    data: Dict[str, Any] = {
        "kelas_mata_kuliah": [
            {
                "kode": c.course_id,
                "jumlah_mahasiswa": c.num_students,
                "sks": c.credits
            } for c in courses
        ],
        "ruangan": [
            {
                "kode": r.room_id,
                "kuota": r.capacity
            } for r in rooms
        ],
        "mahasiswa": [
            {
                "nim": s.student_id,
                "daftar_mk": s.course_list,
                "prioritas": s.priority
            } for s in students
        ],
        "dosen": [
            {
                "dosen_id": l.lecturer_id,
                "course_list": l.course_list
            } for l in lecturers
        ]
    }
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    courses, rooms, students, lecturers = generate_test_data(15, 10, 50, 6)
    save_data_to_json(courses, rooms, students, lecturers, "data/small_test.json")

    # courses, rooms, students, lecturers = generate_test_data(30, 10, 300, 20)
    # save_data_to_json(courses, rooms, students, lecturers, "data/large_test.json")