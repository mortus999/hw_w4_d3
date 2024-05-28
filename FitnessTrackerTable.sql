CREATE DATABASE fitness_tracker;

USE fitness_tracker;


CREATE TABLE Members (
	member_id INT AUTO_INCREMENT PRIMARY KEY,
    member_name VARCHAR(150) NOT NULL, 
    member_email VARCHAR(150), 
    member_phone VARCHAR(150)
    );

CREATE TABLE Workout_Sessions (
	workout_id INT AUTO_INCREMENT PRIMARY KEY,
    cardio_focus VARCHAR (300) NOT NULL, 
    lift_focus VARCHAR (300) NOT NULL, 
    date DATE,
    time TIME, 
    member_id INT, 
    FOREIGN KEY(member_id) REFERENCES Members(member_id)
)

SELECT * FROM Members;
SELECT * FROM Workout_Sessions;
INSERT INTO Workout_Sessions(cardio_focus, lift_focus) VALUES ("treadmil", "biceps");
ALTER TABLE Workout_Sessions DROP time