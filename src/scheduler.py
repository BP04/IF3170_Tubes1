from models import *
from typing import List, Dict, Tuple, Set
import random
import copy

def generate_initial_schedule(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot]) -> Schedule:
    assignments: List[Assignment] = []

    for course in courses:
        for _ in range(course.credits):
            random_room: Room = random.choice(rooms)
            random_time_slot: TimeSlot = random.choice(time_slots)
            assignment: Assignment = Assignment(course, random_time_slot, random_room)
            assignments.append(assignment)

    return Schedule(assignments)

def priority_weight(priority: int) -> float:
    if priority == 1:
        return 1.75
    if priority == 2:
        return 1.5
    if priority == 3:
        return 1.25
    return 1.0

def objective(schedule: Schedule, students: List[Student]) -> float:
    penalty = 0.0

    students_in_course: Dict[str, List[Student]] = {}
    for student in students:
        for course_id in student.course_list:
            if course_id not in students_in_course:
                students_in_course[course_id] = []
            students_in_course[course_id].append(student)

    for student in students:
        filled: Set[int] = set()

        for course_id in student.course_list:

            current_course_assignments: List[Assignment] = schedule.course_assignments[course_id]
            for assignment in current_course_assignments:
                hour_idx: int = assignment.time_slot.hour_index()
                if hour_idx in filled:
                    penalty += 1
                else:
                    filled.add(hour_idx)

    room_time_courses: Dict[Tuple[str, int], List[str]] = {}

    for assignment in schedule.assignments:
        room_id: str = assignment.room.room_id
        hour_index: int = assignment.time_slot.hour_index()
        course_id: str = assignment.course.course_id
        if (room_id, hour_index) not in room_time_courses:
            room_time_courses[(room_id, hour_index)] = []
        room_time_courses[(room_id, hour_index)].append(course_id)

    for courses_list in room_time_courses.values():
        if len(courses_list) == 1:
            continue
        
        for course_id in courses_list:
            students_list: List[Student] = students_in_course[course_id]
            for student in students_list:
                penalty += priority_weight(student.priority_map[course_id])

    return -penalty

def generate_neighbor(schedule: Schedule, rooms: List[Room], time_slots: List[TimeSlot]) -> Schedule:
    new_schedule: Schedule = copy.deepcopy(schedule)

    mutation_type: float = random.random()
    if mutation_type < 0.5:
        # swap two assignments
        index1: int
        index2: int
        index1, index2 = random.sample(range(len(new_schedule.assignments)), 2)
        assignment1: Assignment = new_schedule.assignments[index1]
        assignment2: Assignment = new_schedule.assignments[index2]
        assignment1.room, assignment2.room = assignment2.room, assignment1.room
        assignment1.time_slot, assignment2.time_slot = assignment2.time_slot, assignment1.time_slot
    else:
        # assign different room and time slot for an assignment
        index: int = random.randint(0, len(new_schedule.assignments) - 1)
        new_schedule.assignments[index].room = random.choice(rooms)
        new_schedule.assignments[index].time_slot = random.choice(time_slots)

    return new_schedule

def initialize_population(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], population_size: int) -> List[Schedule]:
    population: List[Schedule] = []

    for _ in range(population_size):
        population.append(generate_initial_schedule(courses, rooms, time_slots))

    return population

def evaluate_population(population: List[Schedule], students: List[Student]) -> List[Tuple[Schedule, float]]:
    population_objective: List[Tuple[Schedule, float]] = []

    for schedule in population:
        objective_score: float = objective(schedule, students)
        population_objective.append((schedule, objective_score))
    
    return population_objective