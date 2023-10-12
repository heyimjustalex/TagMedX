# TagMedX: Open-Source Medical Image Annotation 🏥

TagMedX is an open-source web app built with FastAPI, Next.js, and MySQL, designed for medical image tagging – both classification and detection. It's a tool for healthcare professionals, such as doctors and medical experts, to annotate medical images remotely for AI systems. 

## 🚀  Quickstart

```bash

git clone https://github.com/heyimjustalex/TagMedX.git
cd TagMedX

```
Start without frontend, just backend, DB, and DBAdmin
```bash 
docker-compose up --build
```
Start whole project (with frontend)

```bash
docker-compose -f docker-compose_all.yml up --build
```

## Database

SQL file in /DB/setup.sql (with some random data loading). <br> In /DB folder there are also screenshots of scheme and dbdiagram.io code if modification of scheme is needed. <br>
Scheme might also be viewed in PHPMyadmin

![dbdiagram](./DB/2.PNG)

### Structure
```markdown
Each structure modification must result in backend model update of SQLAlchemy in ./backend/models

    **User:**
        Fields: id, e_mail, password_hash, name, surname, title, role, description, experience
        Purpose:  entity representing a doctor or an admin who controlls datasets
        Relationships: 
            - One-to-Many with Membership
            - One-to-Many with Examination

    **Group:**
        Fields: id, name, description
        Purpose: Represents a group or team of users that will mark a some data set. <br> For example a group of dentists marking teeth dataset
        Relationships: 
            - One-to-Many with Task
            - One-to-Many with Membership

    **Membership:**
        Fields: id_user, id_group
        Purpose: Represents the membership of users in groups.
        Relationships: 
            - Many-to-One with User 
            - Many-to-One with Group

    **Task:**
        Fields: id, id_group, max_samples_for_user, name, description, type
        Purpose: Represents tasks that are created by user with role="admin/manager".<br> A Group is linked with Task, so that a group of doctors<br> can have many tasks assigned. Task is a representation of activity <br>dataset marking. 
        Relationships: 
            - Many-to-One with Group
            - One-to-Many with Sample (one task has multiple photos/samples to mark)
            - One-to-Many with Label (a task has some labels assigned by admin that a doctor might later choose from)

    **Sample:**
        Fields: id, id_task, path, format
        Purpose: Represents samples (information about added photos) to be examined.
        Relationships: 
            - Many-to-One with Task       

    **Examination:**
        Fields: id, id_user, id_sample, to_further_verification, bad_quality
        Purpose: Records information about Sample Examination by User (doctor). <br>It might be detection or classification. <br>If classification there is just one bounding box (BBox).
        Relationships: 
            - Many-to-One with User
            - Many-to-One with Sample
            - One-to-Many with BBox (during single Sample Examination by a particular User he might crop some data on Sample with one BBox or with many. It depends on type of sample)

    **Label:**
        Fields: id, id_task, name, description
        Purpose: Represents labels for tasks that are constrained by admin/manager who creates Task.
        Relationships: 
            - Many-to-One with Task
            - One-to-Many with BBox

    **BBox:**
        Fields: id, id_examination, id_label, comment, x1, y1, x2, y2
        Purpose: Stores bounding box details. <br> x1,y1 means bottom-left corner and x2,y2 top-right corner.
        Relationships: 
            - Many-to-One with Examination
            - Many-to-One with Label


```
## Backend

### General

Project has hot-reload with Docker and it gets started with compose. Written with FastAPI.

### TODO - Deadline: 2.11.2023 but it would be better to end this part up to 26.10.2023
- Register/Login with JWT (dogadajcie się z Michałem jak to zrobić)
- Adding user to a group, getting users that are part of a group
- File (photos) upload (create some new assets folder for uploaded photos) 
- Possibility to print information about photos

### Naming conventions

1. Use typing and linter
2. Try to stick to PEP8. 

- methods: snake_case
- classes: PascalCase

### Project structure

Backend project is divided into 3 main folders: features, models, repositories. Features have user-domain specific folders like groups, users or tasks. Each of these subfolders has it's own controllers, schemas and services. Some facts:
- If you want to make new feature make new folder in feature folder
- Models are mapped to MySQL database entities defined in /DB/setup.sql. Any change made to model any of these means the other needs to be changed.
- Backend is dockerized and avaliable at localhost:8000 (You can test endpoints users/1 or /users)

```
├── backend                   <- FastAPI backend
│   ├── features              <- Domain specific features
        ├── exceptions        <- Our defined exceptions
            ├── definitions   <- Exceptions definitions (used by services)
            ├── handlers      <- Excaptions hanlders used by app.py
|   |   ├── examination       <- Sample examination related features
|   |   ├── groups            <- Group related features
|   |   ├── tasks             <- Tasks related features
|   |   ├── users             <- Users related features
|   |   |   ├── controllers   <- Router and endpoints /users /users/id
|   |   |   ├── schemas       <- Pydantic schemas for response
|   |   |   ├── services      <- Layer talking to Repositories
│   ├── models                <- SQLAlchemy data models
│   ├── repositories          <- SQLAlchemy queries
│   ├── utilities             <- Utilities like database connector or session
│   ├── requirements.txt      <- Packages to install
│   ├── Dockerfile            <- Dockerfile for Docker image
```
<br>


## Dependencies
- Database -  mysql:8.1.0
- Database Admin Panel - phpmyadmin:5.2.1
- Backend (FastAPI) - python:3.8 - (additional dependencies in ./backend/requirements.txt)
- Frontend (Next.js + TS) -  node:20 - (additional dependencies in ./frontend/package.json)