from models import *
from typing import List, Dict, Tuple
from random import choice

def generate_initial_schedule(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot]) -> Schedule:
    assignments = []

    for course in courses:
        for _ in range(course.credits):
            random_room = choice(rooms)
            random_time_slot = choice(time_slots)
            assignment = Assignment(course, random_time_slot, random_room)
            assignments.append(assignment)

    return Schedule(assignments)

def priority_weight(priority: int) -> int:
    if priority == 1:
        return 1.75
    if priority == 2:
        return 1.5
    if priority == 3:
        return 1.25
    return 1

def fitness(schedule: Schedule, students: List[Student]) -> int:
    penalty = 0

    students_in_course: Dict[str, List[Student]] = {}
    for student in students:
        for course_id in student.course_list:
            if course_id not in students_in_course:
                students_in_course[course_id] = []
            students_in_course[course_id].append(student)

    for assignment in schedule.assignments:
        course_id = assignment.course.course_id

        if course_id not in students_in_course:
            continue

        penalty += 2 * max(0, len(students_in_course[course_id]) - assignment.room.capacity)

    for student in students:
        filled: Set[int] = set()

        for course_id in student.course_list:

            current_course_assignments = schedule.course_assignments[course_id]
            for assignment in current_course_assignments:
                if assignment.time_slot.hour_index() in filled:
                    penalty += 1
                else:
                    filled.add(assignment.time_slot.hour_index())

    room_time_courses: Dict[Tuple[str, int], List[str]] = {}

    for assignment in schedule.assignments:
        room_id = assignment.room.room_id
        hour_index = assignment.time_slot.hour_index()
        course_id = assignment.course.course_id
        if (room_id, hour_index) not in room_time_courses:
            room_time_courses[(room_id, hour_index)] = []
        room_time_courses[(room_id, hour_index)].append(course_id)

    for courses in room_time_courses.values():
        if len(courses) == 1:
            continue
        
        for course_id in courses:
            students = students_in_course[course_id]
            for student in students:
                penalty += priority_weight(student.priority_map[course_id])

    return penalty