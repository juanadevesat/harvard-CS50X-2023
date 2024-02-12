import csv
from cs50 import SQL

students = []

with open("students.csv", "r") as file:
    reader = csv.DictReader (file)
    for row in reader:
        students.append(row)

db = SQL("sqlite:///roster.db")
for i in range(len(students)):
    id = students[i]["id"]
    name = students[i]["student_name"]
    house = 0
    if students[i]["house"] == "Gryffindor":
        house = 1
    elif students[i]["house"] == "Hufflepuff":
        house = 2
    elif students[i]["house"] == "Ravenclaw":
        house = 3
    elif students[i]["house"] == "Slytherin":
        house = 4

    db.execute("INSERT INTO students (id, student_name) VALUES (?);", (id, name))
    db.execute("INSERT INTO assignments (student_id, house_id) VALUES (?);", (id, house))