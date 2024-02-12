CREATE TABLE houses (
    id INTEGER,
    house TEXT NOT NULL,
    head TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE students (
    id INTEGER,
    student_name TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE assignments (
    student_id INTEGER NOT NULL,
    house_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (house_id) REFERENCES houses(id)
);

INSERT INTO houses (id, house, head)
VALUES (1, 'Gryffindor', 'Minerva McGonagall');

INSERT INTO houses (id, house, head)
VALUES (2, 'Hufflepuff', 'Pomona Sprout');

INSERT INTO houses (id, house, head)
VALUES (3, 'Ravenclaw', 'Filius Flitwick');

INSERT INTO houses (id, house, head)
VALUES (4, 'Slytherin', 'Severus Snape');