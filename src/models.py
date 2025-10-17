from typing import Tuple, List, Dict, Set

class Course:
    course_id: str
    num_students: int
    credits: int
    
    def __init__(self, course_id: str, num_students: int, credits: int) -> None:
        self.course_id = course_id
        self.num_students = num_students
        self.credits = credits

class TimeSlot:
    # one time slot is one hour
    # interval covers [hour, hour + 1) on that day
    day: str
    hour: int
    
    def __init__(self, day: str, hour: int) -> None:
        self.day = day
        self.hour = hour

    def hour_index(self) -> int:
        day_to_index: Dict[str, int] = {'Senin': 0, 'Selasa': 1, 'Rabu': 2, 'Kamis': 3, 'Jumat': 4}
        hour_index = day_to_index[self.day] * 24 + self.hour
        return hour_index

class Room:
    room_id: str
    capacity: int
    
    def __init__(self, room_id: str, capacity: int) -> None:
        self.room_id = room_id
        self.capacity = capacity

class Student:
    student_id: str
    course_list: List[str]
    priority: List[int]
    priority_map: Dict[str, int]
    
    def __init__(self, student_id: str, course_list: List[str], priority: List[int]) -> None:
        self.student_id = student_id
        self.course_list = course_list
        self.priority = priority

        self.priority_map = {}
        for course_id, priority_val in zip(course_list, priority):
            self.priority_map[course_id] = priority_val

class Lecturer:
    lecturer_id: str
    course_list: List[str]
    
    def __init__(self, lecturer_id: str, course_list: List[str]) -> None:
        self.lecturer_id = lecturer_id
        self.course_list = course_list
class Assignment:
    course: Course
    time_slot: TimeSlot
    room: Room
    
    def __init__(self, course: Course, time_slot: TimeSlot, room: Room) -> None:
        self.course = course
        self.time_slot = time_slot
        self.room = room

class Schedule:
    assignments: List[Assignment]
    course_assignments: Dict[str, List[Assignment]]
    room_time_courses: Dict[Tuple[str, int], List[str]]
    student_schedules: Dict[str, Set[int]]
    lecturer_schedules: Dict[str, Set[int]]
    
    def __init__(self, assignments: List[Assignment], students: List[Student], lecturers: List[Lecturer]) -> None:
        self.assignments = assignments

        self.course_assignments = {}  # course_id -> list of assignments
        for assignment in assignments:
            course_id: str = assignment.course.course_id
            if course_id not in self.course_assignments:
                self.course_assignments[course_id] = []
            self.course_assignments[course_id].append(assignment)
        
        self.room_time_courses = {}  # (room_id, hour_index) -> list of course_ids
        for assignment in assignments:
            room_id: str = assignment.room.room_id
            hour_index: int = assignment.time_slot.hour_index()
            course_id: str = assignment.course.course_id
            if (room_id, hour_index) not in self.room_time_courses:
                self.room_time_courses[(room_id, hour_index)] = []
            self.room_time_courses[(room_id, hour_index)].append(course_id)

        self.student_schedules = {}
        for student in students:
            self.student_schedules[student.student_id] = set()
            for course_id in student.course_list:
                for assignment in self.course_assignments[course_id]:
                    self.student_schedules[student.student_id].add(assignment.time_slot.hour_index())

        self.lecturer_schedules = {}
        for lecturer in lecturers:
            self.lecturer_schedules[lecturer.lecturer_id] = set()
            for course_id in lecturer.course_list:
                for assignment in self.course_assignments[course_id]:
                    self.lecturer_schedules[lecturer.lecturer_id].add(assignment.time_slot.hour_index())