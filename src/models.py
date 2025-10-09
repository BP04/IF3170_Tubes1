from typing import Tuple, List, Dict

class Course:
    def __init__(self, course_id: str, num_students: int, credits: int):
        self.course_id = course_id
        self.num_students = num_students
        self.credits = credits

class TimeSlot:
    # one time slot is one hour
    # interval covers [hour, hour + 1) on that day
    def __init__(self, day: str, hour: int):
        self.day = day
        self.hour = hour

    def hour_index(self) -> int:
        day_to_index: Dict[str, int] = {'Senin': 0, 'Selasa': 1, 'Rabu': 2, 'Kamis': 3, 'Jumat': 4}
        hour_index = day_to_index[self.day] * 24 + self.hour
        return hour_index

class Room:
    def __init__(self, room_id: str, capacity: int):
        self.room_id = room_id
        self.capacity = capacity

class Student:
    def __init__(self, student_id: str, course_list: List[str], priority: List[int]):
        self.student_id = student_id
        self.course_list = course_list
        self.priority = priority

        self.priority_map: Dict[str, int] = {}
        for course_id, priority in zip(course_list, priority):
            self.priority_map[course_id] = priority

class Assignment:
    def __init__(self, course: Course, time_slot: TimeSlot, room: Room):
        self.course = course
        self.time_slot = time_slot
        self.room = room

class Schedule:
    def __init__(self, assignments: List[Assignment]):
        self.assignments = assignments

        self.course_assignments: Dict[str, List[Assignment]] = {} # course_id -> list of assignments
        for assignment in assignments:
            course_id = assignment.course.course_id
            if course_id not in self.course_assignments:
                self.course_assignments[course_id] = []
            self.course_assignments[course_id].append(assignment)