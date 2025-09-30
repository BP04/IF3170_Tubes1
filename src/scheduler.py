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

def intersection_length(interval1: Tuple[int, int], interval2: Tuple[int, int]) -> int:
    start1, end1 = interval1
    start2, end2 = interval2
    if end1 <= start2 or end2 <= start1:
        return 0
    return min(end1, end2) - max(start1, start2)

def fitness(schedule: Schedule, students: List[Student]) -> int:
    penalty = 0

    for student in students:
        for i in range(len(student.course_list)):
            for j in range(i + 1, len(student.course_list)):
                course_id_1 = student.course_list[i]
                course_id_2 = student.course_list[j]

                assignments_1 = [a for a in schedule.assignments if a.course.course_id == course_id_1]
                assignments_2 = [a for a in schedule.assignments if a.course.course_id == course_id_2]

                for a1 in assignments_1:
                    for a2 in assignments_2:
                        interval1 = a1.time_slot.interval()
                        interval2 = a2.time_slot.interval()
                        penalty += intersection_length(interval1, interval2)

    for i in range(len(schedule.assignments)):
        for j in range(i + 1, len(schedule.assignments)):
            a1 = schedule.assignments[i]
            a2 = schedule.assignments[j]

            if a1.room.room_id == a2.room.room_id:
                interval1 = a1.time_slot.interval()
                interval2 = a2.time_slot.interval()
                penalty += intersection_length(interval1, interval2)

    for i in range(len(schedule.assignments)):
        student_count = 0
        for j in range(len(students)):
            student = students[j]
            a1 = schedule.assignments[i]

            if a1.course.course_id in student.course_list:
                student_count += 1
        
        if student_count > a1.room.capacity:
            penalty += (student_count - a1.room.capacity)

    return penalty