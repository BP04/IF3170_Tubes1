import json
from typing import List, Tuple
from models import Course, Room, Student

def load_data_from_json(file_path: str) -> Tuple[List[Course], List[Room], List[Student]]:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return [], [], []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return [], [], []   

    courses = [Course(c['kode'], c['jumlah_mahasiswa'], c['sks']) for c in data['kelas_mata_kuliah']]
    rooms = [Room(r['kode'], r['kuota']) for r in data['ruangan']]
    students = [Student(s['nim'], s['daftar_mk'], s['prioritas']) for s in data['mahasiswa']]

    return courses, rooms, students