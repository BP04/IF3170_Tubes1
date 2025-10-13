from models import *
from typing import List, Dict, Tuple, Set
import random
import copy

def generate_initial_schedule(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot]) -> Schedule:
    assignments = []
    for course in courses:
        for _ in range(course.credits):
            random_room = random.choice(rooms)
            random_time_slot = random.choice(time_slots)
            assignment = Assignment(course, random_time_slot, random_room)
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

    # PENALTI 1: Konflik waktu untuk setiap mahasiswa
    for student in students:
        filled: Set[int] = set()
        for course_id in student.course_list:
            if course_id in schedule.course_assignments:
                for assignment in schedule.course_assignments[course_id]:
                    if assignment.time_slot.hour_index() in filled:
                        penalty += 1
                    else:
                        filled.add(assignment.time_slot.hour_index())

    # PENALTI 2: Pertemuan bertabrakan di ruangan dan waktu yang sama
    room_time_courses: Dict[Tuple[str, int], List[str]] = {}
    for assignment in schedule.assignments:
        key = (assignment.room.room_id, assignment.time_slot.hour_index())
        if key not in room_time_courses:
            room_time_courses[key] = []
        room_time_courses[key].append(assignment.course.course_id)

    for courses_in_slot in room_time_courses.values():
        if len(courses_in_slot) > 1:
            for course_id in courses_in_slot:
                if course_id in students_in_course:
                    for student in students_in_course[course_id]:
                        penalty += priority_weight(student.priority_map.get(course_id, 0))
                        
    # PENALTI 3: Kapasitas ruangan terlampaui (FIXED - sekarang dikali dengan SKS)
    processed_assignments = set()
    for assignment in schedule.assignments:
        course = assignment.course
        room = assignment.room
        assignment_id = (course.course_id, room.room_id, assignment.time_slot.hour_index())
        
        if course.num_students > room.capacity and assignment_id not in processed_assignments:
            penalty += (course.num_students - room.capacity) * course.credits
            processed_assignments.add(assignment_id)

    return -penalty

def generate_neighbor(schedule: Schedule, rooms: List[Room], time_slots: List[TimeSlot]) -> Schedule:
    new_schedule = copy.deepcopy(schedule)
    num_assignments = len(new_schedule.assignments)

    if num_assignments < 1:
        return new_schedule 

    can_swap = num_assignments >= 2
    move_type = random.random() if can_swap else 1.0 

    if move_type < 0.5 and can_swap:
        index1, index2 = random.sample(range(num_assignments), 2)
        assignment1 = new_schedule.assignments[index1]
        assignment2 = new_schedule.assignments[index2]
        assignment1.room, assignment2.room = assignment2.room, assignment1.room
        assignment1.time_slot, assignment2.time_slot = assignment2.time_slot, assignment1.time_slot
    else:
        index = random.randint(0, num_assignments - 1)
        new_schedule.assignments[index].room = random.choice(rooms)
        new_schedule.assignments[index].time_slot = random.choice(time_slots)

    return Schedule(new_schedule.assignments)

def initialize_population(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], population_size: int) -> List[Schedule]:
    population = []
    
    for _ in range(population_size):
        population.append(generate_initial_schedule(courses, rooms, time_slots))
        
    return population

def evaluate_population(population: List[Schedule], students: List[Student]) -> List[Tuple[Schedule, float]]:
    population_objective = []
    
    for schedule in population:
        objective_score = objective(schedule, students)
        population_objective.append((schedule, objective_score))
        
    return population_objective