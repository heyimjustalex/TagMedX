USE db;

CREATE TABLE `User` (
  id INT NOT NULL AUTO_INCREMENT,
  e_mail VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  surname VARCHAR(255),
  title VARCHAR(255),
  specialization VARCHAR(255),
  practice_start_year INT,
  PRIMARY KEY (id)
);

CREATE TABLE `Group` (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255),
  connection_string VARCHAR (255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE `Set` (
  id INT NOT NULL AUTO_INCREMENT,
  id_group INT NOT NULL,
  name VARCHAR(255),
  description VARCHAR(255),
  type VARCHAR(255),
  package_size INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_group) REFERENCES `Group`(id)
);



CREATE TABLE `Membership` (
  id_user INT NOT NULL,
  id_group INT NOT NULL,
  role VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_user, id_group),
  FOREIGN KEY (id_user) REFERENCES `User`(id),
  FOREIGN KEY (id_group) REFERENCES `Group`(id)
);

CREATE TABLE `Package` (
  id INT NOT NULL AUTO_INCREMENT,
  id_set INT NOT NULL,
  id_user INT,
  is_ready BOOLEAN,
  PRIMARY KEY (id),
  FOREIGN KEY (id_set) REFERENCES `Set`(id),
  FOREIGN KEY (id_user) REFERENCES `User`(id)
);

CREATE TABLE `Sample` (
  id INT NOT NULL AUTO_INCREMENT,
  id_package INT NOT NULL,
  path VARCHAR(255) NOT NULL,
  format VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_package) REFERENCES `Package`(id)
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
  id_set INT NOT NULL,
  name VARCHAR(255),
  description VARCHAR(255),
  color VARCHAR(255),
  PRIMARY KEY (id),
  FOREIGN KEY (id_set) REFERENCES `Set`(id)
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


INSERT INTO `User` (e_mail, password_hash, name, surname, title, specialization, practice_start_year)
VALUES
    ('user1@example.com', 'hash1', 'John', 'Doe', 'Mr.',  'Oncology', 2000),
    ('user2@example.com', 'hash2', 'Jane', 'Smith', 'Ms.', 'Pediatrics', 2002),
    ('user3@example.com', 'hash3', 'Alice', 'Johnson', 'Dr.',  'Orthopedics', 2012),
    ('user4@example.com', 'hash4', 'Bob', 'Wilson', 'Mr.', 'Psychiatry', 2023),
    ('user5@example.com', 'hash5', 'Eve', 'Davis', 'Ms.', 'Cardiology', 2020);

INSERT INTO `Group` (name, description,connection_string)
VALUES
    ('Group 1', 'Description 1','password1'),
    ('Group 2', 'Description 2','password2'),
    ('Group 3', 'Description 3','password3'),
    ('Group 4', 'Description 4','password4'),
    ('Group 5', 'Description 5','password5');


INSERT INTO `Set` (id_group, name, description, type, package_size)
VALUES
    (1, 'set 1', 'set Description 1', 'Detection', 100),
    (2, 'set 2', 'set Description 2', 'Detection', 10),
    (3, 'set 3', 'set Description 3', 'Classification', 100),
    (4, 'set 4', 'set Description 4', 'Classification', 10),
    (5, 'set 5', 'set Description 5', 'Classification', 100);

INSERT INTO `Package` (id_set, id_user, is_ready)
VALUES
    (1, NULL, 0),
    (1, NULL, 0),
    (2, NULL, 1),
    (2, NULL, 1),
    (3, NULL, 1);


INSERT INTO `Membership` (id_user, id_group, role)
VALUES
    (1, 1, 'User'),
    (2, 1, 'Admin'),
    (2, 2, 'User'),
    (3, 2, 'Admin'),
    (4, 3, 'Admin');


INSERT INTO `Sample` (id_package, path, format)
VALUES
    (3, '/path/to/sample1', 'Format A'),
    (1, '/path/to/sample2', 'Format B'),
    (4, '/path/to/sample3', 'Format A'),
    (4, '/path/to/sample4', 'Format C'),
    (5, '/path/to/sample5', 'Format B');


INSERT INTO `Examination` (id_user, id_sample, to_further_verification, bad_quality)
VALUES
    (1, 1, 0, 0),
    (2, 2, 1, 0),
    (3, 3, 0, 1),
    (4, 4, 1, 0),
    (2, 5, 0, 0);

INSERT INTO `Label` (id_set, name, description, color)
VALUES
    (1, 'Label 1', 'Label Description 1', NULL),
    (2, 'Label 2', 'Label Description 2', NULL),
    (3, 'Label 3', 'Label Description 3', NULL),
    (4, 'Label 4', 'Label Description 4', NULL),
    (2, 'Label 5', 'Label Description 5', NULL);


INSERT INTO `BBox` (id_examination, id_label, comment, x1, y1, x2, y2)
VALUES
    (1, 1, 'Comment 1', 10.0, 20.0, 30.0, 40.0),
    (2, 2, 'Comment 2', 15.0, 25.0, 35.0, 45.0),
    (3, 3, 'Comment 3', 20.0, 30.0, 40.0, 50.0),
    (4, 4, 'Comment 4', 25.0, 35.0, 45.0, 55.0),
    (2, 5, 'Comment 5', 30.0, 40.0, 50.0, 60.0);
