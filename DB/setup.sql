USE db;

CREATE TABLE `User` (
  id INT NOT NULL AUTO_INCREMENT,
  e_mail VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  surname VARCHAR(255),
  title VARCHAR(255),
  role VARCHAR(255) NOT NULL,
  description VARCHAR(255),
  experience VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE `Group` (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE `Task` (
  id INT NOT NULL AUTO_INCREMENT,
  id_group INT NOT NULL,
  max_samples_for_user INT,
  name VARCHAR(255),
  description VARCHAR(255),
  type VARCHAR(255),
  PRIMARY KEY (id),
  FOREIGN KEY (id_group) REFERENCES `Group`(id)
);

CREATE TABLE `Membership` (
  id_user INT NOT NULL,
  id_group INT NOT NULL,
  PRIMARY KEY (id_user, id_group),
  FOREIGN KEY (id_user) REFERENCES `User`(id),
  FOREIGN KEY (id_group) REFERENCES `Group`(id)
);

CREATE TABLE `Sample` (
  id INT NOT NULL AUTO_INCREMENT,
  id_task INT NOT NULL,
  path VARCHAR(255),
  format VARCHAR(255),
  PRIMARY KEY (id),
  FOREIGN KEY (id_task) REFERENCES `Task`(id)
);

CREATE TABLE `Examination` (
  id INT NOT NULL AUTO_INCREMENT,
  id_user INT NOT NULL,
  id_sample INT NOT NULL,
  to_further_verification BOOLEAN,
  bad_quality BOOLEAN,
  PRIMARY KEY (id),
  FOREIGN KEY (id_user) REFERENCES `User`(id),
  FOREIGN KEY (id_sample) REFERENCES `Sample`(id)
);

CREATE TABLE `Label` (
  id INT NOT NULL AUTO_INCREMENT,
  id_task INT NOT NULL,
  name VARCHAR(255),
  description VARCHAR(255),
  PRIMARY KEY (id),
  FOREIGN KEY (id_task) REFERENCES `Task`(id)
);

CREATE TABLE `BBox` (
  id INT NOT NULL AUTO_INCREMENT,
  id_examination INT NOT NULL,
  id_label INT NOT NULL,
  comment VARCHAR(255),
  x1 FLOAT,
  y1 FLOAT,
  x2 FLOAT,
  y2 FLOAT,
  PRIMARY KEY (id),
  FOREIGN KEY (id_examination) REFERENCES `Examination`(id),
  FOREIGN KEY (id_label) REFERENCES `Label`(id)
);


INSERT INTO `User` (e_mail, password_hash, name, surname, title, role, description, experience)
VALUES
    ('user1@example.com', 'hash1', 'John', 'Doe', 'Mr.', 'User', 'Description 1', 'Experience 1'),
    ('user2@example.com', 'hash2', 'Jane', 'Smith', 'Ms.', 'User', 'Description 2', 'Experience 2'),
    ('user3@example.com', 'hash3', 'Alice', 'Johnson', 'Dr.', 'Admin', 'Description 3', 'Experience 3'),
    ('user4@example.com', 'hash4', 'Bob', 'Wilson', 'Mr.', 'User', 'Description 4', 'Experience 4'),
    ('user5@example.com', 'hash5', 'Eve', 'Davis', 'Ms.', 'User', 'Description 5', 'Experience 5');


INSERT INTO `Group` (name, description)
VALUES
    ('Group 1', 'Description 1'),
    ('Group 2', 'Description 2'),
    ('Group 3', 'Description 3'),
    ('Group 4', 'Description 4'),
    ('Group 5', 'Description 5');


INSERT INTO `Task` (id_group, max_samples_for_user, name, description, type)
VALUES
    (1, 1, 'Task 1', 'Task Description 1', 'Type A'),
    (2, 2, 'Task 2', 'Task Description 2', 'Type B'),
    (3, 2, 'Task 3', 'Task Description 3', 'Type A'),
    (4, 3, 'Task 4', 'Task Description 4', 'Type C'),
    (5, 4, 'Task 5', 'Task Description 5', 'Type B');


INSERT INTO `Membership` (id_user, id_group)
VALUES
    (1, 1),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, 3);


INSERT INTO `Sample` (id_task, path, format)
VALUES
    (1, '/path/to/sample1', 'Format A'),
    (2, '/path/to/sample2', 'Format B'),
    (3, '/path/to/sample3', 'Format A'),
    (4, '/path/to/sample4', 'Format C'),
    (2, '/path/to/sample5', 'Format B');


INSERT INTO `Examination` (id_user, id_sample, to_further_verification, bad_quality)
VALUES
    (1, 1, 0, 0),
    (2, 2, 1, 0),
    (3, 3, 0, 1),
    (4, 4, 1, 0),
    (2, 5, 0, 0);

INSERT INTO `Label` (id_task, name, description)
VALUES
    (1, 'Label 1', 'Label Description 1'),
    (2, 'Label 2', 'Label Description 2'),
    (3, 'Label 3', 'Label Description 3'),
    (4, 'Label 4', 'Label Description 4'),
    (2, 'Label 5', 'Label Description 5');


INSERT INTO `BBox` (id_examination, id_label, comment, x1, y1, x2, y2)
VALUES
    (1, 1, 'Comment 1', 10.0, 20.0, 30.0, 40.0),
    (2, 2, 'Comment 2', 15.0, 25.0, 35.0, 45.0),
    (3, 3, 'Comment 3', 20.0, 30.0, 40.0, 50.0),
    (4, 4, 'Comment 4', 25.0, 35.0, 45.0, 55.0),
    (2, 5, 'Comment 5', 30.0, 40.0, 50.0, 60.0);
