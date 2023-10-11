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
  label_id INT,
  comment VARCHAR(255),
  x1 FLOAT,
  y1 FLOAT,
  x2 FLOAT,
  y2 FLOAT,
  PRIMARY KEY (id),
  FOREIGN KEY (id_examination) REFERENCES `Examination`(id),
  FOREIGN KEY (label_id) REFERENCES `Label`(id)
);
