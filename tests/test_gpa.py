
#Basic tests for the Campusly GPA calculator.
import sys
from pathlib import Path

# add the code folder to the Python path so the test can import app.py.
sys.path.append(str(Path(__file__).resolve().parents[1] / "code"))

from app import calculate_gpa

def test_calculate_gpa_weighted_average():
    rows = [
        {"name": "Course 1", "grade": "A", "credits": "3"},
        {"name": "Course 2", "grade": "B", "credits": "3"},
    ]
    assert calculate_gpa(rows) == 3.5


def test_calculate_gpa_empty_list():
    assert calculate_gpa([]) is None
