CREATE TABLE IF NOT EXISTS Relation_1 (
  CourseName VARCHAR(255),
  CourseID VARCHAR(255),
  Instructor VARCHAR(255)
);

INSERT INTO Relation_1 VALUES ('Intro to CS', 'CSE101', 'Dr. Smith');

INSERT INTO Relation_1 VALUES ('Data Structures', 'CSE102', 'Dr. Lee');

INSERT INTO Relation_1 VALUES ('Algorithms', 'CSE103', 'Dr. Wang');

CREATE TABLE IF NOT EXISTS Relation_2 (
  StudentName VARCHAR(255),
  StudentID INT
);

INSERT INTO Relation_2 VALUES ('Alice', 1);

INSERT INTO Relation_2 VALUES ('Bob', 2);

INSERT INTO Relation_2 VALUES ('Charlie', 3);

INSERT INTO Relation_2 VALUES ('David', 4);

CREATE TABLE IF NOT EXISTS Relation_3 (
  Instructor VARCHAR(255),
  CourseID VARCHAR(255),
  CourseName VARCHAR(255),
  StudentID INT,
  StudentName VARCHAR(255)
);

INSERT INTO Relation_3 VALUES ('Dr. Smith', 'CSE101', 'Intro to CS', 1, 'Alice');

INSERT INTO Relation_3 VALUES ('Dr. Lee', 'CSE102', 'Data Structures', 2, 'Bob');

INSERT INTO Relation_3 VALUES ('Dr. Smith', 'CSE101', 'Intro to CS', 3, 'Charlie');

INSERT INTO Relation_3 VALUES ('Dr. Wang', 'CSE103', 'Algorithms', 4, 'David');

CREATE TABLE IF NOT EXISTS Relation_4 (
  CourseID VARCHAR(255),
  StudentID INT
);

INSERT INTO Relation_4 VALUES ('CSE101', 1);

INSERT INTO Relation_4 VALUES ('CSE102', 2);

INSERT INTO Relation_4 VALUES ('CSE101', 3);

INSERT INTO Relation_4 VALUES ('CSE103', 4);