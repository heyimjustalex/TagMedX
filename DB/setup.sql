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
  x INT,
  y INT,
  width INT,
  height INT,
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
    ('user5@example.com', 'hash5', 'Eve', 'Davis', 'Ms.', 'Cardiology', 2020),
    ('test@test.pl', '$2b$12$ClO7iaMeH519tZAjH3dyjeLxYfme3nUJrI62cnz/JbyGuElU41DAi', 'Jan', 'Kanty', 'Mr.', 'Cardiology', 2000);

INSERT INTO `Group` (name, description,connection_string)
VALUES
    ('Group 1', 'Description 1','password1'),
    ('Group 2', 'Description 2','password2'),
    ('Group 3', 'Description 3','password3'),
    ('Group 4', 'Description 4','password4'),
    ('Group 5', 'Description 5','password5');

INSERT INTO `Membership` (id_user, id_group, role)
VALUES
    (1, 1, 'User'),
    (2, 1, 'User'),
    (6, 1, 'Admin'),
    (3, 2, 'Admin'),
    (2, 2, 'User'),
    (6, 2, 'User');

INSERT INTO `Set` (id_group, name, description, type, package_size)
VALUES
    (1, 'set 1', 'set Description 1', 'Detection', 10),
    (1, 'set 2', 'set Description 2', 'Classification', 10),
    (2, 'set 3', 'set Description 3', 'Detection', 10),
    (2, 'set 4', 'set Description 4', 'Classification', 10);

INSERT INTO `Package` (id_set, id_user, is_ready)
VALUES
    (1, 1, 0),
    (2, 2, 0),
    (3, 6, 0),
    (4, 6, 0);

-- INSERT INTO `Sample` (id_package, path, format)
-- VALUES
--     (3, '/path/to/sample1', 'Format A'),
--     (1, '/path/to/sample2', 'Format B'),
--     (4, '/path/to/sample3', 'Format A'),
--     (4, '/path/to/sample4', 'Format C'),
--     (5, '/path/to/sample5', 'Format B');


-- INSERT INTO `Examination` (id_user, id_sample, to_further_verification, bad_quality)
-- VALUES
--     (1, 1, 0, 0),
--     (2, 2, 1, 0),
--     (3, 3, 0, 1),
--     (4, 4, 1, 0),
--     (2, 5, 0, 0);

INSERT INTO `Label` (id_set, name, description, color)
VALUES
    (1, 'Label 1', 'Label Description 1', 'blue'),
    (1, 'Label 2', 'Label Description 2', 'red'),
    (2, 'Label 3', 'Label Description 3', 'cyan'),
    (3, 'Label 4', 'Label Description 4', 'green'),
    (4, 'Label 5', 'Label Description 5', 'pink');


-- INSERT INTO `BBox` (id_examination, id_label, comment, x, y, width, height)
-- VALUES
--     (1, 1, 'Comment 1', 10, 20, 30, 40),
--     (2, 2, 'Comment 2', 15, 25, 35, 45),
--     (3, 3, 'Comment 3', 20, 30, 40, 50),
--     (4, 4, 'Comment 4', 25, 35, 45, 55),
--     (2, 5, 'Comment 5', 30, 40, 50, 60);

-- PLEASE DO NOT ADD INVALID DATA (E.G BBox WITH LABEL FROM OTHER SET)
