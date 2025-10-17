from models import *
from typing import List, Dict, Tuple, Set
import random
import copy

def generate_initial_schedule(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], 
                             students: List[Student], lecturers: List[Lecturer],
                             students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]]) -> Tuple[Schedule, float]:
    assignments: List[Assignment] = []

    for course in courses:
        for _ in range(course.credits):
            random_room: Room = random.choice(rooms)
            random_time_slot: TimeSlot = random.choice(time_slots)
            assignment: Assignment = Assignment(course, random_time_slot, random_room)
            assignments.append(assignment)

    schedule: Schedule = Schedule(assignments, students, lecturers)
    initial_objective: float = objective(schedule, students, lecturers, students_in_course, lecturers_in_course)
    
    return schedule, initial_objective

def priority_weight(priority: int) -> float:
    if priority == 1:
        return 1.75
    if priority == 2:
        return 1.5
    if priority == 3:
        return 1.25
    return 1.0

def course_priority_penalty(course_ids: List[str], students_in_course: Dict[str, List[Student]]) -> float:
    if len(course_ids) <= 1:
        return 0.0
    
    penalty = 0.0
    for course_id in course_ids:
        if course_id in students_in_course:
            for student in students_in_course[course_id]:
                penalty += priority_weight(student.priority_map.get(course_id, 99))
    
    return penalty

def objective(schedule: Schedule, students: List[Student], lecturers: List[Lecturer],
              students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]]) -> float:
    penalty = 0.0

    for assignment in schedule.assignments:
        course_id = assignment.course.course_id
        if course_id not in students_in_course:
            continue

        penalty += max(0, len(students_in_course[course_id]) - assignment.room.capacity)

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
    
    for lecturer in lecturers:
        filled: Set[int] = set()

        for course_id in lecturer.course_list:
            current_course_assignments: List[Assignment] = schedule.course_assignments[course_id]
            for assignment in current_course_assignments:
                hour_idx: int = assignment.time_slot.hour_index()
                if hour_idx in filled:
                    penalty += 1
                else:
                    filled.add(hour_idx)

    for courses_list_ids in schedule.room_time_courses.values():
        penalty += course_priority_penalty(courses_list_ids, students_in_course)


    return -penalty

def calculate_swap_delta(schedule: Schedule, assignment1: Assignment, assignment2: Assignment,
                         students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]]) -> float:
    delta = 0.0
    
    course1, room1, time1 = assignment1.course, assignment1.room, assignment1.time_slot
    course2, room2, time2 = assignment2.course, assignment2.room, assignment2.time_slot
    hour1, hour2 = time1.hour_index(), time2.hour_index()
    
    num_students1: int = len(students_in_course.get(course1.course_id, []))
    num_students2: int = len(students_in_course.get(course2.course_id, []))
    old_capacity_penalty: int = max(0, num_students1 - room1.capacity) + max(0, num_students2 - room2.capacity)
    new_capacity_penalty: int = max(0, num_students1 - room2.capacity) + max(0, num_students2 - room1.capacity)
    delta += new_capacity_penalty - old_capacity_penalty
    
    courses_at_1_ids = schedule.room_time_courses.get((room1.room_id, hour1), [])
    courses_at_2_ids = schedule.room_time_courses.get((room2.room_id, hour2), [])
    
    delta -= course_priority_penalty(courses_at_1_ids, students_in_course)
    if (room1.room_id, hour1) != (room2.room_id, hour2):
         delta -= course_priority_penalty(courses_at_2_ids, students_in_course)
    
    temp_courses_at_1_ids = list(courses_at_1_ids)
    if course1.course_id in temp_courses_at_1_ids:
        temp_courses_at_1_ids.remove(course1.course_id)
    new_courses_at_1_ids = temp_courses_at_1_ids + [course2.course_id]

    temp_courses_at_2_ids = list(courses_at_2_ids)
    if course2.course_id in temp_courses_at_2_ids:
        temp_courses_at_2_ids.remove(course2.course_id)
    new_courses_at_2_ids = temp_courses_at_2_ids + [course1.course_id]
    
    delta += course_priority_penalty(new_courses_at_1_ids, students_in_course)
    if (room1.room_id, hour1) != (room2.room_id, hour2):
        delta += course_priority_penalty(new_courses_at_2_ids, students_in_course)

    if hour1 != hour2:
        affected_students = set(students_in_course.get(course1.course_id, [])) | set(students_in_course.get(course2.course_id, []))
        affected_lecturers = set(lecturers_in_course.get(course1.course_id, [])) | set(lecturers_in_course.get(course2.course_id, []))

        for student in affected_students:
            schedule_base = schedule.student_schedules[student.student_id] - {hour1, hour2}
            
            takes_c1 = course1.course_id in student.course_list
            takes_c2 = course2.course_id in student.course_list

            clashes_before = 0
            if takes_c1 and hour1 in schedule_base: clashes_before += 1
            if takes_c2 and hour2 in schedule_base: clashes_before += 1

            clashes_after = 0
            if takes_c1 and hour2 in schedule_base: clashes_after += 1 # course1 moves to hour2
            if takes_c2 and hour1 in schedule_base: clashes_after += 1 # course2 moves to hour1
            
            delta += (clashes_after - clashes_before)

        for lecturer in affected_lecturers:
            schedule_base = schedule.lecturer_schedules[lecturer.lecturer_id] - {hour1, hour2}

            takes_c1 = course1.course_id in lecturer.course_list
            takes_c2 = course2.course_id in lecturer.course_list

            clashes_before = 0
            if takes_c1 and hour1 in schedule_base: clashes_before += 1
            if takes_c2 and hour2 in schedule_base: clashes_before += 1

            clashes_after = 0
            if takes_c1 and hour2 in schedule_base: clashes_after += 1
            if takes_c2 and hour1 in schedule_base: clashes_after += 1

            delta += (clashes_after - clashes_before)

    return -delta

