from typing import Tuple, List

class Course:
    def __init__(self, course_id: str, num_students: int, credits: int):
        self.course_id = course_id
        self.num_students = num_students
        self.credits = credits

class TimeSlot:
    def __init__(self, start_day: str, start_hour: int, end_day: str, end_hour: int):
        self.start_day = start_day
        self.start_hour = start_hour
        self.end_day = end_day
        self.end_hour = end_hour

    def interval(self) -> Tuple[int, int]:
        day_to_index = {'Senin': 0, 'Selasa': 1, 'Rabu': 2, 'Kamis': 3, 'Jumat': 4}
        start = day_to_index[self.start_day] * 24 + self.start_hour
        end = day_to_index[self.end_day] * 24 + self.end_hour
        return (start, end)

class Room:
    def __init__(self, room_id: str, capacity: int):
        self.room_id = room_id
        self.capacity = capacity

class Student:
    def __init__(self, student_id: str, course_list: List[int], priority: List[int]):
        self.student_id = student_id
        self.course_list = course_list
        self.priority = priority

class Assignment:
    def __init__(self, course: Course, time_slot: TimeSlot, room: Room):
        self.course = course
        self.time_slot = time_slot
        self.room = room

class Schedule:
    def __init__(self, assignments: List[Assignment]):
        self.assignments = assignments