def calculate_move_delta(schedule: Schedule, assignment: Assignment, new_room: Room, new_time_slot: TimeSlot,
                         students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]]) -> float:
    delta = 0.0

    course, room, time = assignment.course, assignment.room, assignment.time_slot
    hour_old, hour_new = time.hour_index(), new_time_slot.hour_index()
    
    num_students: int = len(students_in_course.get(course.course_id, []))
    old_capacity_penalty = max(0, num_students - room.capacity)
    new_capacity_penalty = max(0, num_students - new_room.capacity)
    delta += new_capacity_penalty - old_capacity_penalty

    if (room.room_id, hour_old) != (new_room.room_id, hour_new):
        courses_at_old_ids = schedule.room_time_courses.get((room.room_id, hour_old), [])
        delta -= course_priority_penalty(courses_at_old_ids, students_in_course)
        
        new_courses_at_old_ids = []
        removed = False
        for c_id in courses_at_old_ids:
            if c_id == course.course_id and not removed:
                removed = True
            else:
                new_courses_at_old_ids.append(c_id)
        
        delta += course_priority_penalty(new_courses_at_old_ids, students_in_course)
        
        courses_at_new_ids = schedule.room_time_courses.get((new_room.room_id, hour_new), [])
        delta -= course_priority_penalty(courses_at_new_ids, students_in_course)
        
        new_courses_at_new_ids = courses_at_new_ids + [course.course_id]
        delta += course_priority_penalty(new_courses_at_new_ids, students_in_course)

    if hour_old != hour_new:
        for student in students_in_course.get(course.course_id, []):
            student_other = schedule.student_schedules[student.student_id] - {hour_old}

            clash_before = hour_old in student_other
            clash_after = hour_new in student_other

            if clash_before and not clash_after:
                delta -= 1
            elif not clash_before and clash_after:
                delta += 1
                
        for lecturer in lecturers_in_course.get(course.course_id, []):
            lecturer_other = schedule.lecturer_schedules[lecturer.lecturer_id] - {hour_old}

            clash_before = hour_old in lecturer_other
            clash_after = hour_new in lecturer_other

            if clash_before and not clash_after:
                delta -= 1
            elif not clash_before and clash_after:
                delta += 1
    
    return -delta

def generate_neighbor(schedule: Schedule, rooms: List[Room], time_slots: List[TimeSlot],
                     current_objective: float, students: List[Student], lecturers: List[Lecturer],
                     students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]]) -> Tuple[Schedule, float]:
    mutation_type: float = random.random()

    if len(schedule.assignments) < 2:
        mutation_type = 1.0

    delta: float = 0.0

    new_assignments: List[Assignment] = [copy.copy(a) for a in schedule.assignments]

    if mutation_type < 0.5:
        # swap two assignments
        index1: int
        index2: int
        index1, index2 = random.sample(range(len(schedule.assignments)), 2)
        assignment1: Assignment = schedule.assignments[index1]
        assignment2: Assignment = schedule.assignments[index2]
        
        delta = calculate_swap_delta(schedule, assignment1, assignment2, students_in_course, lecturers_in_course)
        
        new_assignments[index1].room, new_assignments[index2].room = new_assignments[index2].room, new_assignments[index1].room
        new_assignments[index1].time_slot, new_assignments[index2].time_slot = new_assignments[index2].time_slot, new_assignments[index1].time_slot
    else:
        # assign different room and time slot for an assignment
        index: int = random.randint(0, len(schedule.assignments) - 1)
        assignment: Assignment = schedule.assignments[index]
        new_room: Room = random.choice(rooms)
        new_time_slot: TimeSlot = random.choice(time_slots)
        
        delta = calculate_move_delta(schedule, assignment, new_room, new_time_slot, students_in_course, lecturers_in_course)
        
        new_assignments[index].room = new_room
        new_assignments[index].time_slot = new_time_slot

    new_schedule: Schedule = Schedule(new_assignments, students, lecturers)

    new_objective: float = current_objective + delta
    
    # turn on when testing
    actual_objective: float = objective(new_schedule, students, lecturers, students_in_course, lecturers_in_course)
    assert abs(new_objective - actual_objective) < 1e-6, f"Delta calculation mismatch: {new_objective} vs {actual_objective}, diff={new_objective - actual_objective}"
    
    return new_schedule, new_objective

def initialize_population(courses: List[Course], rooms: List[Room], time_slots: List[TimeSlot], 
                          students: List[Student], lecturers: List[Lecturer],
                          students_in_course: Dict[str, List[Student]], lecturers_in_course: Dict[str, List[Lecturer]],
                          population_size: int) -> List[Tuple[Schedule, float]]:
    population: List[Tuple[Schedule, float]] = []

    for _ in range(population_size):
        schedule, objective = generate_initial_schedule(courses, rooms, time_slots, students, lecturers, students_in_course, lecturers_in_course)
        population.append((schedule, objective))

    return population